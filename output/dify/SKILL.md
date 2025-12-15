# Dify Skill

## When to Use This Skill

Use this skill when you need to work with Dify, including:
- Building LLM-powered applications with visual workflows
- Creating AI chatbots and conversational agents
- Implementing RAG (Retrieval-Augmented Generation) systems
- Developing AI agents with tool calling capabilities
- Deploying production-ready LLM applications
- Managing knowledge bases and document processing
- Integrating LLMs with existing tools and data sources
- Monitoring and optimizing LLM application performance

## Overview

**Dify** (Do It For You) is an open-source platform for building agentic workflows and LLM applications. It provides a visual interface for designing complex AI processes without extensive coding, supporting integration with hundreds of LLM models and existing tools.

**Key Resources:**
- https://github.com/langgenius/dify
- https://docs.dify.ai/
- https://cloud.dify.ai (Cloud version with 200 free GPT-4 calls)
- Discord: https://discord.gg/dify

**Platform Name**: **D**o **I**t **F**or **Y**ou - reflecting its purpose of simplifying LLM application development.

## Core Capabilities

### 1. Visual Workflow Engine
- Node-based interface for building AI workflows
- Drag-and-drop components for rapid development
- Real-time preview and testing
- Version control for workflow iterations

### 2. Model Support
- **Hundreds of LLMs**: Integration with proprietary and open-source models
- **Dozens of providers**: OpenAI, Anthropic, Google, Hugging Face, local models, etc.
- **Model comparison**: Side-by-side testing in Prompt IDE
- **Flexible switching**: Easy model provider changes

### 3. RAG Pipeline
- **Document processing**: PDF, PPT, TXT, Markdown support
- **Knowledge bases**: Create and manage multiple knowledge sources
- **Chunking strategies**: Configurable text segmentation
- **Retrieval methods**: Vector search, keyword search, hybrid retrieval
- **Embedding models**: Multiple embedding provider support

### 4. Agent Capabilities
- **Function calling**: ReAct-based agent architecture
- **50+ built-in tools**: Pre-configured integrations
- **Custom tools**: Add your own API and function tools
- **Multi-step reasoning**: Complex task decomposition

### 5. LLMOps
- **Application monitoring**: Track usage and performance
- **Analytics dashboard**: User interactions and metrics
- **Debugging tools**: Step-by-step execution inspection
- **Variable tracking**: Monitor data flow through workflows

### 6. Backend-as-a-Service
- **REST APIs**: Programmatic access to applications
- **Web applications**: Deploy as standalone web apps
- **Embedded components**: Integrate into existing applications
- **API documentation**: Auto-generated API specs

## Installation

### Prerequisites

**System Requirements:**
- CPU: ≥2 cores
- RAM: ≥4 GB
- Docker and Docker Compose installed

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/langgenius/dify.git
cd dify

# Navigate to docker directory
cd docker

# Copy environment example
cp .env.example .env

# Edit .env with your configuration
vim .env

# Start Dify
docker compose up -d

# Access the dashboard
open http://localhost/install
```

### Option 2: Dify Cloud

```bash
# Sign up at https://cloud.dify.ai
# Get 200 free GPT-4 calls
# No installation required
```

### Option 3: Deploy to Cloud Platforms

**Kubernetes:**
```bash
helm repo add dify https://langgenius.github.io/dify-helm
helm install dify dify/dify
```

**AWS:**
```bash
# Using AWS CDK
cdk deploy DifyStack
```

**Azure/Google Cloud/Alibaba Cloud:**
See deployment guides in official documentation.

### Environment Configuration

Key environment variables in `.env`:

```bash
# API Service
API_URL=http://localhost:5001

# Web Service
WEB_URL=http://localhost:3000

# Database
DB_USERNAME=postgres
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432
DB_DATABASE=dify

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password

# Storage (S3, Azure Blob, or local)
STORAGE_TYPE=local
STORAGE_LOCAL_PATH=storage

# Vector Database
VECTOR_STORE=weaviate  # or pgvector, qdrant, milvus

# API Keys for LLM Providers
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

## Quick Start

### 1. Create Your First Application

```bash
# After installation, access http://localhost/install
# Complete initial setup wizard
# Create your first workspace
```

**Application Types:**
1. **Chatbot** - Conversational AI with memory
2. **Text Generator** - Single-turn text generation
3. **Agent** - Task-oriented AI with tools
4. **Workflow** - Custom multi-step processes

### 2. Build a Simple Chatbot

**Via Web Interface:**
1. Click "Create Application"
2. Select "Chatbot"
3. Choose your LLM model (e.g., GPT-4, Claude)
4. Configure system prompt
5. Test in playground
6. Publish as API or web app

**Example System Prompt:**
```
You are a helpful customer service assistant for TechCorp.
You can help users with:
- Product information
- Order tracking
- Technical support
- Account management

Be friendly, professional, and concise.
```

### 3. Add Knowledge Base (RAG)

**Create Knowledge Base:**
1. Go to "Knowledge" section
2. Click "Create Knowledge Base"
3. Upload documents (PDF, TXT, Markdown)
4. Configure chunking settings:
   - **Chunk size**: 500 tokens (recommended)
   - **Overlap**: 50 tokens
5. Select embedding model
6. Process documents

**Connect to Application:**
1. Open your chatbot
2. Add "Knowledge Retrieval" node
3. Select your knowledge base
4. Configure retrieval settings:
   - **Top K**: 3-5 results
   - **Score threshold**: 0.7
   - **Reranking**: Enable for better results

### 4. Using the API

**Python Example:**
```python
import requests

API_KEY = "your_dify_api_key"
API_URL = "http://localhost/v1"

# Send a chat message
response = requests.post(
    f"{API_URL}/chat-messages",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "inputs": {},
        "query": "What are your business hours?",
        "response_mode": "streaming",
        "conversation_id": "",
        "user": "user-123"
    }
)

for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
```

**Node.js Example:**
```javascript
const fetch = require('node-fetch');

const API_KEY = 'your_dify_api_key';
const API_URL = 'http://localhost/v1';

async function sendMessage(query) {
  const response = await fetch(`${API_URL}/chat-messages`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      inputs: {},
      query: query,
      response_mode: 'blocking',
      user: 'user-123'
    })
  });

  return await response.json();
}

sendMessage('Hello!').then(console.log);
```

## Workflow Development

### Visual Workflow Builder

**Core Nodes:**

1. **LLM Node** - Call language models
2. **Knowledge Retrieval** - Query knowledge bases
3. **Tool Node** - Execute functions and APIs
4. **Code Node** - Run custom Python/JavaScript
5. **Conditional** - Branch based on logic
6. **Variable Aggregator** - Combine data
7. **HTTP Request** - Call external APIs
8. **Template Transform** - Format text

### Example: Customer Support Workflow

```yaml
Workflow Steps:
1. Start → User Message
2. Knowledge Retrieval → Search documentation
3. Conditional Branch:
   - If relevant docs found → Use context
   - If not found → Use general knowledge
4. LLM Node → Generate response
5. Tool Node → Create ticket (if needed)
6. End → Return response
```

**Implementation:**
1. Drag "LLM" node to canvas
2. Connect to "Knowledge Retrieval" node
3. Add "Conditional" node with logic:
   ```python
   {{retrieval.score}} > 0.7
   ```
4. Configure LLM prompt:
   ```
   Context: {{retrieval.context}}
   User question: {{user.query}}

   Provide a helpful answer based on the context.
   If the context doesn't contain the answer, say so politely.
   ```

### Code Node Examples

**Python Code Node:**
```python
def main(data: dict) -> dict:
    # Access workflow variables
    user_query = data.get('query', '')

    # Custom processing
    processed = user_query.upper()

    # Return results
    return {
        'result': processed,
        'length': len(user_query)
    }
```

**JavaScript Code Node:**
```javascript
function main(data) {
  const query = data.query || '';

  // Process data
  const words = query.split(' ');

  return {
    word_count: words.length,
    first_word: words[0]
  };
}
```

## Agent Development

### Building an Agent with Tools

**Built-in Tools:**
- Google Search
- Wikipedia
- Weather APIs
- Calculator
- Web Scraper
- Database queries
- File operations
- Email sending

**Example: Research Agent**

```yaml
Agent Configuration:
  Model: gpt-4
  Reasoning Mode: ReAct
  Tools:
    - Google Search
    - Wikipedia
    - Web Scraper
  System Prompt: |
    You are a research assistant that helps users find
    accurate information from reliable sources.

    Always:
    1. Search for current information
    2. Cite your sources
    3. Verify facts from multiple sources
```

**Custom Tool Definition:**

```python
# Define custom tool for Dify
{
  "name": "check_inventory",
  "description": "Check product inventory levels",
  "parameters": {
    "type": "object",
    "properties": {
      "product_id": {
        "type": "string",
        "description": "Product identifier"
      }
    },
    "required": ["product_id"]
  }
}
```

## Knowledge Base Management

### Document Processing

**Supported Formats:**
- PDF
- Microsoft Word (.docx)
- PowerPoint (.pptx)
- Text files (.txt)
- Markdown (.md)
- HTML
- CSV

### Chunking Strategies

**1. Fixed Size Chunking:**
```yaml
Strategy: fixed_size
Chunk Size: 500 tokens
Overlap: 50 tokens
Use Case: General documents, articles
```

**2. Paragraph Chunking:**
```yaml
Strategy: paragraph
Min Size: 100 tokens
Max Size: 800 tokens
Use Case: Well-formatted documents
```

**3. Semantic Chunking:**
```yaml
Strategy: semantic
Model: text-embedding-ada-002
Similarity Threshold: 0.8
Use Case: Complex technical documents
```

### Retrieval Configuration

**Vector Search:**
```yaml
Type: vector
Top K: 5
Score Threshold: 0.7
Embedding Model: text-embedding-3-large
```

**Hybrid Retrieval:**
```yaml
Type: hybrid
Vector Weight: 0.7
Keyword Weight: 0.3
Reranking: enabled
Reranking Model: cross-encoder/ms-marco-MiniLM-L-12-v2
```

## API Integration

### REST API Endpoints

**Chat Messages:**
```bash
POST /v1/chat-messages
Content-Type: application/json
Authorization: Bearer {api_key}

{
  "inputs": {},
  "query": "Your question here",
  "response_mode": "streaming",
  "user": "user-identifier"
}
```

**Completion Messages:**
```bash
POST /v1/completion-messages
Content-Type: application/json
Authorization: Bearer {api_key}

{
  "inputs": {
    "name": "John",
    "topic": "AI"
  },
  "response_mode": "blocking",
  "user": "user-123"
}
```

**Feedback:**
```bash
POST /v1/messages/{message_id}/feedbacks
Content-Type: application/json
Authorization: Bearer {api_key}

{
  "rating": "like",
  "user": "user-123"
}
```

### SDK Usage

**Python SDK:**
```python
from dify_client import DifyClient

client = DifyClient(api_key="your_api_key")

# Chat completion
response = client.chat(
    query="What is Dify?",
    user="user-123",
    conversation_id=None
)

print(response.answer)
```

**Streaming Response:**
```python
for chunk in client.chat_stream(
    query="Explain quantum computing",
    user="user-123"
):
    print(chunk.delta, end="", flush=True)
```

## Best Practices

### Development

1. **Start Simple**: Begin with basic chatbots before complex workflows
2. **Test Incrementally**: Validate each node before connecting
3. **Use Variables**: Properly scope and name workflow variables
4. **Version Control**: Save workflow versions before major changes
5. **Monitor Costs**: Track token usage and API costs

### Production

1. **Security**:
   - Use environment variables for API keys
   - Implement rate limiting
   - Enable authentication on public endpoints
   - Regular security updates

2. **Performance**:
   - Cache frequent queries
   - Optimize knowledge base chunking
   - Use streaming for long responses
   - Implement connection pooling

3. **Monitoring**:
   ```yaml
   Metrics to Track:
     - Response latency
     - Token usage
     - Error rates
     - User satisfaction scores
     - Knowledge retrieval accuracy
   ```

4. **Scalability**:
   - Use load balancers
   - Scale workers horizontally
   - Separate databases for different services
   - Implement queue systems for async tasks

### Knowledge Base Optimization

1. **Document Quality**:
   - Clean and format documents before upload
   - Remove duplicates and outdated content
   - Use consistent terminology

2. **Chunking**:
   - Start with 500-token chunks
   - Adjust based on document structure
   - Use overlap for context preservation

3. **Retrieval Tuning**:
   - Monitor retrieval accuracy
   - Adjust score thresholds
   - Use reranking for critical applications
   - A/B test retrieval configurations

## Troubleshooting

### Common Issues

#### Issue 1: Docker Containers Won't Start

**Symptoms:**
- `docker compose up` fails
- Services crash on startup

**Solutions:**
```bash
# Check logs
docker compose logs

# Verify environment variables
cat .env

# Ensure ports are available
lsof -i :3000
lsof -i :5001

# Reset and restart
docker compose down -v
docker compose up -d
```

#### Issue 2: Knowledge Retrieval Returns No Results

**Symptoms:**
- Queries return empty results
- Low relevance scores

**Solutions:**
1. Check document processing status
2. Verify embedding model configuration
3. Lower score threshold temporarily
4. Test with exact document text
5. Rebuild knowledge base index

```bash
# Via API - trigger reindex
POST /v1/datasets/{dataset_id}/documents/{document_id}/processing
```

#### Issue 3: High Latency on API Calls

**Symptoms:**
- Slow response times
- Timeout errors

**Solutions:**
1. Enable caching:
   ```yaml
   cache:
     enabled: true
     ttl: 3600
   ```

2. Use streaming mode:
   ```python
   response_mode: "streaming"
   ```

3. Optimize LLM settings:
   ```yaml
   max_tokens: 500  # Reduce if possible
   temperature: 0.7
   top_p: 0.9
   ```

4. Check database performance:
   ```bash
   # Monitor PostgreSQL
   docker exec -it dify-db psql -U postgres -c "\
     SELECT pid, query, state, wait_event_type \
     FROM pg_stat_activity WHERE state != 'idle';"
   ```

#### Issue 4: Model API Errors

**Symptoms:**
- "Invalid API key" errors
- Rate limit exceeded

**Solutions:**
```bash
# Verify API keys in .env
cat .env | grep API_KEY

# Check provider status
curl https://status.openai.com/api/v2/status.json

# Implement retry logic
max_retries: 3
retry_delay: 1000  # milliseconds
```

### Debugging Tips

1. **Use Workflow Debugger**:
   - Step through each node
   - Inspect variable values
   - Check node execution time

2. **Enable Detailed Logging**:
   ```bash
   # In .env
   LOG_LEVEL=DEBUG
   ```

3. **Test Components Individually**:
   - Test LLM calls separately
   - Verify knowledge retrieval standalone
   - Test tools in isolation

4. **Monitor System Resources**:
   ```bash
   docker stats
   ```

## Advanced Topics

### Custom Model Providers

Add custom LLM providers:

```python
# model_providers/custom_provider.py
from dify.core.model_runtime import ModelProvider

class CustomProvider(ModelProvider):
    def get_models(self):
        return [
            {
                'model': 'custom-gpt',
                'label': 'Custom GPT Model',
                'model_type': 'llm'
            }
        ]

    def invoke(self, model, credentials, prompt, **kwargs):
        # Custom API call logic
        response = your_api_call(prompt)
        return response
```

### Workflow Optimization

**Parallel Execution:**
```yaml
Workflow:
  - Node1: LLM Call
  - Parallel:
      - Node2a: Knowledge Retrieval
      - Node2b: External API Call
  - Node3: Combine Results
```

**Conditional Caching:**
```python
# Cache expensive operations
if cache.exists(query_hash):
    return cache.get(query_hash)
else:
    result = expensive_operation()
    cache.set(query_hash, result, ttl=3600)
    return result
```

### Enterprise Deployment

**High Availability Setup:**
```yaml
Services:
  API:
    replicas: 3
    load_balancer: nginx
  Worker:
    replicas: 5
    queue: redis
  Database:
    primary: postgres-main
    replicas: 2
    backup: daily
```

**Monitoring Stack:**
```yaml
Monitoring:
  - Prometheus: Metrics collection
  - Grafana: Visualization
  - Loki: Log aggregation
  - Alertmanager: Alerts
```

## Resources

### Official Documentation
- **Main Docs**: https://docs.dify.ai/
- **GitHub**: https://github.com/langgenius/dify
- **API Reference**: https://docs.dify.ai/api-reference
- **Cloud Platform**: https://cloud.dify.ai

### Community
- **Discord**: https://discord.gg/dify
- **GitHub Discussions**: https://github.com/langgenius/dify/discussions
- **Issue Tracker**: https://github.com/langgenius/dify/issues

### Deployment Guides
- Kubernetes: https://github.com/langgenius/dify-helm
- AWS: https://github.com/langgenius/dify-aws
- Azure: https://github.com/langgenius/dify-azure
- Google Cloud: https://github.com/langgenius/dify-gcp

### Related Tools
- **LangChain**: Alternative framework for LLM apps
- **LlamaIndex**: Data framework for LLMs
- **Flowise**: Visual LLM workflow builder
- **LangFlow**: Drag-and-drop LLM pipeline builder

## Contributing

Dify is an active open-source project with 8,220+ commits.

**Ways to Contribute:**
1. Report bugs via GitHub Issues
2. Submit pull requests for features
3. Improve documentation
4. Share use cases and examples
5. Help with translations

**Development Setup:**
```bash
# Clone repository
git clone https://github.com/langgenius/dify.git
cd dify

# See deployment guide
# https://docs.dify.ai/development/deploy-from-source
```

**Security Issues:**
Email: security@dify.ai

## Version Information

**Last Updated**: 2025-12-15
**Skill Version**: 1.0.0
**Dify GitHub**: 8,220+ commits, actively maintained

---

*Note: Dify is rapidly evolving. Always check the official documentation for the latest features and best practices. This skill is based on official documentation and repository information as of December 2025.*
