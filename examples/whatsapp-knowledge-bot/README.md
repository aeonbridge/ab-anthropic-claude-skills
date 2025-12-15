# WhatsApp Knowledge Bot with Temporal Memory

**Multi-Skill Integration Example**

This project demonstrates a real-world integration of **three Claude AI Skills** to create an intelligent WhatsApp bot with temporal memory and RAG capabilities.

## 🎯 Skills Combined

### 1. Evolution API Skill (WhatsApp Integration)
- **Purpose**: Receive and send WhatsApp messages
- **Usage**: Webhook-based message handling, media support
- **Documentation**: `../../output/evolution-api/SKILL.md`

### 2. Dify Skill (LLM Processing & RAG)
- **Purpose**: Process messages with RAG pipeline
- **Usage**: Knowledge base queries, contextual responses
- **Documentation**: `../../output/dify/SKILL.md`

### 3. Graphiti Skill (Temporal Knowledge Graph)
- **Purpose**: Store and retrieve conversation history
- **Usage**: Bi-temporal memory, context retrieval
- **Documentation**: `../../output/graphiti/SKILL.md`

## 🏗️ Architecture

```
┌─────────────────┐
│   WhatsApp      │
│     User        │
└────────┬────────┘
         │ Message
         ↓
┌─────────────────────────────────────────────────┐
│           Evolution API (Skill 1)               │
│  • Receives WhatsApp messages via webhook       │
│  • Sends responses back to WhatsApp             │
└────────┬──────────────────────────┬─────────────┘
         │                          │
         │ HTTP Webhook             │ Send Message
         ↓                          ↑
┌─────────────────────────────────────────────────┐
│         Knowledge Bot (Integration)             │
│                                                 │
│  1. Get context → Graphiti                      │
│  2. Process     → Dify                          │
│  3. Respond     → Evolution API                 │
│  4. Store       → Graphiti                      │
└───┬─────────────────────────────────────┬───────┘
    │                                     │
    │ Query Context                       │ Store Interaction
    ↓                                     ↓
┌──────────────────────┐         ┌───────────────────┐
│  Graphiti (Skill 3)  │         │   Dify (Skill 2)  │
│  • Temporal Graph    │         │   • RAG Pipeline  │
│  • Neo4j Database    │         │   • Knowledge Base│
│  • Memory Retrieval  │         │   • LLM Processing│
└──────────────────────┘         └───────────────────┘
```

## 🚀 Features

### Intelligent Conversation
- **Context-Aware Responses**: Uses conversation history from Graphiti
- **RAG-Enhanced**: Queries knowledge base in Dify for accurate answers
- **Temporal Memory**: Remembers past interactions with timestamp precision

### WhatsApp Integration
- **Real-time Messages**: Instant webhook-based processing
- **Multi-user Support**: Handles multiple conversations simultaneously
- **Message Types**: Text, media, location support

### Knowledge Management
- **Bi-temporal Storage**: Event time + ingestion time tracking
- **Graph Relationships**: Links users, conversations, and topics
- **Efficient Retrieval**: Hybrid search for relevant context

## 📋 Prerequisites

- Docker and Docker Compose
- WhatsApp Business account (for production)
- API Keys:
  - Dify API key (create app at http://localhost:3000 after setup)
  - Optional: OpenAI/Anthropic API keys for LLM models

## 🛠️ Installation

### 1. Clone and Navigate

```bash
cd examples/whatsapp-knowledge-bot
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

**Required Configuration**:
```env
EVOLUTION_API_KEY=your-evolution-api-key
DIFY_API_KEY=your-dify-api-key
```

### 3. Start All Services

```bash
docker-compose up -d
```

This starts:
- Evolution API (Port 8080)
- Dify Web UI (Port 3000)
- Dify API (Port 5001)
- Neo4j Browser (Port 7474)
- Knowledge Bot (Port 8000)
- Supporting services (PostgreSQL, Redis, Weaviate)

### 4. Setup Dify

1. Open http://localhost:3000
2. Create an account
3. Create a new Chatbot application
4. Add a knowledge base
5. Upload documentation or content
6. Get API key from Settings → API Access
7. Update `DIFY_API_KEY` in `.env`

### 5. Setup Evolution API

1. Open http://localhost:8080
2. Create a WhatsApp instance named "whatsapp-bot"
3. Scan QR code with WhatsApp
4. Verify webhook is configured: http://bot:8000/webhook

### 6. Restart Bot with New Keys

```bash
docker-compose restart bot
```

## 📊 Usage

### Send a Message

Send a WhatsApp message to your connected number:

```
User: "What are your business hours?"
```

**What Happens**:

1. **Evolution API** receives message via webhook
2. **Bot** queries **Graphiti** for conversation history
3. **Bot** sends query to **Dify** with context
4. **Dify** searches knowledge base and generates response
5. **Bot** sends response via **Evolution API**
6. **Bot** stores interaction in **Graphiti**

### View Conversation Context

Check stored context for a user:

```bash
curl http://localhost:8000/stats/5511999999999
```

Response:
```json
{
  "phone": "5511999999999",
  "total_interactions": 15,
  "recent_interactions": [
    {
      "timestamp": "2025-12-15T10:30:00",
      "content": "User asked about hours...",
      "relevance": 0.95
    }
  ]
}
```

### Check Health

```bash
curl http://localhost:8000/health
```

## 🔍 How It Works

### Message Flow

```python
# 1. Evolution API Webhook → Bot
@app.post("/webhook")
async def webhook_handler(request: Request):
    # Receives WhatsApp message
    message = extract_message(request)

# 2. Bot → Graphiti (Get Context)
context = await bot.get_conversation_context(phone)
# Returns: List of previous interactions

# 3. Bot → Dify (Process with RAG)
response = await bot.process_with_dify(
    message=user_message,
    context=context,
    phone=phone
)
# Returns: AI-generated response with knowledge base

# 4. Bot → Evolution API (Send Response)
await bot.send_whatsapp_message(phone, response)

# 5. Bot → Graphiti (Store Interaction)
await bot.store_interaction(
    phone=phone,
    user_message=user_message,
    bot_response=response,
    timestamp=datetime.now()
)
```

### Skill Integration Details

#### Skill 1: Evolution API (WhatsApp)

```python
# Sending messages
await http_client.post(
    f"{EVOLUTION_API_URL}/message/sendText/{INSTANCE}",
    headers={"apikey": API_KEY},
    json={"number": phone, "text": message}
)
```

**Why this skill**: Handles all WhatsApp communication, QR code pairing, webhook management.

#### Skill 2: Dify (LLM & RAG)

```python
# Processing with RAG
response = await http_client.post(
    f"{DIFY_API_URL}/v1/chat-messages",
    json={
        "query": message,
        "inputs": {"conversation_history": context},
        "user": phone,
        "conversation_id": f"whatsapp_{phone}"
    }
)
```

**Why this skill**: Provides RAG pipeline, knowledge base, LLM orchestration, visual workflow.

#### Skill 3: Graphiti (Temporal Memory)

```python
# Storing episodes
await graphiti.add_episode(
    name=f"conversation_{phone}_{timestamp}",
    episode_body=conversation_text,
    reference_time=timestamp
)

# Retrieving context
results = await graphiti.search(
    query=f"user {phone} conversations",
    num_results=5
)
```

**Why this skill**: Bi-temporal graph storage, efficient context retrieval, relationship tracking.

## 📈 Advanced Features

### Custom Workflows in Dify

1. Create workflow in Dify UI
2. Add nodes:
   - LLM Node for processing
   - Knowledge Retrieval for RAG
   - Conditional for routing
3. Connect to bot via API

### Temporal Queries in Graphiti

```python
# Get conversations from specific time period
results = await graphiti.search(
    query=f"conversations with {phone} last week",
    num_results=10,
    filters={"created_at": {"gte": week_ago}}
)
```

### Multi-Channel Support

Extend to other channels:
- Telegram (similar webhook pattern)
- Slack (Slack API + same bot core)
- Web chat (WebSocket + same processing)

## 🐛 Troubleshooting

### Bot not receiving messages

**Check**:
```bash
# Verify webhook configuration
curl http://localhost:8080/instance/whatsapp-bot

# Check bot logs
docker-compose logs -f bot
```

**Solution**: Ensure webhook URL is `http://bot:8000/webhook` (internal Docker network)

### Dify connection errors

**Check**:
```bash
# Verify Dify is running
curl http://localhost:5001/health

# Check API key
echo $DIFY_API_KEY
```

**Solution**: Create app in Dify UI and get valid API key

### Graphiti/Neo4j errors

**Check**:
```bash
# Verify Neo4j is running
docker-compose logs neo4j

# Access Neo4j Browser
open http://localhost:7474
# Login: neo4j / password123
```

**Solution**: Ensure Neo4j has started completely (can take 30-60 seconds)

### Evolution API not connecting to WhatsApp

**Solution**:
1. Restart instance in Evolution UI
2. Scan QR code again
3. Check firewall/network settings

## 📊 Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f bot
docker-compose logs -f evolution-api
docker-compose logs -f dify-api
```

### Neo4j Graph Visualization

1. Open http://localhost:7474
2. Login with neo4j/password123
3. Query conversations:

```cypher
// View all episodes
MATCH (e:Episode)
RETURN e
LIMIT 25

// View user conversations
MATCH (e:Episode)
WHERE e.name CONTAINS '5511999999999'
RETURN e
ORDER BY e.created_at DESC
```

### Dify Analytics

1. Open http://localhost:3000
2. Go to your app
3. View Analytics tab for:
   - Message counts
   - Response times
   - Knowledge base hit rate

## 🔐 Security

### Production Deployment

1. **Use Environment Variables**: Never commit API keys
2. **Enable Authentication**: Configure Evolution API auth
3. **HTTPS Only**: Use reverse proxy (nginx/Caddy)
4. **Rate Limiting**: Implement in bot code
5. **Input Validation**: Sanitize all user inputs

### Recommended `.env` for Production

```env
# Strong API keys
EVOLUTION_API_KEY=$(openssl rand -hex 32)
DIFY_SECRET_KEY=$(openssl rand -hex 32)
NEO4J_PASSWORD=$(openssl rand -hex 16)

# Enable SSL for Neo4j
NEO4J_URI=bolt+s://neo4j:7687

# Production URLs
EVOLUTION_API_URL=https://evolution.yourdomain.com
DIFY_API_URL=https://dify.yourdomain.com
```

## 📚 Learn More

### Skill Documentation

- **Evolution API**: `../../output/evolution-api/SKILL.md`
- **Dify**: `../../output/dify/SKILL.md`
- **Graphiti**: `../../output/graphiti/SKILL.md`

### Official Resources

- Evolution API: https://doc.evolution-api.com
- Dify: https://docs.dify.ai
- Graphiti: https://github.com/getzep/graphiti

## 🤝 Contributing

Improvements welcome! Consider adding:
- More message types (images, voice, video)
- Sentiment analysis
- Multi-language support
- Analytics dashboard
- Admin commands

## 📄 License

This example is part of the Claude Skills repository (Apache-2.0).

## 🎓 What You Learned

This example demonstrates:

1. **Multi-Skill Integration**: Combining 3 independent skills
2. **Microservices Architecture**: Docker Compose orchestration
3. **Asynchronous Processing**: FastAPI + background tasks
4. **Temporal Data**: Bi-temporal knowledge graphs
5. **RAG Implementation**: Knowledge base + LLM synthesis
6. **Webhook Handling**: Real-time message processing
7. **Production Patterns**: Health checks, logging, error handling

---

**Built with Claude Skills** - Demonstrating the power of skill composition.
