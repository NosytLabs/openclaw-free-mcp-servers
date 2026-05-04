# Troubleshooting Guide

## Common Issues

### 1. Import Errors

**Error:** `ModuleNotFoundError: No module named 'torch'`

**Solution:**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

**Error:** `ModuleNotFoundError: No module named 'kokoro'`

**Solution:**
```bash
pip install kokoro soundfile
```

### 2. CUDA Issues

**Error:** `CUDA out of memory`

**Solutions:**
1. Use smaller model:
   ```
   Generate with sdxl-turbo: your prompt
   ```

2. Reduce resolution:
   - Default: 1024x1024
   - Try: 512x512 or 768x768

3. Clear GPU memory:
   ```python
   import torch
   torch.cuda.empty_cache()
   ```

**Error:** `CUDA not available`

**Solutions:**
1. Check NVIDIA driver:
   ```bash
   nvidia-smi
   ```

2. Reinstall PyTorch with CUDA:
   ```bash
   pip uninstall torch torchvision
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
   ```

### 3. Model Download Issues

**Error:** `Connection timeout` or `Download failed`

**Solutions:**
1. Check internet connection
2. Verify disk space (need 20GB+)
3. Try again (downloads resume)
4. Manual download:
   ```python
   from huggingface_hub import snapshot_download
   snapshot_download("ByteDance/SDXL-Lightning")
   ```

### 4. Generation Quality Issues

**Problem:** Blurry or low-quality images

**Solutions:**
1. Use more steps:
   ```
   Generate 30 step image: your prompt
   ```

2. Use better model:
   ```
   Generate with sdxl-base: your prompt
   ```

3. Add quality terms:
   ```
   Generate: your prompt, masterpiece, best quality, highly detailed
   ```

**Problem:** Wrong content generated

**Solutions:**
1. Be more specific:
   - Bad: "Generate a person"
   - Good: "Generate a portrait of a young woman with brown hair, 
     smiling, outdoor setting, natural lighting"

2. Use negative prompts:
   ```
   Generate: beautiful landscape, avoid: people, buildings, text
   ```

### 5. TTS Issues

**Problem:** Robotic or unnatural voice

**Solutions:**
1. Try different voice:
   ```
   TTS with af_heart: your text
   ```

2. Add punctuation:
   - Use periods, commas
   - Add exclamation points for emphasis

3. Break into shorter sentences

**Problem:** Wrong pronunciation

**Solutions:**
1. Use phonetic spelling
2. Add spaces: "N A S A" instead of "NASA"
3. Try different voice

### 6. OpenClaw Integration Issues

**Problem:** MCP server not found

**Solutions:**
1. Verify installation:
   ```bash
   ls ~/.openclaw/mcp-servers/
   ```

2. Re-copy files:
   ```bash
   cp -r mcp-servers/* ~/.openclaw/mcp-servers/
   ```

3. Restart OpenClaw:
   ```bash
   openclaw gateway restart
   ```

**Problem:** OpenClaw doesn't call MCP server

**Solutions:**
1. Check config:
   ```bash
   openclaw config show
   ```

2. Re-import config:
   ```bash
   openclaw config import openclaw-config.json
   ```

3. Check logs:
   ```bash
   openclaw logs
   ```

## Performance Optimization

### Faster Generation

1. **Use Lightning models:**
   - `sdxl-lightning` (4 steps)
   - `sdxl-turbo` (1 step)

2. **Reduce resolution:**
   - 512x512: 4x faster than 1024x1024

3. **Keep model loaded:**
   - First generation: slow (loads model)
   - Subsequent: fast (reuses model)

### Lower Memory Usage

1. **Enable CPU offload:**
   ```python
   pipeline.enable_model_cpu_offload()
   ```

2. **Use attention slicing:**
   ```python
   pipeline.enable_attention_slicing()
   ```

3. **Reduce batch size:**
   - Generate one image at a time

## Getting Help

1. **Check GitHub Issues:**
   https://github.com/NosytLabs/openclaw-free-mcp-servers/issues

2. **Create New Issue:**
   Include:
   - Error message
   - Python version
   - GPU model & VRAM
   - Steps to reproduce

3. **Community:**
   - OpenClaw Discord
   - GitHub Discussions
