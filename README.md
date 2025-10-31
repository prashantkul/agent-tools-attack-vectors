# Agent Tools Attack Vectors

Security labs for exploring attack vectors in AI agent tool systems.

## 📚 Available Labs

### Lab 1: The "Confused Deputy" Exfiltration CTF

**Difficulty**: Intermediate
**Topics**: Tool composition, data exfiltration, defense strategies

A hands-on CTF that teaches the "Confused Deputy" vulnerability pattern, where combining seemingly harmless agent tools creates an attack surface for data exfiltration.

**What you'll learn**:
- How tool composition creates security vulnerabilities
- Data exfiltration techniques via URL parameters
- Defense strategies: allowlists, MCP policies, and monitoring
- Production-ready agent security practices

**Technologies**:
- Google ADK (Agent Development Kit)
- Gemini 2.0 Flash
- Model Context Protocol (MCP)
- Streamlit (for security dashboards)

[**Start Lab →**](confused-deputy-lab/README.md)

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Google API Key ([Get one here](https://ai.google.dev/))

### Getting Started

```bash
# 1. Navigate to a lab
cd confused-deputy-lab

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
export GOOGLE_API_KEY='your-api-key'

# 4. Test your setup
python test_setup.py

# 5. Start the lab
python agent/interactive_agent.py
```

## 📖 Lab Structure

Each lab includes:

- **📂 Scenario**: A realistic agent with tools
- **🎯 Objective**: A specific security vulnerability to exploit
- **🛡️ Defenses**: Multiple defense strategies with implementations
- **📊 Monitoring**: Security dashboards and logging
- **📝 Documentation**: Complete setup and teaching guides

## 🎓 For Educators

These labs are designed for:

- University courses on AI security
- Security training workshops
- CTF competitions
- Self-paced learning

Each lab includes:
- Detailed teaching guides
- Progressive difficulty levels
- Hands-on demonstrations
- Discussion questions
- Assessment criteria

## 🔒 Security Notice

These labs contain **intentionally vulnerable code** for educational purposes.

⚠️ **DO NOT** use vulnerable implementations in production systems.

Always implement proper security controls when deploying AI agents.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add your lab or improvement
4. Submit a pull request

See individual lab READMEs for specific contribution guidelines.

## 📄 License

This repository is for educational purposes. See LICENSE for details.

## 🔗 Resources

### Agent Security

- [OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Google ADK Documentation](https://github.com/google/adk-python)

### Security Tools

- [Agent Security Bench](https://huggingface.co/datasets/Anthropic/agent-security-bench)
- [Promptfoo](https://www.promptfoo.dev/)
- [Garak LLM Scanner](https://github.com/leondz/garak)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/prashantkul/agent-tools-attack-vectors/issues)
- **Discussions**: [GitHub Discussions](https://github.com/prashantkul/agent-tools-attack-vectors/discussions)

## 🙏 Acknowledgments

Created for educational purposes based on real-world agent security research.

Special thanks to the AI security community for their ongoing research and tools.

---

**Ready to learn about agent security?** [Start with the Confused Deputy Lab →](confused-deputy-lab/README.md)
