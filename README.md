# OpenClaw Free MCP Servers

[![GitHub stars](https://img.shields.io/github/stars/Tyson/openclaw-free-mcp-servers?style=social)](https://github.com/Tyson/openclaw-free-mcp-servers/stargazers)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)

🎨 **FREE Image Generation** and 🔊 **FREE Text-to-Speech** MCP servers for [OpenClaw](https://openclaw.ai) - No API keys required!

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/Tyson/openclaw-free-mcp-servers.git
cd openclaw-free-mcp-servers

# Install dependencies
pip install -r requirements.txt

# Copy MCP servers to OpenClaw
mkdir -p ~/.openclaw/mcp-servers
cp -r mcp-servers/* ~/.openclaw/mcp-servers/

# Update OpenClaw config
openclaw config import openclaw-config.json

# Restart OpenClaw
openclaw gateway restart
```

## 📦 What's Included

### 1. Image Generation MCP Server 🎨

**File:** `mcp-servers/image-generation/server.py`

Generate images locally using Stable Diffusion XL - **FREE**, no API keys!

**Features:**
- SDXL Lightning (4 steps, fast)
- SDXL Turbo (1 step, real-time)
- SDXL Base (30 steps, highest quality)
- Playground v2.5 (aesthetic focus)

**Requirements:**
- NVIDIA GPU with 8GB+ VRAM
- CUDA 12.1+

**Try it:**
```
Generate an image of a futuristic city at sunset
Create a cyberpunk portrait, neon lighting
```

### 2. Kokoro TTS MCP Server 🔊

**File:** `mcp-servers/kokoro-tts/server.py`

Text-to-speech using Kokoro-82M model - **FREE**, runs on CPU!

**Features:**
- 82M parameter model (ultra-lightweight)
- 10 voices (American/British)
- 9 languages supported
- Telegram voice message optimized

**Requirements:**
- Any CPU
- 500MB RAM

**Try it:**
```
Read this aloud: Hello from OpenClaw!
Create a voice message saying: Hey! Check this out!
```

## 💰 Cost Savings

| Feature | API Cost | This Solution | Monthly Savings |
|---------|----------|---------------|-----------------|
| Image Generation | $0.04/image (DALL-E) | **$0** | ~$120/1000 images |
| Text-to-Speech | $0.03/1K chars (ElevenLabs) | **$0** | ~$90/3M chars |
| **Total** | | | **~$210/month** |

## 📋 Test Results

### Latest Test Run: 2026-04-19

```
OpenClaw MCP Server Test Suite
==================================================
Testing: Image Generation (Simple)
==================================================
[PASS] Server starts correctly

Testing: Image Generation (Full)
==================================================
[PASS] Server starts correctly

Testing: Kokoro TTS
==================================================
[PASS] Server starts correctly

Total: 3/3 servers working

Dependency Check
==================================================
[OK] PyTorch: INSTALLED
[OK] Diffusers: INSTALLED
[OK] Transformers: INSTALLED
[OK] Kokoro TTS: INSTALLED
[OK] SoundFile: INSTALLED
[OK] MCP SDK: INSTALLED
[OK] Pillow (PIL): INSTALLED

Dependencies: 7/7 installed
```

### System Requirements Test

| Component | Status | Notes |
|-----------|--------|-------|
| PyTorch CPU | ✅ | 2.7.1+cpu |
| PyTorch CUDA | ⚠️ | Not available (CPU mode) |
| Diffusers | ✅ | 0.32.0 |
| Transformers | ✅ | 4.57.3 |
| Kokoro | ✅ | Installed |
| SoundFile | ✅ | Installed |
| MCP SDK | ✅ | Installed |

## 🔧 Installation

### Option 1: Automated Setup (Windows)

```batch
# Run as Administrator
.\install-all-deps.bat
```

### Option 2: Manual Installation

```bash
# PyTorch with CUDA (recommended)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# Or PyTorch CPU-only
pip install torch torchvision

# Image generation
pip install diffusers transformers accelerate Pillow

# Text-to-speech
pip install kokoro soundfile

# MCP SDK
pip install mcp
```

### Option 3: PowerShell Script

```powershell
# Run as Administrator
.\setup-enhanced-openclaw.ps1
```

## ⚙️ Configuration

Add to your `~/.openclaw/openclaw.json`:

```json
{
  "mcp": {
    "servers": {
      "image-generation": {
        "command": "python",
        "args": [
          "/path/to/openclaw-free-mcp-servers/mcp-servers/image-generation/server.py"
        ],
        "description": "FREE local image generation using SDXL"
      },
      "kokoro-tts": {
        "command": "python",
        "args": [
          "/path/to/openclaw-free-mcp-servers/mcp-servers/kokoro-tts/server.py"
        ],
        "description": "FREE text-to-speech using Kokoro"
      }
    }
  }
}
```

Or use the provided config:

```bash
openclaw config import openclaw-config.json
```

## 🧪 Testing

### Run Tests

```bash
# Test all MCP servers
python test-mcp-servers.py

# Check dependencies
python -c "import torch; import diffusers; import kokoro; print('All OK!')"
```

### Manual Test Commands

**Image Generation:**
```bash
# Start the server manually
python mcp-servers/image-generation/server.py
```

**TTS:**
```bash
# Start the server manually
python mcp-servers/kokoro-tts/server.py
```

## 📁 Repository Structure

```
openclaw-free-mcp-servers/
├── mcp-servers/
│   ├── image-generation/
│   │   ├── server.py              # Full image generation server
│   │   └── server-simple.py      # Status-only server
│   └── kokoro-tts/
│       └── server.py             # TTS server
├── tests/
│   └── test-mcp-servers.py       # Automated tests
├── docs/
│   ├── INTEGRATION-REPORT.md     # Detailed setup guide
│   ├── QUICK-START.md            # Quick reference
│   └── STATUS-REPORT.md          # Current status
├── openclaw-config.json          # Sample OpenClaw config
├── requirements.txt              # Python dependencies
├── install-all-deps.bat          # Windows installer
├── setup-enhanced-openclaw.ps1   # PowerShell setup
└── README.md                     # This file
```

## 🔍 Available Tools

### Image Generation

| Tool | Description | Parameters |
|------|-------------|------------|
| `generate_image_free` | Generate images | prompt, model, width, height, negative_prompt, seed |
| `list_image_models` | List available models | - |
| `check_image_gen_status` | Check dependencies | - |

### Text-to-Speech

| Tool | Description | Parameters |
|------|-------------|------------|
| `text_to_speech` | Convert text to speech | text, voice, language, speed, format |
| `speak_telegram_voice` | Generate Telegram voice | text, voice |
| `list_voices` | List available voices | - |

### Voice Options

**American:**
- `af_heart` - Warm, clear (default)
- `af_bella` - Soft, gentle
- `af_nicole` - Professional
- `af_sarah` - Neutral
- `am_adam` - Deep, authoritative
- `am_michael` - Friendly

**British:**
- `bf_emma` - Warm
- `bf_isabella` - Clear
- `bm_george` - Professional
- `bm_lewis` - Friendly

## 🛠️ Troubleshooting

### Image Generation Not Working

```bash
# Check GPU
nvidia-smi

# Check PyTorch CUDA
python -c "import torch; print(torch.cuda.is_available())"

# If CUDA not available, reinstall PyTorch:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

### TTS Not Working

```bash
# Install missing dependencies
pip install kokoro soundfile

# Windows: Install espeak-ng
# Download from: https://github.com/espeak-ng/espeak-ng/releases
```

### MCP Server Connection Issues

```bash
# Check server paths in config
openclaw config get mcp.servers

# Test server manually
python mcp-servers/image-generation/server-simple.py

# Restart OpenClaw
openclaw gateway restart
```

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Credits

- **Diffusers** by Hugging Face - Image generation pipeline
- **Kokoro** by Hexgrad - Text-to-speech model
- **OpenClaw** - The amazing agent framework
- **ClawHub** - Skills and plugins registry

## 📚 Resources

- [OpenClaw Docs](https://docs.openclaw.ai)
- [ClawHub Skills](https://clawhub.ai/skills)
- [ClawHub Plugins](https://clawhub.ai/plugins)
- [Diffusers Docs](https://huggingface.co/docs/diffusers)
- [Kokoro GitHub](https://github.com/hexgrad/kokoro)

## ⭐ Show Your Support

If this project helps you save money on API costs, please give it a star on GitHub!

---

**Made with ❤️ for the OpenClaw community**
