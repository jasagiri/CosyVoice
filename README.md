# CosyVoice-JP

**CosyVoice3 の日本語対応フォーク版** - 世界初のWindowsネイティブ完全対応 + Whisper自動文字起こし統合

![CosyVoice-JP GUI](./asset/CosyVoiceJP-GUI.png)

---

## Why CosyVoice-JP?

元のCosyVoiceは **Linux専用** として開発されており、Windowsでの動作は公式にサポートされていませんでした。
本フォークは、複数のWindows固有の問題を解決し、**Windowsネイティブ環境での完全動作** を実現しました。

### 解決した技術的課題

| 問題 | 症状 | 解決策 |
|------|------|--------|
| **DLLロードエラー** | `OSError: Error loading c10.dll` - PyTorchのDLLが正しくロードされない | Pythonモジュールのインポート順序を最適化（torch → gradio） |
| **torchcodecエラー** | `TorchCodec is required` - Windowsで未サポートのコーデックを要求 | soundfileによるフォールバック処理を実装 |
| **sox依存問題** | Linux専用の音声処理ツールに依存 | 代替ライブラリで完全置換 |
| **torchaudio API変更** | PyTorch nightly版でのAPI破壊的変更 | soundfileベースの互換レイヤーを実装 |

---

## 特徴

### Windowsネイティブ完全対応
- **Linux専用だったCosyVoiceをWindowsで動作可能に**
- RTX 5090 (sm_120) などの最新GPUにも対応
- PyTorch nightly (CUDA 12.8) での動作確認済み
- ワンクリック起動（`run.bat`をダブルクリックするだけ）
- 自動ポート選択（使用中のポートを自動回避）

### GUI完全日本語化
- すべてのUI要素を日本語に翻訳
- 操作手順も日本語で表示
- エラーメッセージも日本語化

### Whisper自動文字起こし統合
- OpenAI Whisperをボタン一つで呼び出し
- プロンプト音声の内容を自動でテキスト化
- 言語自動検出対応

### 言語選択機能
- 出力言語（発音）を明示的に指定可能
- 日本語、英語、中国語、韓国語など9言語対応

---

## 元リポジトリからの変更点

| ファイル | 変更内容 |
|----------|----------|
| `webui.py` | GUI日本語化、Whisper統合、Windows互換性修正、言語選択機能 |
| `launcher.py` | 自動ポート選択、ブラウザ自動起動（**新規作成**） |
| `run.bat` | ワンクリック起動スクリプト（**新規作成**） |
| `cosyvoice/utils/file_utils.py` | torchcodec問題の回避パッチ、soundfileフォールバック |

---

## 動作環境

| 項目 | 要件 |
|------|------|
| **OS** | Windows 10/11（Linux非依存） |
| **GPU** | NVIDIA GPU（CUDA対応） |
| **Python** | 3.10 |
| **PyTorch** | nightly版推奨（CUDA 12.8対応） |
| **特記** | RTX 5090など最新GPU対応 |

---

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

**ワンクリック起動:**
`run.bat` をダブルクリック

**コマンドラインから:**
```bash
conda activate cosyvoice3
python launcher.py
```

ブラウザが自動で開き、`http://localhost:7865` でWebUIにアクセスできます。

---

## 使い方

### 3秒ボイスクローン（推奨）
1. プロンプト音声をアップロードまたは録音（3〜30秒）
2. 「自動文字起こし (Whisper)」ボタンでテキストを取得
3. 合成テキストを入力
4. 「音声を生成」をクリック

### 多言語クローン
1. プロンプト音声をアップロード（例：英語）
2. 合成テキストを別の言語で入力（例：日本語）
3. 「音声を生成」をクリック

### 自然言語制御
1. プロンプト音声をアップロード
2. 指示テキストを入力（例：「優しく話して」「早口で」「囁いて」）
3. 「音声を生成」をクリック

---

## ライセンス

| コンポーネント | ライセンス |
|----------------|------------|
| CosyVoice | Apache License 2.0 (c) Alibaba Inc |
| Whisper | MIT License (c) OpenAI |
| Matcha-TTS | MIT License |
| 本フォーク | Apache License 2.0 |

---

## 免責事項

- 本ソフトウェアは「現状のまま」提供され、明示または黙示を問わず、いかなる種類の保証もありません
- **音声クローン技術の悪用（なりすまし、詐欺、名誉毀損、ディープフェイク等）は固く禁じます**
- 生成された音声の利用については、利用者自身の責任において行ってください
- 本ソフトウェアの使用により生じたいかなる損害についても、開発者は責任を負いません
- 各国・地域の法令を遵守してご利用ください
- 他者の権利（肖像権、著作権、パブリシティ権等）を侵害しないようご注意ください

---

## 謝辞

- **元リポジトリ**: [FunAudioLLM/CosyVoice](https://github.com/FunAudioLLM/CosyVoice)
- Alibaba FunAudioLLM チームの素晴らしい研究に感謝します
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Matcha-TTS](https://github.com/shivammehta25/Matcha-TTS)

---

## 引用

```bibtex
@article{du2025cosyvoice,
  title={CosyVoice 3: Towards In-the-wild Speech Generation via Scaling-up and Post-training},
  author={Du, Zhihao and Gao, Changfeng and Wang, Yuxuan and others},
  journal={arXiv preprint arXiv:2505.17589},
  year={2025}
}
```
