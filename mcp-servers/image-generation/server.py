#!/usr/bin/env python3
"""
MCP Server for FREE Local Image Generation
Supports: Stable Diffusion XL, SDXL Lightning, FLUX.1-schnell (GGUF)
For OpenClaw Integration - No API keys required!
"""

import asyncio
import base64
import io
import sys
from typing import Optional, Dict, Any
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent
from pathlib import Path

# Try to import torch and diffusers
try:
    import torch
    from diffusers import StableDiffusionXLPipeline, DiffusionPipeline
    from diffusers import DPMSolverMultistepScheduler, EulerAncestralDiscreteScheduler
    import requests
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    print("WARNING: PyTorch/diffusers not installed. Image generation unavailable.", file=sys.stderr)

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

app = Server("free-image-generation")

# Model configurations - all free, no API keys
MODELS = {
    "sdxl-base": {
        "repo": "stabilityai/stable-diffusion-xl-base-1.0",
        "variant": "fp16",
        "steps": 30,
        "guidance": 7.5,
        "description": "High quality 1024x1024 images (12GB VRAM)"
    },
    "sdxl-lightning": {
        "repo": "ByteDance/SDXL-Lightning",
        "variant": "fp16",
        "steps": 4,
        "guidance": 0.0,
        "description": "Ultra-fast generation in 4 steps (8GB VRAM)"
    },
    "sdxl-turbo": {
        "repo": "stabilityai/sdxl-turbo",
        "variant": "fp16",
        "steps": 1,
        "guidance": 0.0,
        "description": "Real-time generation in 1 step (8GB VRAM)"
    },
    "playground-v2.5": {
        "repo": "playgroundai/playground-v2.5-1024px-aesthetic",
        "variant": "fp16",
        "steps": 25,
        "guidance": 3.0,
        "description": "Aesthetic-focused model (10GB VRAM)"
    }
}

# Global pipeline cache
pipeline_cache: Dict[str, Any] = {}

def get_pipeline(model_key: str):
    """Get or create pipeline with caching"""
    if not HAS_TORCH:
        raise RuntimeError("PyTorch not installed. Run: pip install torch diffusers transformers")
    
    if model_key not in pipeline_cache:
        config = MODELS.get(model_key, MODELS["sdxl-lightning"])
        print(f"Loading model: {config['repo']}...", file=sys.stderr)
        
        try:
            # Try loading with minimal VRAM usage
            pipe = DiffusionPipeline.from_pretrained(
                config["repo"],
                torch_dtype=torch.float16,
                variant=config.get("variant"),
                use_safetensors=True
            )
            
            # Enable memory optimizations
            pipe.enable_model_cpu_offload()
            pipe.enable_vae_slicing()
            
            # Use faster scheduler for Lightning/Turbo
            if "lightning" in model_key or "turbo" in model_key:
                pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(
                    pipe.scheduler.config
                )
            
            pipeline_cache[model_key] = pipe
            print(f"Model {model_key} loaded successfully!", file=sys.stderr)
            
        except Exception as e:
            print(f"Error loading {model_key}: {e}", file=sys.stderr)
            raise
    
    return pipeline_cache[model_key]

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="generate_image_free",
            description="Generate images for FREE using local models (no API key needed!). "
                       "Best for: artistic images, concept art, illustrations, photorealistic scenes. "
                       "Models: SDXL Lightning (4 steps, fast), SDXL Turbo (1 step, real-time), "
                       "SDXL Base (highest quality), Playground v2.5 (aesthetic focus). "
                       "Requirements: 8-12GB VRAM for fast models, 12GB+ for base model.",
            inputSchema={
                "type": "object",
                "required": ["prompt"],
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Detailed description of the image you want to generate. Be specific!"
                    },
                    "model": {
                        "type": "string",
                        "description": "Which model to use",
                        "enum": ["sdxl-lightning", "sdxl-turbo", "sdxl-base", "playground-v2.5"],
                        "default": "sdxl-lightning"
                    },
                    "width": {
                        "type": "integer",
                        "description": "Image width (multiples of 64 recommended)",
                        "enum": [512, 768, 832, 1024, 1216, 1344],
                        "default": 1024
                    },
                    "height": {
                        "type": "integer",
                        "description": "Image height (multiples of 64 recommended)",
                        "enum": [512, 768, 832, 1024, 1216, 1344],
                        "default": 1024
                    },
                    "negative_prompt": {
                        "type": "string",
                        "description": "What to avoid in the image (optional)",
                        "default": "blurry, low quality, distorted, ugly"
                    },
                    "seed": {
                        "type": "integer",
                        "description": "Random seed for reproducibility (optional)"
                    }
                }
            }
        ),
        Tool(
            name="list_image_models",
            description="List available free local image generation models with their requirements",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list:
    if name == "list_image_models":
        model_info = []
        for key, config in MODELS.items():
            model_info.append(f"• {key}: {config['description']}")
        
        return [
            TextContent(
                type="text",
                text=f"Available FREE Local Models:\n\n" + "\n".join(model_info) + 
                     "\n\nAll models run locally - NO API keys needed!"
                     "\nRecommend 8GB+ VRAM for best experience."
            )
        ]
    
    if name == "generate_image_free":
        if not HAS_TORCH or not HAS_PIL:
            return [
                TextContent(
                    type="text",
                    text="ERROR: Required dependencies not installed.\n\n"
                         "Please install:\n"
                         "  pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121\n"
                         "  pip install diffusers transformers accelerate Pillow\n\n"
                         "Requires NVIDIA GPU with 8GB+ VRAM."
                )
            ]
        
        prompt = arguments.get("prompt")
        model_key = arguments.get("model", "sdxl-lightning")
        width = arguments.get("width", 1024)
        height = arguments.get("height", 1024)
        negative_prompt = arguments.get("negative_prompt", "blurry, low quality, distorted, ugly")
        seed = arguments.get("seed")
        
        try:
            # Get pipeline
            pipe = get_pipeline(model_key)
            config = MODELS.get(model_key, MODELS["sdxl-lightning"])
            
            # Set seed if provided
            generator = None
            if seed is not None:
                generator = torch.Generator(device="cuda" if torch.cuda.is_available() else "cpu")
                generator.manual_seed(seed)
            
            # Generate image
            print(f"Generating image with {model_key}: {prompt[:50]}...", file=sys.stderr)
            
            with torch.inference_mode():
                result = pipe(
                    prompt=prompt,
                    negative_prompt=negative_prompt if config["guidance"] > 0 else None,
                    width=width,
                    height=height,
                    num_inference_steps=config["steps"],
                    guidance_scale=config["guidance"],
                    generator=generator
                )
            
            image = result.images[0]
            
            # Convert to base64
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            return [
                TextContent(
                    type="text",
                    text=f"Generated {width}x{height} image using {model_key} in {config['steps']} steps.\n"
                         f"Model: {config['repo']}\n"
                         f"Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}\n\n"
                         f"This image was generated LOCALLY for FREE - no API costs!"
                ),
                ImageContent(
                    type="image",
                    data=img_base64,
                    mimeType="image/png"
                )
            ]
            
        except Exception as e:
            return [
                TextContent(
                    type="text",
                    text=f"Error generating image: {str(e)}\n\n"
                         f"Make sure you have:\n"
                         f"1. NVIDIA GPU with 8GB+ VRAM\n"
                         f"2. CUDA installed\n"
                         f"3. All dependencies: pip install torch diffusers transformers Pillow"
                )
            ]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    from mcp.server.stdio import stdio_server
    
    print("FREE Image Generation MCP Server starting...", file=sys.stderr)
    print(f"PyTorch available: {HAS_TORCH}", file=sys.stderr)
    print(f"PIL available: {HAS_PIL}", file=sys.stderr)
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
