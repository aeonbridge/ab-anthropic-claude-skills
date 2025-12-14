# Anthropic Claude Skills Collection

Collection of comprehensive Claude AI skills created using skill-seekers.

## Skills

### Agno AI Framework Skill

**Version:** 1.0.0
**Description:** Comprehensive skill for building, deploying, and managing multi-agent AI systems using the Agno framework.

**What's Included:**
- Complete documentation from https://docs.agno.com
- Code examples and best practices
- Agent creation and management guides
- Multi-agent teams and workflows
- Tools, knowledge bases, and memory integration
- Production deployment with AgentOS
- API reference and common patterns

**Usage:**
1. Use the packaged skill: `output/agno.zip`
2. Or explore the skill directory: `output/agno/`
3. Main skill file: `output/agno/SKILL.md`

**Key Features:**
- Building AI agents with various LLM providers (Anthropic, OpenAI, Google, etc.)
- Implementing RAG (Retrieval-Augmented Generation) patterns
- Creating multi-agent collaboration systems
- Deploying production-ready agent applications
- 100+ pre-built tool integrations
- Performance optimization and best practices

## How to Create Skills

This repository demonstrates how to create Claude skills using [skill-seekers](https://github.com/yusufkaraaslan/Skill_Seekers):

```bash
# Install skill-seekers
pip install skill-seekers

# Scrape documentation
skill-seekers scrape --config configs/agno_docs.json

# Package the skill
zip -r agno.zip output/agno/
```

## Configuration Files

Configuration files for skill creation are stored in `configs/`:
- `agno_unified.json` - Unified configuration for Agno (docs + GitHub)
- `agno_docs.json` - Documentation-only configuration

## Resources

- **Agno Framework**: https://github.com/agno-agi/agno
- **Agno Documentation**: https://docs.agno.com
- **Skill Seekers**: https://github.com/yusufkaraaslan/Skill_Seekers

## License

Apache-2.0
