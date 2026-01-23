# Copyright (c) 2024 Alibaba Inc (authors: Xiang Lyu, Liu Yue)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import sys
import argparse
# Import torch first before gradio to avoid DLL loading issues on Windows
import torch
import torchaudio
import numpy as np
import gradio as gr
import soundfile as sf
import random
import librosa
import whisper
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append('{}/third_party/Matcha-TTS'.format(ROOT_DIR))
from cosyvoice.cli.cosyvoice import AutoModel
from cosyvoice.utils.file_utils import logging
from cosyvoice.utils.common import set_all_random_seed

# Whisper model for transcription (lazy loading)
whisper_model = None

# CosyVoice3 supports: zero_shot, cross_lingual, instruct2
# Note: CosyVoice3 does NOT support sft (preset voices) or original instruct mode
inference_mode_list = ['3秒ボイスクローン', '多言語クローン', '自然言語制御']
instruct_dict = {'3秒ボイスクローン': '1. プロンプト音声ファイルを選択、または録音（30秒以内）\n   ※両方指定した場合はファイルが優先されます\n2. プロンプトテキストを入力（自動文字起こし推奨）\n3. 音声生成ボタンをクリック',
                 '多言語クローン': '1. プロンプト音声ファイルを選択、または録音（30秒以内）\n   ※両方指定した場合はファイルが優先されます\n2. 音声生成ボタンをクリック',
                 '自然言語制御': '1. プロンプト音声ファイルを選択、または録音\n2. 指示テキストを入力（例: 優しく話して）\n3. 音声生成ボタンをクリック'}
stream_mode_list = [('オフ', False), ('オン', True)]
max_val = 0.8

# Language options for explicit language control
language_list = [
    ('自動検出', ''),
    ('日本語', '日本語で話してください。'),
    ('中国語', '请用中文说。'),
    ('英語', 'Please speak in English.'),
    ('韓国語', '한국어로 말해주세요.'),
    ('ドイツ語', 'Bitte sprechen Sie auf Deutsch.'),
    ('フランス語', 'Parlez en français, s\'il vous plaît.'),
    ('スペイン語', 'Por favor, habla en español.'),
    ('イタリア語', 'Per favore, parla in italiano.'),
    ('ロシア語', 'Пожалуйста, говорите по-русски.'),
]


def load_whisper_model(model_size="base"):
    """Load Whisper model (lazy loading)."""
    global whisper_model
    if whisper_model is None:
        logging.info(f"Loading Whisper model: {model_size}")
        whisper_model = whisper.load_model(model_size)
        logging.info("Whisper model loaded successfully")
    return whisper_model

def transcribe_audio(prompt_wav_upload, prompt_wav_record, whisper_model_size):
    """Transcribe audio using Whisper."""
    # Determine which audio to use
    if prompt_wav_upload is not None:
        audio_path = prompt_wav_upload
    elif prompt_wav_record is not None:
        audio_path = prompt_wav_record
    else:
        gr.Warning("文字起こしする音声ファイルがありません。音声をアップロードまたは録音してください。")
        return ""
    
    try:
        gr.Info("文字起こしを開始します...")
        model = load_whisper_model(whisper_model_size)
        
        # Transcribe
        result = model.transcribe(audio_path, language=None)  # Auto-detect language
        transcribed_text = result["text"].strip()
        detected_lang = result.get("language", "unknown")
        
        gr.Info(f"文字起こし完了 (検出言語: {detected_lang})")
        logging.info(f"Transcription completed: {transcribed_text[:50]}...")
        
        return transcribed_text
    except Exception as e:
        gr.Warning(f"文字起こしエラー: {str(e)}")
        logging.error(f"Transcription error: {e}")
        return ""

def generate_seed():
    seed = random.randint(1, 100000000)
    return {
        "__type__": "update",
        "value": seed
    }


def change_instruction(mode_checkbox_group):
    return instruct_dict[mode_checkbox_group]


def generate_audio(tts_text, mode_checkbox_group, sft_dropdown, prompt_text, prompt_wav_upload, prompt_wav_record, instruct_text,
                   seed, stream, speed, language_hint):
    if prompt_wav_upload is not None:
        prompt_wav = prompt_wav_upload
    elif prompt_wav_record is not None:
        prompt_wav = prompt_wav_record
    else:
        prompt_wav = None
    
    # All CosyVoice3 modes require prompt audio
    if prompt_wav is None:
        gr.Warning('プロンプト音声が空です。音声ファイルを指定してください。')
        yield (cosyvoice.sample_rate, default_data)
        return
    
    # Check audio file
    try:
        wav_info = sf.info(prompt_wav)
        if wav_info.samplerate < prompt_sr:
            gr.Warning('プロンプト音声のサンプリングレート({})が{}未満です。'.format(wav_info.samplerate, prompt_sr))
            yield (cosyvoice.sample_rate, default_data)
            return
    except Exception as e:
        gr.Warning(f'プロンプト音声の読み込みに失敗しました: {str(e)}')
        yield (cosyvoice.sample_rate, default_data)
        return
    
    # Mode-specific validation
    if mode_checkbox_group == '自然言語制御':
        if instruct_text == '':
            gr.Warning('自然言語制御モードでは指示テキストが必要です。例: 優しく話して')
            yield (cosyvoice.sample_rate, default_data)
            return
    
    if mode_checkbox_group == '多言語クローン':
        if instruct_text != '':
            gr.Info('多言語クローンモードでは、指示テキストは無視されます。')
        gr.Info('多言語クローンモードでは、合成テキストとプロンプト音声を異なる言語にしてください。')
    
    if mode_checkbox_group == '3秒ボイスクローン':
        if prompt_text == '':
            gr.Warning('プロンプトテキストが空です。自動文字起こしボタンを使用してください。')
            yield (cosyvoice.sample_rate, default_data)
            return
        if instruct_text != '':
            gr.Info('3秒ボイスクローンモードでは、指示テキストは無視されます。')

    # Build language instruction if specified (only used in 自然言語制御 mode)
    lang_instruction = language_hint if language_hint else ''
    
    # Generate audio based on mode
    # Note: 3秒ボイスクローン uses zero_shot for best voice cloning quality
    #       Language selection only affects 自然言語制御 mode
    try:
        if mode_checkbox_group == '3秒ボイスクローン':
            # Use zero_shot for best voice cloning (language selection ignored for quality)
            prompt_text_processed = prompt_text
            if '<|endofprompt|>' not in prompt_text_processed:
                prompt_text_processed = 'You are a helpful assistant.<|endofprompt|>' + prompt_text_processed
            logging.info('get zero_shot inference request (voice cloning priority)')
            logging.info(f'tts_text: {tts_text}')
            logging.info(f'prompt_text_processed: {prompt_text_processed}')
            set_all_random_seed(seed)
            for i in cosyvoice.inference_zero_shot(tts_text, prompt_text_processed, prompt_wav, stream=stream, speed=speed):
                yield (cosyvoice.sample_rate, i['tts_speech'].numpy().flatten())
        elif mode_checkbox_group == '多言語クローン':
            logging.info('get cross_lingual inference request')
            tts_text_processed = tts_text
            if '<|endofprompt|>' not in tts_text_processed:
                tts_text_processed = 'You are a helpful assistant.<|endofprompt|>' + tts_text_processed
            logging.info(f'tts_text_processed: {tts_text_processed}')
            set_all_random_seed(seed)
            for i in cosyvoice.inference_cross_lingual(tts_text_processed, prompt_wav, stream=stream, speed=speed):
                yield (cosyvoice.sample_rate, i['tts_speech'].numpy().flatten())
        elif mode_checkbox_group == '自然言語制御':
            # CosyVoice3 uses inference_instruct2
            # Language selection is applied here
            logging.info('get instruct2 inference request')
            combined_instruct = instruct_text
            if lang_instruction:
                combined_instruct = f'{lang_instruction} {instruct_text}'
            instruct_text_processed = f'You are a helpful assistant. {combined_instruct}<|endofprompt|>'
            logging.info(f'tts_text: {tts_text}')
            logging.info(f'instruct_text_processed: {instruct_text_processed}')
            set_all_random_seed(seed)
            for i in cosyvoice.inference_instruct2(tts_text, instruct_text_processed, prompt_wav, stream=stream, speed=speed):
                yield (cosyvoice.sample_rate, i['tts_speech'].numpy().flatten())
    except Exception as e:
        logging.error(f'Audio generation error: {e}')
        import traceback
        traceback.print_exc()
        gr.Warning(f'音声生成エラー: {str(e)}')
        yield (cosyvoice.sample_rate, default_data)


def main():
    with gr.Blocks() as demo:
        gr.Markdown("### CosyVoice3 音声合成システム")
        gr.Markdown("#### 合成したいテキストを入力し、推論モードを選択して、手順に従って操作してください")

        tts_text = gr.Textbox(label="合成テキスト", lines=1, value="こんにちは。私はCosyVoice音声合成システムです。自然で快適な音声を生成できます。")
        with gr.Row():
            mode_checkbox_group = gr.Radio(choices=inference_mode_list, label='推論モード', value=inference_mode_list[0])
            instruction_text = gr.Text(label="操作手順", value=instruct_dict[inference_mode_list[0]], scale=0.5)
            sft_dropdown = gr.Dropdown(choices=sft_spk, label='プリセット音声', value=sft_spk[0], scale=0.25)
            stream = gr.Radio(choices=stream_mode_list, label='ストリーミング', value=stream_mode_list[0][1])
            speed = gr.Number(value=1, label="速度調整（非ストリーミング時のみ）", minimum=0.5, maximum=2.0, step=0.1)
            with gr.Column(scale=0.25):
                seed_button = gr.Button(value="\U0001F3B2")
                seed = gr.Number(value=0, label="ランダムシード")

        with gr.Row():
            prompt_wav_upload = gr.Audio(sources='upload', type='filepath', label='プロンプト音声ファイル（サンプリングレート16kHz以上）')
            prompt_wav_record = gr.Audio(sources='microphone', type='filepath', label='プロンプト音声を録音')
        
        with gr.Row():
            with gr.Column(scale=3):
                prompt_text = gr.Textbox(label="プロンプトテキスト", lines=1, placeholder="プロンプト音声の内容を入力、または自動文字起こしボタンをクリック...", value='')
            with gr.Column(scale=1):
                whisper_model_size = gr.Dropdown(
                    choices=["tiny", "base", "small", "medium", "large"],
                    value="base",
                    label="Whisperモデル"
                )
                transcribe_button = gr.Button("自動文字起こし (Whisper)")
        
        with gr.Row():
            with gr.Column(scale=2):
                instruct_text = gr.Textbox(label="指示テキスト", lines=1, placeholder="指示テキストを入力してください（例: 優しく話して、早口で）...", value='')
            with gr.Column(scale=1):
                language_dropdown = gr.Dropdown(
                    choices=[lang[0] for lang in language_list],
                    value=language_list[0][0],
                    label="出力言語（発音制御）"
                )

        generate_button = gr.Button("音声を生成")

        audio_output = gr.Audio(label="生成された音声", autoplay=True, streaming=True)

        # Helper function to convert language dropdown to instruction
        def get_language_hint(lang_name):
            for name, hint in language_list:
                if name == lang_name:
                    return hint
            return ''
        
        seed_button.click(generate_seed, inputs=[], outputs=seed)
        transcribe_button.click(
            transcribe_audio,
            inputs=[prompt_wav_upload, prompt_wav_record, whisper_model_size],
            outputs=[prompt_text]
        )
        
        # Wrapper to convert language dropdown value
        def generate_with_language(tts_text, mode, sft, prompt_text, wav_upload, wav_record, instruct, seed, stream, speed, lang_name):
            lang_hint = get_language_hint(lang_name)
            yield from generate_audio(tts_text, mode, sft, prompt_text, wav_upload, wav_record, instruct, seed, stream, speed, lang_hint)
        
        generate_button.click(generate_with_language,
                              inputs=[tts_text, mode_checkbox_group, sft_dropdown, prompt_text, prompt_wav_upload, prompt_wav_record, instruct_text,
                                      seed, stream, speed, language_dropdown],
                              outputs=[audio_output])
        mode_checkbox_group.change(fn=change_instruction, inputs=[mode_checkbox_group], outputs=[instruction_text])
    demo.queue(max_size=4, default_concurrency_limit=2)
    demo.launch(server_name='0.0.0.0', server_port=args.port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port',
                        type=int,
                        default=8000)
    parser.add_argument('--model_dir',
                        type=str,
                        default='pretrained_models/CosyVoice2-0.5B',
                        help='local path or modelscope repo id')
    args = parser.parse_args()
    cosyvoice = AutoModel(model_dir=args.model_dir)

    sft_spk = cosyvoice.list_available_spks()
    if len(sft_spk) == 0:
        sft_spk = ['']
    prompt_sr = 16000
    default_data = np.zeros(cosyvoice.sample_rate)
    main()
