# CosyVoice-JP

CosyVoice3 の日本語対応フォーク版 - Windows ネイティブ対応 + Whisper 自動文字起こし統合

![CosyVoice-JP GUI](./asset/CosyVoiceJP-GUI.png)

## 特徴

- **GUI完全日本語化**: すべてのUI要素を日本語に翻訳
- **Whisper自動文字起こし**: プロンプト音声の内容を自動でテキスト化
- **Windowsネイティブ対応**: DLLロード問題、torchcodec問題を解決
- **ワンクリック起動**: `run.bat` をダブルクリックするだけで起動
- **自動ポート選択**: 使用中のポートを自動回避

## 元リポジトリからの変更点

| ファイル | 変更内容 |
|----------|----------|
| `webui.py` | GUI日本語化、Whisper統合、Windows互換性修正 |
| `launcher.py` | 自動ポート選択、ブラウザ自動起動（新規） |
| `run.bat` | ワンクリック起動スクリプト（新規） |
| `cosyvoice/utils/file_utils.py` | torchcodec問題の回避パッチ |

## 動作環境

- **OS**: Windows 10/11
- **GPU**: NVIDIA GPU（CUDA対応）
- **Python**: 3.10
- **特記**: RTX 5090 対応（PyTorch nightly cu128）

## インストール手順

### 1. リポジトリのクローン

```bash
git clone --recursive https://github.com/hiroki-abe-58/CosyVoice-JP.git
cd CosyVoice-JP
git submodule update --init --recursive
```

### 2. Conda環境の作成

```bash
conda create -n cosyvoice3 python=3.10 -y
conda activate cosyvoice3
```

### 3. 依存関係のインストール

```bash
# PyTorch（CUDA 12.8対応、RTX 5090の場合はnightly必須）
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu128

# その他の依存関係
pip install -r requirements.txt

# Whisper（自動文字起こし用）
pip install openai-whisper

# Windows互換性のための追加パッケージ
pip install soundfile
pip install "ruamel.yaml>=0.15.0,<0.18.0"
```

### 4. モデルのダウンロード

```python
from huggingface_hub import snapshot_download
snapshot_download('FunAudioLLM/Fun-CosyVoice3-0.5B-2512', 
                  local_dir='pretrained_models/Fun-CosyVoice3-0.5B-2512')
```

### 5. 起動

`run.bat` をダブルクリック、またはコマンドラインから：

```bash
conda activate cosyvoice3
python launcher.py
```

## 使い方

### 3秒ボイスクローン
1. プロンプト音声をアップロードまたは録音
2. 「自動文字起こし」ボタンでテキストを取得
3. 合成テキストを入力
4. 「音声を生成」をクリック

### 多言語クローン
1. プロンプト音声をアップロード（例：英語）
2. 合成テキストを別の言語で入力（例：日本語）
3. 「音声を生成」をクリック

### 自然言語制御
1. プロンプト音声をアップロード
2. 指示テキストを入力（例：「優しく話して」「早口で」）
3. 「音声を生成」をクリック

## ライセンス

- **CosyVoice**: Apache License 2.0 (c) Alibaba Inc
- **Whisper**: MIT License (c) OpenAI
- **Matcha-TTS**: MIT License

本フォーク版も Apache License 2.0 に従います。

## 免責事項

- 本ソフトウェアは「現状のまま」提供され、明示または黙示を問わず、いかなる種類の保証もありません
- 音声クローン技術の悪用（なりすまし、詐欺、名誉毀損等）は固く禁じます
- 生成された音声の利用については、利用者自身の責任において行ってください
- 本ソフトウェアの使用により生じたいかなる損害についても、開発者は責任を負いません
- 各国・地域の法令を遵守してご利用ください

## 謝辞

- 元リポジトリ: [FunAudioLLM/CosyVoice](https://github.com/FunAudioLLM/CosyVoice)
- Alibaba FunAudioLLM チームの素晴らしい研究に感謝します
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Matcha-TTS](https://github.com/shivammehta25/Matcha-TTS)

## 引用

```bibtex
@article{du2025cosyvoice,
  title={CosyVoice 3: Towards In-the-wild Speech Generation via Scaling-up and Post-training},
  author={Du, Zhihao and others},
  journal={arXiv preprint arXiv:2505.17589},
  year={2025}
}
```
