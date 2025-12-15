# Claude Skills Integration Examples

This directory contains practical examples demonstrating **real-world integration** of multiple Claude Skills to build production-ready applications.

## 🎯 Philosophy

These examples show how to:
- **Combine multiple skills** into cohesive applications
- **Integrate different technologies** seamlessly
- **Build production-ready** systems with proper architecture
- **Follow best practices** for microservices and APIs
- **Document thoroughly** for learning and maintenance

## 📚 Available Examples

### 1. WhatsApp Knowledge Bot with Temporal Memory

**Status**: ✅ Complete
**Directory**: `whatsapp-knowledge-bot/`
**Skills Used**: 3

Intelligent WhatsApp bot combining:
- **Evolution API** - WhatsApp message handling
- **Dify** - LLM processing with RAG
- **Graphiti** - Temporal knowledge graph memory

**Features**:
- Context-aware conversations
- Bi-temporal memory storage
- Knowledge base integration
- Multi-user support
- Production-ready Docker setup

**Complexity**: Intermediate
**Time to Deploy**: ~5 minutes
**Use Cases**:
- Customer support automation
- Knowledge base Q&A
- Conversational AI assistants
- Multi-channel chatbots

[**View Full Documentation →**](whatsapp-knowledge-bot/README.md)
[**Quick Start Guide →**](whatsapp-knowledge-bot/QUICKSTART.md)

---

## 🚀 Coming Soon

### 2. AI-Powered Video Content Pipeline

**Skills**: yt-dlp + Dify + MCP
**Status**: Planned

Download YouTube videos, extract transcriptions, generate summaries with Dify, serve via MCP.

### 3. Multi-Agent Research Assistant

**Skills**: Agno + GraphRAG + Dify
**Status**: Planned

Create multi-agent research system with graph-based knowledge retrieval and visual workflows.

### 4. Document Processing Workflow

**Skills**: Dify + Graphiti + MCP
**Status**: Planned

Upload documents, build knowledge graph, query via MCP, visualize relationships.

---

## 📖 How to Use These Examples

### 1. Choose an Example

Browse examples above and select one that matches your needs.

### 2. Review Prerequisites

Each example lists:
- Required skills
- System requirements
- API keys needed
- Technical knowledge level

### 3. Follow Quick Start

Most examples include:
- `README.md` - Complete documentation
- `QUICKSTART.md` - 5-minute setup guide
- `docker-compose.yml` - One-command deployment

### 4. Customize

Examples are designed to be:
- **Modular**: Replace components easily
- **Extensible**: Add new features
- **Educational**: Well-commented code
- **Production-ready**: Best practices applied

## 🎓 Learning Path

### Beginner: Single Skill

Start with individual skills:
```bash
cd ../output/dify
cat SKILL.md  # Read skill documentation
```

### Intermediate: Two Skills

Try simple integrations:
- Dify + Evolution API
- Graphiti + MCP
- Agno + Dify

### Advanced: Multi-Skill

Build complete applications:
- WhatsApp Knowledge Bot (3 skills)
- Research Assistant (3 skills)
- Content Pipeline (3 skills)

## 🏗️ Architecture Patterns

### Pattern 1: Webhook Chain

```
User → Service A (webhook) → Service B (API) → Service C (storage)
```

Example: WhatsApp Bot
- Evolution API (webhook) → Bot (API) → Graphiti (storage)

### Pattern 2: RAG Pipeline

```
Query → Context Retrieval → LLM Processing → Response
```

Example: Knowledge Bot
- User message → Graphiti → Dify RAG → Response

### Pattern 3: Multi-Agent Orchestration

```
Task → Agent Team → Tools → Results → Synthesis
```

Example: Research Assistant
- Research task → Agno agents → GraphRAG → Report

### Pattern 4: Event-Driven

```
Event → Queue → Processor → Action
```

Example: Document Processing
- Upload → RabbitMQ → Dify → Knowledge Graph

## 🛠️ Common Patterns

### Docker Compose

All examples use Docker Compose:
```yaml
services:
  service-a:  # Skill 1
  service-b:  # Skill 2
  service-c:  # Skill 3
  integration:  # Your code
```

### Environment Configuration

```bash
cp .env.example .env
# Edit .env with your keys
docker-compose up -d
```

### Health Checks

```bash
curl http://localhost:8000/health
```

### Monitoring

```bash
docker-compose logs -f [service]
```

## 📊 Example Comparison

| Example | Skills | Complexity | Deploy Time | Use Cases |
|---------|--------|------------|-------------|-----------|
| WhatsApp Bot | 3 | ⭐⭐⭐ | 5 min | Support, Q&A |
| Video Pipeline | 3 | ⭐⭐ | 10 min | Content, Analysis |
| Research Agent | 3 | ⭐⭐⭐⭐ | 15 min | Research, Reports |
| Doc Processing | 3 | ⭐⭐⭐ | 10 min | Knowledge, Graph |

## 🔍 Example Structure

Each example follows this structure:

```
example-name/
├── README.md              # Complete documentation
├── QUICKSTART.md          # 5-minute guide
├── docker-compose.yml     # All services
├── Dockerfile             # Custom service build
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
├── src/                   # Source code
│   └── main.py           # Integration logic
├── config/                # Configuration files
└── docs/                  # Additional documentation
    └── ARCHITECTURE.md    # Architecture details
```

## 🎯 Best Practices

### 1. Start Simple

Begin with a single skill, then add complexity.

### 2. Use Docker

Containerize all services for consistency.

### 3. Environment Variables

Never commit API keys. Use `.env` files.

### 4. Error Handling

Implement retries, fallbacks, and logging.

### 5. Documentation

Document architecture, setup, and troubleshooting.

### 6. Testing

Test each integration point independently.

### 7. Monitoring

Add health checks and observability.

## 🤝 Contributing Examples

Want to add an example? Follow this template:

1. **Create directory**: `examples/your-example/`
2. **Use ≥2 skills**: Demonstrate skill integration
3. **Add Docker Compose**: One-command deployment
4. **Write docs**: README + QUICKSTART
5. **Test thoroughly**: Ensure it works
6. **Submit PR**: Include screenshots/demo

### Example Template

```bash
# Copy template
cp -r examples/template examples/your-example

# Customize
# - Update docker-compose.yml
# - Write src/main.py
# - Document in README.md
# - Add QUICKSTART.md

# Test
cd examples/your-example
docker-compose up -d
# Verify it works

# Submit
git add examples/your-example
git commit -m "Add [Your Example] integration"
```

## 📚 Resources

### Skills Documentation

All skills used in examples:
```bash
ls -la ../output/*/SKILL.md
```

Individual skill docs:
- Agno: `../output/agno/SKILL.md`
- Dify: `../output/dify/SKILL.md`
- Evolution API: `../output/evolution-api/SKILL.md`
- Graphiti: `../output/graphiti/SKILL.md`
- GraphRAG: `../output/graphrag/SKILL.md`
- MCP: `../output/mcp/SKILL.md`
- yt-dlp: `../output/yt-dlp/SKILL.md`

### External Resources

- Claude Skills Documentation: https://code.claude.com/docs/en/skills
- Docker Compose Guide: https://docs.docker.com/compose/
- FastAPI Documentation: https://fastapi.tiangolo.com
- Microservices Patterns: https://microservices.io/patterns/

## 🐛 Troubleshooting

### Docker Issues

```bash
# Reset everything
docker-compose down -v
docker system prune -a

# Restart
docker-compose up -d
```

### Port Conflicts

```bash
# Check ports in use
lsof -i :8000
lsof -i :3000

# Change port in docker-compose.yml
```

### Memory Issues

```bash
# Increase Docker memory
# Docker Desktop → Settings → Resources → Memory → 8GB
```

### Network Issues

```bash
# Check network
docker network ls
docker network inspect example_network
```

## 💡 Tips

1. **Read QUICKSTART first** - Fastest way to get running
2. **Check logs often** - `docker-compose logs -f`
3. **Start services separately** - Debug one at a time
4. **Use health checks** - Verify each service works
5. **Test integrations** - Curl each endpoint
6. **Monitor resources** - `docker stats`
7. **Backup data** - Before major changes

## 🎓 Learning Outcomes

By working through these examples, you'll learn:

- ✅ Multi-skill integration patterns
- ✅ Microservices architecture
- ✅ Docker Compose orchestration
- ✅ API integration techniques
- ✅ Webhook handling
- ✅ Async processing
- ✅ Error handling & retries
- ✅ Logging & monitoring
- ✅ Production deployment
- ✅ Documentation best practices

---

**Built with Claude Skills** - Demonstrating practical skill composition for real-world applications.

For questions or contributions, see the main repository README.
