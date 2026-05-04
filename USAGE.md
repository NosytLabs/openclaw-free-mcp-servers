# Usage Guide

## Image Generation MCP Server

### Basic Usage

**Via OpenClaw:**
```
Generate an image of a futuristic city at sunset
Create a portrait of a robot, cyberpunk style
```

### Available Models

1. **SDXL Lightning** (Default)
   - Fastest (4 steps)
   - 8GB VRAM
   - Best for: Quick iterations

2. **SDXL Turbo**
   - Ultra-fast (1 step)
   - 8GB VRAM
   - Best for: Real-time generation

3. **SDXL Base**
   - Highest quality (30 steps)
   - 12GB VRAM
   - Best for: Final renders

4. **Playground v2.5**
   - Aesthetic focus (25 steps)
   - 10GB VRAM
   - Best for: Art/illustration

### Advanced Options

**Specify Model:**
```
Generate with sdxl-base: a majestic dragon
```

**Adjust Steps:**
```
Generate 50 step image of a landscape
```

**Negative Prompt:**
```
Generate a portrait, avoid: blurry, distorted, low quality
```

## Text-to-Speech MCP Server

### Basic Usage

**Via OpenClaw:**
```
Convert to speech: Hello, welcome to OpenClaw!
TTS with american female voice: This is a test
```

### Available Voices

**American English:**
- `af_heart` - Warm, clear female
- `af_bella` - Soft, gentle female
- `af_sarah` - Neutral female
- `am_adam` - Deep, authoritative male
- `am_michael` - Friendly male

**British English:**
- `bf_emma` - Soft, warm female
- `bf_isabella` - Clear female
- `bm_george` - Professional male
- `bm_lewis` - Friendly male

### Voice Selection

```
TTS with british male voice: Hello there!
Convert to speech with af_bella: Welcome back!
```

## Performance Tips

### Image Generation

1. **Start with Lightning**
   - Fastest model for testing prompts

2. **Use Lower Steps for Iteration**
   - 4-8 steps for drafts
   - 20-30 steps for finals

3. **Batch Generation**
   - Generate multiple at once
   - Reuses loaded model

### TTS

1. **CPU is Fine**
   - No GPU needed
   - Fast generation (~1s per sentence)

2. **Cache Results**
   - Save commonly used phrases
   - Reuse audio files

## Examples

### Creating Art

```
Generate with playground-v2.5: oil painting of a serene lake at dawn, 
impressionist style, golden hour lighting, reflection in water, 
masterpiece quality
```

### Quick Sketches

```
Generate with sdxl-turbo: simple sketch of a cat
```

### Voice Messages

```
TTS with am_adam: Welcome to our automated system. 
Please select from the following options.
```

### Multiple Languages

```
TTS in spanish: Hola, bienvenido!
TTS in french: Bonjour, comment allez-vous?
```

## Integration with Scripts

### Python

```python
import subprocess
import json

# Generate image
result = subprocess.run([
    "python", "mcp-servers/image-generation/server.py",
    "--prompt", "a beautiful sunset"
], capture_output=True)

# Parse result
image_data = json.loads(result.stdout)
```

### Shell

```bash
#!/bin/bash
python mcp-servers/kokoro-tts/server.py \
    --text "Hello world" \
    --voice "af_sarah" \
    --output speech.wav
```
