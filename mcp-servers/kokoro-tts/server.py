#!/usr/bin/env python3
"""
MCP Server for Kokoro TTS (Text-to-Speech)
Ultra-lightweight 82M parameter TTS model - runs on CPU!
For OpenClaw Integration - No API keys required!
"""

import asyncio
import base64
import io
import sys
import os
from pathlib import Path
from typing import Optional
from mcp.server import Server
from mcp.types import Tool, TextContent

# Try to import Kokoro
try:
    from kokoro import KPipeline
    import torch
    import soundfile as sf
    HAS_KOKORO = True
except ImportError:
    HAS_KOKORO = False
    print("WARNING: Kokoro not installed. TTS unavailable.", file=sys.stderr)

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

app = Server("kokoro-tts")

# Available voices by language
VOICES = {
    "american": {
        "af_heart": "American Female - Heart (warm, clear)",
        "af_bella": "American Female - Bella (soft, gentle)",
        "af_nicole": "American Female - Nicole (professional)",
        "af_sarah": "American Female - Sarah (neutral)",
        "am_adam": "American Male - Adam (deep, authoritative)",
        "am_michael": "American Male - Michael (friendly)"
    },
    "british": {
        "bf_emma": "British Female - Emma (soft, warm)",
        "bf_isabella": "British Female - Isabella (clear)",
        "bm_george": "British Male - George (professional)",
        "bm_lewis": "British Male - Lewis (friendly)"
    }
}

# Language codes for Kokoro
LANG_CODES = {
    "american": "a",  # American English
    "british": "b",  # British English
    "spanish": "e",  # Spanish
    "french": "f",   # French
    "hindi": "h",    # Hindi
    "italian": "i",  # Italian
    "japanese": "j",  # Japanese
    "portuguese": "p",  # Brazilian Portuguese
    "chinese": "z"   # Mandarin Chinese
}

# Pipeline cache
pipeline_cache = {}

def get_pipeline(lang_code: str = "a"):
    """Get or create Kokoro pipeline"""
    if not HAS_KOKORO:
        raise RuntimeError("Kokoro not installed. Run: pip install kokoro soundfile")
    
    if lang_code not in pipeline_cache:
        print(f"Loading Kokoro pipeline for language: {lang_code}...", file=sys.stderr)
        try:
            pipeline = KPipeline(lang_code=lang_code)
            pipeline_cache[lang_code] = pipeline
            print(f"Pipeline loaded for {lang_code}!", file=sys.stderr)
        except Exception as e:
            print(f"Error loading pipeline: {e}", file=sys.stderr)
            raise
    
    return pipeline_cache[lang_code]

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="text_to_speech",
            description="Convert text to speech using Kokoro TTS (FREE, no API key!). "
                       "Ultra-fast 82M parameter model. Runs on CPU or GPU. "
                       "Best for: voice messages, audio content, accessibility. "
                       "Supports: American/British English, Spanish, French, Hindi, Italian, "
                       "Japanese, Portuguese, Chinese. Multiple voice options available.",
            inputSchema={
                "type": "object",
                "required": ["text"],
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to convert to speech. Supports long texts - will auto-split."
                    },
                    "voice": {
                        "type": "string",
                        "description": "Voice to use",
                        "enum": [
                            "af_heart", "af_bella", "af_nicole", "af_sarah",
                            "am_adam", "am_michael",
                            "bf_emma", "bf_isabella", "bm_george", "bm_lewis"
                        ],
                        "default": "af_heart"
                    },
                    "language": {
                        "type": "string",
                        "description": "Language/accent",
                        "enum": ["american", "british", "spanish", "french", "hindi", "italian", "japanese", "portuguese", "chinese"],
                        "default": "american"
                    },
                    "speed": {
                        "type": "number",
                        "description": "Speech speed multiplier (0.5 = slow, 1.0 = normal, 1.5 = fast)",
                        "minimum": 0.5,
                        "maximum": 2.0,
                        "default": 1.0
                    },
                    "format": {
                        "type": "string",
                        "description": "Audio output format",
                        "enum": ["wav", "mp3", "ogg"],
                        "default": "wav"
                    }
                }
            }
        ),
        Tool(
            name="list_voices",
            description="List all available TTS voices with descriptions",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="speak_telegram_voice",
            description="Generate voice message optimized for Telegram (OGG format, ~24kHz)",
            inputSchema={
                "type": "object",
                "required": ["text"],
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to convert to voice message (keep under 60 seconds for Telegram)"
                    },
                    "voice": {
                        "type": "string",
                        "description": "Voice to use",
                        "enum": ["af_heart", "af_bella", "am_adam", "am_michael", "bf_emma", "bm_george"],
                        "default": "af_heart"
                    }
                }
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list:
    if name == "list_voices":
        voice_list = []
        for accent, voices in VOICES.items():
            voice_list.append(f"\n{accent.upper()}:")
            for voice_id, desc in voices.items():
                voice_list.append(f"  • {voice_id}: {desc}")
        
        return [
            TextContent(
                type="text",
                text=f"Available Kokoro TTS Voices:\n{''.join(voice_list)}\n\n"
                     f"All voices are FREE - no API costs!\n"
                     f"Model: Kokoro-82M (Apache 2.0 license)\n"
                     f"Quality: Comparable to larger models like ElevenLabs"
            )
        ]
    
    if name == "text_to_speech":
        if not HAS_KOKORO:
            return [
                TextContent(
                    type="text",
                    text="ERROR: Kokoro not installed.\n\n"
                         "Please install:\n"
                         "  pip install kokoro soundfile\n\n"
                         "For non-English languages, also install:\n"
                         "  pip install misaki[ja]  # For Japanese\n"
                         "  pip install misaki[zh]  # For Chinese\n\n"
                         "Optional (for Windows):\n"
                         "  Download espeak-ng from: https://github.com/espeak-ng/espeak-ng/releases"
                )
            ]
        
        text = arguments.get("text", "")
        voice = arguments.get("voice", "af_heart")
        language = arguments.get("language", "american")
        speed = arguments.get("speed", 1.0)
        format_type = arguments.get("format", "wav")
        
        if not text:
            return [TextContent(type="text", text="Error: No text provided")]
        
        try:
            # Get language code
            lang_code = LANG_CODES.get(language, "a")
            
            # Get pipeline
            pipeline = get_pipeline(lang_code)
            
            print(f"Generating speech: {text[:50]}...", file=sys.stderr)
            
            # Generate audio
            generator = pipeline(text, voice=voice, speed=speed)
            
            # Collect all audio segments
            audio_segments = []
            for i, (gs, ps, audio) in enumerate(generator):
                audio_segments.append(audio)
            
            # Concatenate all segments
            if len(audio_segments) > 1:
                full_audio = np.concatenate(audio_segments)
            else:
                full_audio = audio_segments[0]
            
            # Convert to bytes
            buffer = io.BytesIO()
            sf.write(buffer, full_audio, 24000, format="WAV")
            buffer.seek(0)
            audio_bytes = buffer.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            
            # Calculate duration
            duration = len(full_audio) / 24000
            
            return [
                TextContent(
                    type="text",
                    text=f"Generated speech audio:\n"
                         f"• Duration: {duration:.1f} seconds\n"
                         f"• Voice: {voice}\n"
                         f"• Speed: {speed}x\n"
                         f"• Language: {language}\n"
                         f"• Text: {text[:100]}{'...' if len(text) > 100 else ''}\n\n"
                         f"Audio data (base64 encoded WAV, 24kHz):\n{audio_base64[:100]}..."
                )
            ]
            
        except Exception as e:
            return [
                TextContent(
                    type="text",
                    text=f"Error generating speech: {str(e)}\n\n"
                         f"Make sure you have:\n"
                         f"1. Kokoro installed: pip install kokoro soundfile\n"
                         f"2. For Windows: espeak-ng installed\n"
                         f"3. Sufficient memory (model is small but needs ~500MB)"
                )
            ]
    
    if name == "speak_telegram_voice":
        if not HAS_KOKORO:
            return [
                TextContent(
                    type="text",
                    text="ERROR: Kokoro not installed. Run: pip install kokoro soundfile"
                )
            ]
        
        text = arguments.get("text", "")
        voice = arguments.get("voice", "af_heart")
        
        if not text:
            return [TextContent(type="text", text="Error: No text provided")]
        
        # Estimate duration (approx 13 chars per second at normal speed)
        estimated_duration = len(text) / 13
        if estimated_duration > 60:
            return [
                TextContent(
                    type="text",
                    text=f"Text too long for Telegram voice message ({estimated_duration:.0f}s estimated).\n"
                         f"Please keep under 60 seconds. Current text: {len(text)} characters"
                )
            ]
        
        try:
            pipeline = get_pipeline("a")  # Always use American English for Telegram
            
            print(f"Generating Telegram voice: {text[:50]}...", file=sys.stderr)
            
            # Generate with standard speed for clarity
            generator = pipeline(text, voice=voice, speed=1.0)
            
            audio_segments = []
            for i, (gs, ps, audio) in enumerate(generator):
                audio_segments.append(audio)
            
            if len(audio_segments) > 1:
                full_audio = np.concatenate(audio_segments)
            else:
                full_audio = audio_segments[0]
            
            # Convert to OGG for Telegram (best compatibility)
            buffer = io.BytesIO()
            sf.write(buffer, full_audio, 24000, format="OGG")
            buffer.seek(0)
            audio_bytes = buffer.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            
            duration = len(full_audio) / 24000
            
            return [
                TextContent(
                    type="text",
                    text=f"Telegram voice message ready!\n"
                         f"• Duration: {duration:.1f}s\n"
                         f"• Format: OGG (Telegram optimized)\n"
                         f"• Sample rate: 24kHz\n"
                         f"• Voice: {voice}\n\n"
                         f"Base64 audio (save and send to Telegram):\n{audio_base64}"
                )
            ]
            
        except Exception as e:
            return [
                TextContent(
                    type="text",
                    text=f"Error generating voice: {str(e)}"
                )
            ]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    from mcp.server.stdio import stdio_server
    
    print("Kokoro TTS MCP Server starting...", file=sys.stderr)
    print(f"Kokoro available: {HAS_KOKORO}", file=sys.stderr)
    print(f"NumPy available: {HAS_NUMPY}", file=sys.stderr)
    
    if HAS_KOKORO:
        print("Ready to generate speech! Try voices like 'af_heart', 'am_adam', etc.", file=sys.stderr)
    else:
        print("WARNING: Install kokoro with: pip install kokoro soundfile", file=sys.stderr)
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
