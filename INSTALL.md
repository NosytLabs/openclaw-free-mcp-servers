# Installation Guide

## Prerequisites

### Hardware Requirements

**For Image Generation:**
- NVIDIA GPU with 8GB+ VRAM (12GB+ recommended)
- CUDA 12.1 or later
- 20GB+ free disk space for models

**For TTS Only:**
- CPU only (no GPU required!)
- 2GB+ RAM
- 1GB free disk space

### Software Requirements

- Python 3.10 or later
- pip package manager
- git (for cloning)

## Quick Install

### 1. Clone Repository

```bash
git clone https://github.com/NosytLabs/openclaw-free-mcp-servers.git
cd openclaw-free-mcp-servers
```

### 2. Install Dependencies

**Option A: Full Install (Image Generation + TTS)**

```bash
pip install -r requirements.txt
```

**Option B: CPU-Only (TTS Only)**

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install mcp kokoro soundfile numpy
```

**Option C: Install as Package**

```bash
pip install -e .
```

### 3. Verify Installation

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import mcp; print('MCP: OK')"
python -c "import kokoro; print('Kokoro: OK')"
```

## OpenClaw Integration

### 1. Copy MCP Servers

```bash
mkdir -p ~/.openclaw/mcp-servers
cp -r mcp-servers/* ~/.openclaw/mcp-servers/
```

### 2. Import Configuration

```bash
openclaw config import openclaw-config.json
```

### 3. Restart OpenClaw

```bash
openclaw gateway restart
```

### 4. Test

Ask OpenClaw:
```
Generate an image of a sunset over mountains
Convert this text to speech: Hello world
```

## Troubleshooting

### CUDA Out of Memory

Try smaller models:
- Use `sdxl-lightning` instead of `sdxl-base`
- Reduce image resolution
- Close other GPU applications

### Import Errors

```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Model Download Issues

Models auto-download on first use. If download fails:
- Check internet connection
- Verify disk space
- Try again (downloads resume automatically)

## Manual Model Installation

```python
from diffusers import StableDiffusionXLPipeline
import torch

# Pre-download model
pipeline = StableDiffusionXLPipeline.from_pretrained(
    "ByteDance/SDXL-Lightning",
    torch_dtype=torch.float16,
    variant="fp16"
)
```
