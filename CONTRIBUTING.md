# Contributing to OpenClaw Free MCP Servers

Thank you for your interest in contributing! This project helps OpenClaw users save money on API costs by providing FREE local alternatives.

## How to Contribute

### Reporting Issues

- Use GitHub Issues to report bugs
- Include your OS, Python version, and error messages
- For MCP server issues, include OpenClaw logs

### Suggesting Features

- Open a GitHub Issue with the "enhancement" label
- Describe the use case and expected behavior
- Mention potential API cost savings

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards

- Python 3.10+ compatible
- Follow PEP 8 style guide
- Include docstrings for functions
- Add type hints where possible
- Test your changes locally

### Testing

Before submitting:

```bash
# Run tests
python tests/test-mcp-servers.py

# Check dependencies
pip install -r requirements.txt

# Test MCP servers manually
python mcp-servers/image-generation/server-simple.py
```

### Documentation

- Update README.md if adding features
- Update QUICK-START.md with new instructions
- Add examples to docs/

## Areas Needing Help

- [ ] More voice options for TTS
- [ ] Additional image generation models
- [ ] GPU optimization guides
- [ ] Windows/Mac/Linux specific guides
- [ ] Telegram integration examples
- [ ] Performance benchmarks

## Questions?

Open an issue or join the OpenClaw community!

---

Thanks for helping make AI more accessible! 🎉
