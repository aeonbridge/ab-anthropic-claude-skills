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

### Evolution API Skill

**Version:** 1.0.0
**Description:** Comprehensive skill for Evolution API - open-source WhatsApp integration platform with multi-service chatbot and automation support.

**What's Included:**
- Complete WhatsApp integration guide using Baileys and Official API
- Instance management and connection handling
- Comprehensive messaging API (text, media, interactive messages)
- Webhook system and event handling
- Integration guides (Typebot, Chatwoot, Dify, OpenAI)
- Group management and operations
- Message queue integration (RabbitMQ, Kafka, SQS)
- Database persistence (PostgreSQL, MySQL)
- Docker deployment and production setup
- Node.js and Python webhook examples

**Usage:**
1. Use the packaged skill: `output/evolution-api.zip`
2. Or explore the skill directory: `output/evolution-api/`
3. Main skill file: `output/evolution-api/SKILL.md`

**Key Features:**
- WhatsApp Business API integration
- Send/receive text, media, location, contacts, buttons
- Interactive messages (lists, buttons)
- Typebot chatbot integration
- Chatwoot customer service integration
- OpenAI and Dify AI integration
- Real-time webhooks for all events
- Group creation and management
- Contact and profile management
- S3/MinIO media storage
- Redis caching for performance
- WebSocket support for live events
- Production-ready with high availability
- Complete REST API with authentication
- Multi-instance support

### Model Context Protocol (MCP) Skill

**Version:** 1.0.0
**Description:** Comprehensive skill for Model Context Protocol (MCP) - standardized protocol for integrating LLMs with external context, tools, and data sources.

**What's Included:**
- Complete MCP server development guide (Python FastMCP & TypeScript)
- MCP client implementation patterns
- Security and OAuth 2.1 authorization
- MCP Inspector tool for testing and debugging
- Transport options (STDIO, SSE, HTTP with SSE)
- Resource, Tool, and Prompt server patterns
- Integration with Claude Desktop and other clients
- Best practices for production deployment
- Common server implementations (filesystem, API, database)

**Usage:**
1. Use the packaged skill: `output/mcp.zip`
2. Or explore the skill directory: `output/mcp/`
3. Main skill file: `output/mcp/SKILL.md`

**Key Features:**
- Building MCP servers with FastMCP (Python) or TypeScript SDK
- Implementing resources, tools, and prompts
- OAuth 2.1 authorization and security
- JSON-RPC communication protocol
- STDIO transport for local integrations
- SSE (Server-Sent Events) for remote connections
- Structured output with Pydantic models
- Progress reporting for long-running operations
- Multi-client support and session management
- Claude Desktop integration
- MCP Inspector for development and testing
- Production deployment patterns

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
- `evolution_api_github.json` - GitHub configuration for Evolution API
- `mcp_github.json` - GitHub configuration for Model Context Protocol

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

### Evolution API
- **GitHub**: https://github.com/EvolutionAPI/evolution-api
- **Documentation**: https://doc.evolution-api.com/
- **Website**: https://evolution-api.com

### Model Context Protocol
- **Documentation**: https://modelcontextprotocol.io/
- **Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **TypeScript SDK**: https://github.com/modelcontextprotocol/typescript-sdk
- **Specification**: https://spec.modelcontextprotocol.io/

### Tools
- **Skill Seekers**: https://github.com/yusufkaraaslan/Skill_Seekers

## License

Apache-2.0
