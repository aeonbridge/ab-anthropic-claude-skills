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

### yt-dlp Skill

**Version:** 1.0.0
**Description:** Comprehensive skill for yt-dlp - feature-rich command-line audio/video downloader with support for thousands of sites.

**What's Included:**
- Complete yt-dlp usage guide and examples
- Installation instructions for all platforms
- Format selection and quality optimization
- Audio extraction and conversion
- Playlist and channel downloads
- Live stream recording
- Advanced features (SponsorBlock, metadata, subtitles)
- Python integration examples
- Troubleshooting and best practices

**Usage:**
1. Use the packaged skill: `output/yt-dlp.zip`
2. Or explore the skill directory: `output/yt-dlp/`
3. Main skill file: `output/yt-dlp/SKILL.md`

**Key Features:**
- Downloading videos from YouTube, Vimeo, TikTok, and thousands of other sites
- Audio extraction as MP3, M4A, OPUS, and other formats
- Playlist and channel batch downloads
- Format selection and quality control
- Subtitle and metadata embedding
- Live stream recording
- FFmpeg integration for post-processing
- Browser cookie support for authenticated content
- SponsorBlock integration
- Configuration file support for automation

### Graphiti & Zep Knowledge Graph Skill

**Version:** 1.0.0
**Description:** Comprehensive skill for Graphiti and Zep - temporal knowledge graph framework for AI agents with dynamic context engineering.

**What's Included:**
- Complete Graphiti framework guide
- Zep platform integration
- Temporal knowledge graph concepts
- Entity and relationship management
- Hybrid search implementation (semantic + BM25 + graph traversal)
- Multi-database support (Neo4j, FalkorDB, Kuzu, Neptune)
- LLM integration examples
- Agent framework integration (LangGraph, CrewAI, Autogen)
- Python, TypeScript, and Go SDK examples
- Production deployment and best practices

**Usage:**
1. Use the packaged skill: `output/graphiti.zip`
2. Or explore the skill directory: `output/graphiti/`
3. Main skill file: `output/graphiti/SKILL.md`

**Key Features:**
- Building temporal knowledge graphs for AI agents
- Persistent agent memory across conversations
- Bi-temporal data model (event time + ingestion time)
- Point-in-time historical queries
- Custom entity types and ontologies
- Hybrid search combining multiple methods
- Sub-second query latency
- Integration with major agent frameworks
- Enterprise features (RBAC, BYOK, audit logging)
- Multi-user context management
- Graph RAG for personalized AI applications

### Microsoft GraphRAG Skill

**Version:** 1.0.0
**Description:** Comprehensive skill for Microsoft GraphRAG - modular graph-based RAG system for reasoning over private datasets.

**What's Included:**
- Complete GraphRAG pipeline guide
- Knowledge graph extraction from unstructured text
- Hierarchical community detection (Leiden algorithm)
- Multiple query modes (Global, Local, DRIFT)
- Indexing pipeline configuration
- Prompt tuning for domain-specific datasets
- LLM integration (OpenAI, Azure OpenAI, Ollama)
- Python API and CLI usage
- Cost management and optimization
- Production deployment best practices

**Usage:**
1. Use the packaged skill: `output/graphrag.zip`
2. Or explore the skill directory: `output/graphrag/`
3. Main skill file: `output/graphrag/SKILL.md`

**Key Features:**
- Extract entities, relationships, and claims from text
- Build knowledge graphs automatically from documents
- Hierarchical community detection for multi-level summarization
- Global search for holistic corpus understanding
- Local search for entity-specific queries
- DRIFT search combining entity and community context
- Domain-specific prompt tuning
- Support for multiple LLM providers
- Cost estimation and optimization tools
- Integration with LangChain, FastAPI, Streamlit
- Better than baseline RAG for complex reasoning tasks

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
- `ytdlp_github.json` - GitHub configuration for yt-dlp
- `graphiti_github.json` - GitHub configuration for Graphiti
- `graphrag_github.json` - GitHub configuration for Microsoft GraphRAG

## Resources

### Agno
- **GitHub**: https://github.com/agno-agi/agno
- **Documentation**: https://docs.agno.com
- **Community**: https://community.agno.com

### yt-dlp
- **GitHub**: https://github.com/yt-dlp/yt-dlp
- **Supported Sites**: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

### Graphiti & Zep
- **Graphiti GitHub**: https://github.com/getzep/graphiti
- **Zep Documentation**: https://help.getzep.com/
- **Zep Concepts**: https://help.getzep.com/concepts

### Microsoft GraphRAG
- **GitHub**: https://github.com/microsoft/graphrag
- **Documentation**: https://microsoft.github.io/graphrag/
- **Research Paper**: https://arxiv.org/abs/2404.16130

### Tools
- **Skill Seekers**: https://github.com/yusufkaraaslan/Skill_Seekers

## License

Apache-2.0
