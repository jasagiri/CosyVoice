![SVG Banners](https://svg-banners.vercel.app/api?type=origin&text1=CosyVoice🤠&text2=Text-to-Speech%20💖%20Large%20Language%20Model&width=800&height=210)

## CosyVoice — Apple Silicon Fork

This is a fork of [FunAudioLLM/CosyVoice](https://github.com/FunAudioLLM/CosyVoice) with **native Apple Silicon (MPS) support** and [CosyVoice-JP](https://github.com/hiroki-abe-58/CosyVoice-JP) Japanese localization.

### What's different from upstream

| Feature | CUDA (Linux) | MPS (Apple Silicon) | CPU |
|---------|:---:|:---:|:---:|
| Inference | ✅ | ✅ | ✅ |
| fp16 | ✅ | ✅ | ❌ |
| JIT | ✅ | ✅ | ❌ |
| TensorRT | ✅ | ❌ | ❌ |
| vLLM | ✅ | ❌ | ❌ |
| Training (DeepSpeed/DDP) | ✅ | ❌ | ❌ |

### Upstream links

**Fun-CosyVoice 3.0**: [Demos](https://funaudiollm.github.io/cosyvoice3/); [Paper](https://arxiv.org/pdf/2505.17589); [Modelscope](https://www.modelscope.cn/models/FunAudioLLM/Fun-CosyVoice3-0.5B-2512); [Huggingface](https://huggingface.co/FunAudioLLM/Fun-CosyVoice3-0.5B-2512); [CV3-Eval](https://github.com/FunAudioLLM/CV3-Eval)

**CosyVoice 2.0**: [Demos](https://funaudiollm.github.io/cosyvoice2/); [Paper](https://arxiv.org/pdf/2412.10117); [Modelscope](https://www.modelscope.cn/models/iic/CosyVoice2-0.5B); [HuggingFace](https://huggingface.co/FunAudioLLM/CosyVoice2-0.5B)

**CosyVoice 1.0**: [Demos](https://fun-audio-llm.github.io); [Paper](https://funaudiollm.github.io/pdf/CosyVoice_v1.pdf); [Modelscope](https://www.modelscope.cn/models/iic/CosyVoice-300M); [HuggingFace](https://huggingface.co/FunAudioLLM/CosyVoice-300M)

---

## Install

### macOS Apple Silicon (M1/M2/M3/M4)

``` sh
git clone --recursive https://github.com/jasagiri/CosyVoice.git
cd CosyVoice
bash setup_macos.sh
```

Or manually:

``` sh
conda create -n cosyvoice -y python=3.10
conda activate cosyvoice
conda install -c conda-forge pynini==2.1.5 -y
pip install torch torchaudio
pip install -r requirements.txt
git submodule update --init --recursive
```

### Linux with CUDA

``` sh
git clone --recursive https://github.com/jasagiri/CosyVoice.git
cd CosyVoice
conda create -n cosyvoice -y python=3.10
conda activate cosyvoice
pip install -r requirements-cuda.txt
```

### Model download

We strongly recommend that you download our pretrained `Fun-CosyVoice3-0.5B` `CosyVoice2-0.5B` `CosyVoice-300M` `CosyVoice-300M-SFT` `CosyVoice-300M-Instruct` model and `CosyVoice-ttsfrd` resource.

``` python
# modelscope SDK model download
from modelscope import snapshot_download
snapshot_download('FunAudioLLM/Fun-CosyVoice3-0.5B-2512', local_dir='pretrained_models/Fun-CosyVoice3-0.5B')
snapshot_download('iic/CosyVoice2-0.5B', local_dir='pretrained_models/CosyVoice2-0.5B')
snapshot_download('iic/CosyVoice-300M', local_dir='pretrained_models/CosyVoice-300M')
snapshot_download('iic/CosyVoice-300M-SFT', local_dir='pretrained_models/CosyVoice-300M-SFT')
snapshot_download('iic/CosyVoice-300M-Instruct', local_dir='pretrained_models/CosyVoice-300M-Instruct')
snapshot_download('iic/CosyVoice-ttsfrd', local_dir='pretrained_models/CosyVoice-ttsfrd')

# for oversea users, huggingface SDK model download
from huggingface_hub import snapshot_download
snapshot_download('FunAudioLLM/Fun-CosyVoice3-0.5B-2512', local_dir='pretrained_models/Fun-CosyVoice3-0.5B')
snapshot_download('FunAudioLLM/CosyVoice2-0.5B', local_dir='pretrained_models/CosyVoice2-0.5B')
snapshot_download('FunAudioLLM/CosyVoice-300M', local_dir='pretrained_models/CosyVoice-300M')
snapshot_download('FunAudioLLM/CosyVoice-300M-SFT', local_dir='pretrained_models/CosyVoice-300M-SFT')
snapshot_download('FunAudioLLM/CosyVoice-300M-Instruct', local_dir='pretrained_models/CosyVoice-300M-Instruct')
snapshot_download('FunAudioLLM/CosyVoice-ttsfrd', local_dir='pretrained_models/CosyVoice-ttsfrd')
```

Optionally, you can unzip `ttsfrd` resource and install `ttsfrd` package for better text normalization performance.

Notice that this step is not necessary. If you do not install `ttsfrd` package, we will use wetext by default.

``` sh
cd pretrained_models/CosyVoice-ttsfrd/
unzip resource.zip -d .
pip install ttsfrd_dependency-0.1-py3-none-any.whl
pip install ttsfrd-0.4.2-cp310-cp310-linux_x86_64.whl
```

### Basic Usage

We strongly recommend using `Fun-CosyVoice3-0.5B` for better performance.
Follow the code in `example.py` for detailed usage of each model.
```sh
python example.py
```

#### vLLM Usage (CUDA only)
CosyVoice2/3 now supports **vLLM 0.11.x+ (V1 engine)** and **vLLM 0.9.0 (legacy)**.

``` sh
conda create -n cosyvoice_vllm --clone cosyvoice
conda activate cosyvoice_vllm
# for vllm==0.9.0
pip install vllm==v0.9.0 transformers==4.51.3 numpy==1.26.4
# for vllm>=0.11.0
pip install vllm==v0.11.0 transformers==4.57.1 numpy==1.26.4
python vllm_example.py
```

#### Start web demo

``` python
# change iic/CosyVoice-300M-SFT for sft inference, or iic/CosyVoice-300M-Instruct for instruct inference
python3 webui.py --port 50000 --model_dir pretrained_models/CosyVoice-300M
```

#### Build for deployment (CUDA only)

``` sh
cd runtime/python
docker build -t cosyvoice:v1.0 .
# for grpc usage
docker run -d --runtime=nvidia -p 50000:50000 cosyvoice:v1.0 /bin/bash -c "cd /opt/CosyVoice/CosyVoice/runtime/python/grpc && python3 server.py --port 50000 --max_conc 4 --model_dir iic/CosyVoice-300M && sleep infinity"
cd grpc && python3 client.py --port 50000 --mode <sft|zero_shot|cross_lingual|instruct>
# for fastapi usage
docker run -d --runtime=nvidia -p 50000:50000 cosyvoice:v1.0 /bin/bash -c "cd /opt/CosyVoice/CosyVoice/runtime/python/fastapi && python3 server.py --port 50000 --model_dir iic/CosyVoice-300M && sleep infinity"
cd fastapi && python3 client.py --port 50000 --mode <sft|zero_shot|cross_lingual|instruct>
```

---

## Apple Silicon Technical Details

This fork introduces a device abstraction layer (`cosyvoice/utils/device.py`) that automatically selects the best available backend:

- **CUDA** (Linux/Windows with NVIDIA GPU) — full feature set
- **MPS** (macOS Apple Silicon) — inference with fp16 and JIT support
- **CPU** — fallback for all platforms

TensorRT, vLLM, and DeepSpeed are CUDA-only and are gracefully disabled on non-CUDA platforms with appropriate warnings.

Upstream PR: [FunAudioLLM/CosyVoice#1869](https://github.com/FunAudioLLM/CosyVoice/pull/1869)

## Japanese Localization (CosyVoice-JP)

This fork incorporates changes from [CosyVoice-JP](https://github.com/hiroki-abe-58/CosyVoice-JP) by @hiroki-abe-58:

- **Japanese WebUI** — `webui.py` with Japanese interface strings
- **Windows native support** — DLL load order fix, torchaudio/soundfile fallback, sox alternative
- **Port auto-detection** — `launcher.py` for automatic free port selection
- **Windows quick start** — `run.bat` for one-click launch

CosyVoice natively supports Japanese as one of its 9 languages. The upstream model (`Fun-CosyVoice3-0.5B`) works for Japanese TTS out of the box — no additional Japanese-specific model is required.

## Credits

- [FunAudioLLM/CosyVoice](https://github.com/FunAudioLLM/CosyVoice) — Original project by Alibaba
- [CosyVoice-JP](https://github.com/hiroki-abe-58/CosyVoice-JP) by @hiroki-abe-58 — Japanese localization and Windows compatibility

## Citations

``` bibtex
@article{du2024cosyvoice,
  title={Cosyvoice: A scalable multilingual zero-shot text-to-speech synthesizer based on supervised semantic tokens},
  author={Du, Zhihao and Chen, Qian and Zhang, Shiliang and Hu, Kai and Lu, Heng and Yang, Yexin and Hu, Hangrui and Zheng, Siqi and Gu, Yue and Ma, Ziyang and others},
  journal={arXiv preprint arXiv:2407.05407},
  year={2024}
}

@article{du2024cosyvoice,
  title={Cosyvoice 2: Scalable streaming speech synthesis with large language models},
  author={Du, Zhihao and Wang, Yuxuan and Chen, Qian and Shi, Xian and Lv, Xiang and Zhao, Tianyu and Gao, Zhifu and Yang, Yexin and Gao, Changfeng and Wang, Hui and others},
  journal={arXiv preprint arXiv:2412.10117},
  year={2024}
}

@article{du2025cosyvoice,
  title={CosyVoice 3: Towards In-the-wild Speech Generation via Scaling-up and Post-training},
  author={Du, Zhihao and Gao, Changfeng and Wang, Yuxuan and Yu, Fan and Zhao, Tianyu and Wang, Hao and Lv, Xiang and Wang, Hui and Shi, Xian and An, Keyu and others},
  journal={arXiv preprint arXiv:2505.17589},
  year={2025}
}
```

## Disclaimer
The content provided above is for academic purposes only and is intended to demonstrate technical capabilities. Some examples are sourced from the internet. If any content infringes on your rights, please contact us to request its removal.
