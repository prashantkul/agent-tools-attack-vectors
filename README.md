# Agent Tools Attack Vectors

Security labs for exploring attack vectors in AI agent tool systems.

---

## 📚 Available Labs

### Lab 1: The "Confused Deputy" Exfiltration CTF

**Difficulty**: Intermediate
**Topics**: Tool composition, data exfiltration, defense strategies
**Technologies**: Google ADK, Gemini 2.5 Flash, Model Context Protocol (MCP), Arize AX

A hands-on CTF lab that teaches the "Confused Deputy" vulnerability pattern, where combining seemingly harmless agent tools creates a security vulnerability that allows data exfiltration.

**What you'll learn**:
- What the Confused Deputy problem is and how it applies to AI agents
- How tool composition creates security vulnerabilities
- Data exfiltration techniques via URL parameters
- Defense strategies: embedded security, MCP policies, and monitoring
- Real-time observability with Arize AX
- Production-ready agent security practices

**[Start Lab](confused-deputy-lab/)**

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** (required for Google ADK)
- Google API Key ([Get one here](https://aistudio.google.com/app/apikey))
- (Optional) Arize AX account for observability ([Sign up](https://app.arize.com))

### Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/prashantkul/agent-tools-attack-vectors.git
cd agent-tools-attack-vectors

# 2. Navigate to a lab
cd confused-deputy-lab

# 3. Follow the lab's README for setup instructions
# Each lab has its own environment.yml and detailed setup guide
```

---

## Lab Structure

Each lab includes:

- Realistic scenario with an agent and tools
- Clear security objective (vulnerability to understand and exploit)
- Multiple progressive defense strategies
- Integration with monitoring and tracing platforms
- Complete setup guides and teaching materials
- Interactive hands-on practice

---

## 🎓 For Educators

These labs are designed for:

- University courses on AI security
- Security training workshops
- CTF competitions
- Self-paced learning
- Corporate security training

Each lab provides:
- Detailed teaching guides
- Progressive difficulty levels
- Hands-on demonstrations
- Discussion questions
- Real-world context

---

## 🔒 Security Notice

These labs contain **intentionally vulnerable code** for educational purposes.

⚠️ **DO NOT** use vulnerable implementations in production systems.

Always implement proper security controls when deploying AI agents.

---

## 🛠️ Technologies Used

- **Google ADK** - Agent Development Kit for building AI agents
- **Gemini 2.5 Flash** - Google's latest LLM for agent reasoning
- **Model Context Protocol (MCP)** - Standard protocol for agent-tool communication
- **Arize AX** - Observability platform for AI agents
- **Python 3.11+** - Programming language

---

## Contributing

Contributions are welcome. To add a new lab:

1. Fork the repository
2. Create a new lab directory (e.g., `new-lab-name/`)
3. Follow the structure of existing labs
4. Include comprehensive documentation
5. Submit a pull request

Lab requirements:
- Clear security objective
- Multiple defense strategies
- Working code with Google ADK
- Complete setup instructions
- Teaching materials

---

## 📄 License

This repository is for educational purposes. See LICENSE for details.

---

## 🔗 Resources

### Agent Security Research

- [OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Confused Deputy Problem](https://en.wikipedia.org/wiki/Confused_deputy_problem)

### Tools & Frameworks

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Arize AX Observability](https://docs.arize.com/ax)
- [Agent Security Bench](https://huggingface.co/datasets/Anthropic/agent-security-bench)

### Security Testing Tools

- [Promptfoo](https://www.promptfoo.dev/)
- [Garak LLM Scanner](https://github.com/leondz/garak)

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/prashantkul/agent-tools-attack-vectors/issues)
- **Discussions**: [GitHub Discussions](https://github.com/prashantkul/agent-tools-attack-vectors/discussions)

---

## Acknowledgments

Created for educational purposes based on real-world agent security research.
