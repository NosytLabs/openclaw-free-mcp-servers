#!/usr/bin/env python3
"""
Test script for OpenClaw MCP servers
"""

import subprocess
import sys
import json

def test_server(name, path):
    """Test if an MCP server can start"""
    print(f"\n{'='*50}")
    print(f"Testing: {name}")
    print(f"{'='*50}")
    
    try:
        # Try to start the server and get its tool list
        result = subprocess.run(
            [sys.executable, path],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if "Error" in result.stderr or "Traceback" in result.stderr:
            print(f"[FAIL] FAILED")
            print(f"Error: {result.stderr[:200]}")
            return False
        else:
            print(f"[PASS] Server starts correctly")
            return True
            
    except subprocess.TimeoutExpired:
        print(f"[PASS] Server starts (timeout expected for MCP servers)")
        return True
    except Exception as e:
        print(f"[FAIL] FAILED: {e}")
        return False

def main():
    print("OpenClaw MCP Server Test Suite")
    print("=" * 50)
    
    servers = [
        ("Image Generation (Simple)", "mcp-servers/image-generation/server-simple.py"),
        ("Image Generation (Full)", "mcp-servers/image-generation/server.py"),
        ("Kokoro TTS", "mcp-servers/kokoro-tts/server.py"),
    ]
    
    results = {}
    for name, path in servers:
        success = test_server(name, f"C:/Users/Tyson/.openclaw/{path}")
        results[name] = success
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    for name, success in results.items():
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} servers working")
    
    # Check dependencies
    print("\n" + "=" * 50)
    print("DEPENDENCY CHECK")
    print("=" * 50)
    
    deps = [
        ("torch", "PyTorch"),
        ("diffusers", "Diffusers"),
        ("transformers", "Transformers"),
        ("kokoro", "Kokoro TTS"),
        ("soundfile", "SoundFile"),
        ("mcp", "MCP SDK"),
        ("PIL", "Pillow (PIL)"),
    ]
    
    installed = 0
    for module, name in deps:
        try:
            __import__(module)
            print(f"[OK] {name}: INSTALLED")
            installed += 1
        except ImportError:
            print(f"[MISSING] {name}: NOT INSTALLED")
    
    print(f"\nDependencies: {installed}/{len(deps)} installed")
    
    if installed < len(deps):
        print("\n[!] Run install-all-deps.bat to install missing dependencies")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
