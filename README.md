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

### Dify Skill

**Version:** 1.0.0
**Description:** Comprehensive skill for Dify - open-source platform for building agentic workflows and LLM applications with visual interface.

**What's Included:**
- Complete visual workflow builder guide
- RAG (Retrieval-Augmented Generation) pipeline setup
- Agent development with 50+ built-in tools
- Knowledge base management and document processing
- LLMOps monitoring and analytics
- REST API integration (Python, Node.js)
- Deployment guides (Docker, Kubernetes, Cloud platforms)
- Production best practices and troubleshooting

**Usage:**
1. Use the packaged skill: `output/dify.zip`
2. Or explore the skill directory: `output/dify/`
3. Main skill file: `output/dify/SKILL.md`

**Key Features:**
- Visual workflow engine with drag-and-drop interface
- Support for hundreds of LLMs from dozens of providers
- Prompt IDE for model comparison
- RAG pipeline with PDF, PPT, and document support
- ReAct-based agents with custom tool integration
- Application monitoring and performance analytics
- Backend-as-a-Service with REST APIs
- Deploy as web apps, APIs, or embedded components
- Multiple deployment options (Cloud, Docker, Kubernetes)
- Knowledge base chunking strategies and retrieval optimization

### Langextract Skill

**Version:** 1.0.0
**Description:** Comprehensive skill for Langextract - Google's language detection and extraction library.

**What's Included:**
- Complete documentation and examples
- API reference and best practices
- Integration guides
- Troubleshooting tips

**Usage:**
1. Use the packaged skill: `output/langextract.zip`
2. Or explore the skill directory: `output/langextract/`
3. Main skill file: `output/langextract/SKILL.md`

**Key Features:**
- Language detection
- Text extraction
- Multi-language support

### Ticketmaster API Skill

**Version:** 1.0.0
**Description:** Comprehensive skill for Ticketmaster Discovery API - event search and ticket discovery platform.

**What's Included:**
- Complete Ticketmaster Discovery API documentation
- Authentication and API key management
- Event search, details, images, and suggestions endpoints
- Attraction and venue search capabilities
- Classification and genre queries
- Rate limiting and quota management (5 requests/second, 5000/day)
- Python and JavaScript integration examples
- React and Node.js use cases
- Troubleshooting and best practices

**Usage:**
1. Use the packaged skill: `output/ticketmaster.zip`
2. Or explore the skill directory: `output/ticketmaster/`
3. Main skill file: `output/ticketmaster/SKILL.md`

**Key Features:**
- Search 230K+ events across US, Canada, Mexico, Australia, UK, Ireland, and Europe
- Find events by keyword, location, category, date range
- Get event details, images, venues, and attractions
- Advanced filtering (price range, genre, segment)
- Location-based search with radius
- Pagination and sorting options
- HAL format responses with embedded resources
- Rate limit monitoring and management
- Complete error handling patterns

## How to Create Skills

### Automated Skill Generation (Recommended)

This repository includes automated scripts for creating comprehensive Claude skills:

```bash
# Quick start: Create a skill from URLs
./create_skill.py <skill_name> <url1> [url2] [url3] ...

# Example: Create FastAPI skill
./create_skill.py fastapi \
  https://fastapi.tiangolo.com \
  https://github.com/tiangolo/fastapi

# Example: Create Redis skill
./create_skill.py redis \
  https://redis.io/docs \
  https://github.com/redis/redis-py

# Get enhancement guidance
./enhance_skill.py <skill_name>
```

**What the script does:**
- Creates configuration file automatically
- Generates comprehensive SKILL.md template
- Creates proper directory structure
- Packages as .zip file
- Updates README.md
- Commits and pushes to git

**Documentation:**
- 📖 [Complete Scripts Guide](SCRIPTS_GUIDE.md) - Detailed usage and options
- 📚 [Examples](EXAMPLES.md) - 50+ examples for popular technologies
- 🛠️ Scripts: `create_skill.py`, `enhance_skill.py`

### Manual Skill Creation

You can also create skills manually using [skill-seekers](https://github.com/yusufkaraaslan/Skill_Seekers):

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
- `dify_github.json` - GitHub configuration for Dify
- `langextract_github.json` - GitHub configuration for Langextract
- `ticketmaster_github.json` - GitHub configuration for Ticketmaster

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

### Dify
- **GitHub**: https://github.com/langgenius/dify
- **Documentation**: https://docs.dify.ai/
- **Cloud Platform**: https://cloud.dify.ai
- **Discord**: https://discord.gg/dify

### Langextract
- **GitHub**: https://github.com/google/langextract
- **Examples**: https://github.com/google/langextract/tree/main/examples
- **Documentation**: https://github.com/google/langextract/tree/main/docs/examples

### Ticketmaster
- **Getting Started**: https://developer.ticketmaster.com/products-and-docs/apis/getting-started/
- **Discovery API**: https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/
- **Search Events**: https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/#search-events-v2
- **Event Images**: https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/#event-images-v2
- **Classifications**: https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/#anchor_getGenre

### Tools
- **Skill Seekers**: https://github.com/yusufkaraaslan/Skill_Seekers

## License

Apache-2.0
