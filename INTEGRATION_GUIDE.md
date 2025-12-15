# Multi-Skill Integration Guide

This guide demonstrates how to combine multiple Claude Skills to build production-ready applications.

## 🎯 Case Study: WhatsApp Knowledge Bot

Location: `examples/whatsapp-knowledge-bot/`

### Skills Integrated

1. **Evolution API Skill** (`output/evolution-api/SKILL.md`)
2. **Dify Skill** (`output/dify/SKILL.md`)
3. **Graphiti Skill** (`output/graphiti/SKILL.md`)

### Why These Skills?

| Skill | Purpose | Contribution |
|-------|---------|--------------|
| **Evolution API** | WhatsApp integration | Message reception & sending |
| **Dify** | LLM processing | RAG, knowledge base, AI responses |
| **Graphiti** | Temporal memory | Conversation history, context |

### Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Layer                              │
│  WhatsApp User → Message → WhatsApp Business API            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                   Communication Layer                        │
│  Evolution API (Skill 1)                                     │
│  • Receives messages via webhook                             │
│  • Manages WhatsApp connection                               │
│  • Sends responses back                                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  Integration Layer                           │
│  Knowledge Bot (Custom Python Service)                       │
│  • Orchestrates skill interactions                           │
│  • Implements business logic                                 │
│  • Handles error recovery                                    │
└────┬─────────────────────┬──────────────────┬───────────────┘
     │                     │                  │
     ↓                     ↓                  ↓
┌──────────┐      ┌──────────────┐    ┌─────────────┐
│ Graphiti │      │     Dify     │    │  Evolution  │
│ (Skill 3)│      │  (Skill 2)   │    │ API (Skill 1│
│          │      │              │    │             │
│ Context  │      │ RAG + LLM    │    │  Send       │
│ Retrieval│      │ Processing   │    │  Response   │
└──────────┘      └──────────────┘    └─────────────┘
```

## 📝 Implementation Steps

### Step 1: Define the Integration Flow

```python
# Flow designed based on user journey:

1. User sends WhatsApp message
   ↓
2. Evolution API receives (webhook)
   ↓
3. Bot retrieves conversation context (Graphiti)
   ↓
4. Bot processes with RAG (Dify)
   ↓
5. Bot sends response (Evolution API)
   ↓
6. Bot stores interaction (Graphiti)
```

### Step 2: Setup Service Communication

**Docker Compose Network**:

```yaml
networks:
  bot-network:
    driver: bridge

services:
  evolution-api:
    networks:
      - bot-network
    environment:
      - WEBHOOK_GLOBAL_URL=http://bot:8000/webhook
```

**Key Design Decision**: Internal Docker networking for service-to-service communication.

### Step 3: Implement Skill Integration

#### Skill 1: Evolution API (WhatsApp)

**Usage Pattern**: Webhook receiver + HTTP sender

```python
# Receive messages via webhook
@app.post("/webhook")
async def webhook_handler(request: Request):
    data = await request.json()
    # Extract WhatsApp message
    phone = extract_phone(data)
    message = extract_message(data)

    # Process in background
    background_tasks.add_task(bot.handle_message, phone, message)

# Send messages via HTTP API
async def send_whatsapp_message(phone: str, message: str):
    await http_client.post(
        f"{EVOLUTION_API_URL}/message/sendText/{INSTANCE}",
        headers={"apikey": API_KEY},
        json={"number": phone, "text": message}
    )
```

**Skill Documentation Used**:
- `output/evolution-api/SKILL.md` - Webhook configuration
- `output/evolution-api/SKILL.md` - Message sending API

#### Skill 2: Dify (RAG Processing)

**Usage Pattern**: HTTP API client with context injection

```python
async def process_with_dify(message: str, context: List[Dict]):
    # Build context string from Graphiti results
    context_str = "\n".join([
        f"[{ctx['timestamp']}] {ctx['content']}"
        for ctx in context
    ])

    # Call Dify with context
    response = await http_client.post(
        f"{DIFY_API_URL}/v1/chat-messages",
        json={
            "query": message,
            "inputs": {"conversation_history": context_str},
            "conversation_id": f"whatsapp_{phone}"
        }
    )

    return response.json()['answer']
```

**Skill Documentation Used**:
- `output/dify/SKILL.md` - API integration (Python example)
- `output/dify/SKILL.md` - Knowledge base configuration
- `output/dify/SKILL.md` - Conversation ID management

#### Skill 3: Graphiti (Temporal Memory)

**Usage Pattern**: Async graph operations

```python
# Initialize Graphiti connection
driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(user, pass))
graphiti = Graphiti(driver)

# Retrieve conversation context
async def get_conversation_context(phone: str):
    results = await graphiti.search(
        query=f"user {phone} conversations",
        num_results=5
    )
    return [
        {'timestamp': r.created_at, 'content': r.content}
        for r in results
    ]

# Store new interaction
async def store_interaction(phone, user_msg, bot_response):
    episode = f"User ({phone}): {user_msg}\nBot: {bot_response}"

    await graphiti.add_episode(
        name=f"conversation_{phone}_{timestamp}",
        episode_body=episode,
        reference_time=datetime.now()
    )
```

**Skill Documentation Used**:
- `output/graphiti/SKILL.md` - Python SDK initialization
- `output/graphiti/SKILL.md` - Episode creation
- `output/graphiti/SKILL.md` - Hybrid search

### Step 4: Orchestrate Skills

**Main handler integrating all three skills**:

```python
async def handle_message(phone: str, message: str):
    try:
        # Step 1: Get context from Graphiti (Skill 3)
        context = await self.get_conversation_context(phone)
        logger.info(f"Retrieved {len(context)} context items")

        # Step 2: Process with Dify (Skill 2)
        response = await self.process_with_dify(message, context, phone)
        logger.info(f"Generated response")

        # Step 3: Send via Evolution API (Skill 1)
        sent = await self.send_whatsapp_message(phone, response)

        if sent:
            # Step 4: Store in Graphiti (Skill 3)
            await self.store_interaction(
                phone, message, response, datetime.now()
            )

        logger.info("Message handled successfully")

    except Exception as e:
        logger.error(f"Error handling message: {e}")
        # Fallback: send error message
        await self.send_whatsapp_message(
            phone,
            "Sorry, I encountered an error. Please try again."
        )
```

## 🛠️ Integration Patterns

### Pattern 1: Skill Chaining

**When**: Linear flow of data through skills

```python
# Input → Skill A → Skill B → Skill C → Output
result = await skill_c(
    await skill_b(
        await skill_a(input)
    )
)
```

**Example**: WhatsApp Bot
- Input (message) → Graphiti (context) → Dify (response) → Evolution (send)

### Pattern 2: Skill Branching

**When**: Conditional skill selection

```python
if condition:
    result = await skill_a(input)
else:
    result = await skill_b(input)
```

**Example**: Smart routing based on message type
- Image → Dify vision model
- Text → Dify RAG pipeline
- Location → Graphiti spatial search

### Pattern 3: Parallel Skill Execution

**When**: Independent skill operations

```python
results = await asyncio.gather(
    skill_a(input),
    skill_b(input),
    skill_c(input)
)
```

**Example**: Multi-source enrichment
- Parallel: Graphiti context + Dify knowledge + External API

### Pattern 4: Event-Driven Integration

**When**: Asynchronous, decoupled services

```python
# Skill A emits event
await event_bus.publish("message.received", data)

# Skill B subscribes
@event_bus.subscribe("message.received")
async def handle(data):
    await skill_b(data)
```

**Example**: Message queue for reliability
- Evolution webhook → RabbitMQ → Bot → Graphiti

## 🎯 Integration Checklist

### Planning Phase

- [ ] Identify skills needed for use case
- [ ] Read each skill's documentation
- [ ] Map data flow between skills
- [ ] Define error handling strategy
- [ ] Plan monitoring approach

### Implementation Phase

- [ ] Setup Docker Compose for all skills
- [ ] Configure service networking
- [ ] Implement integration layer
- [ ] Add error handling & retries
- [ ] Add logging & observability
- [ ] Write health checks

### Testing Phase

- [ ] Test each skill independently
- [ ] Test skill integrations
- [ ] Test error scenarios
- [ ] Load test critical paths
- [ ] Security audit

### Documentation Phase

- [ ] Architecture diagram
- [ ] Setup instructions
- [ ] API documentation
- [ ] Troubleshooting guide
- [ ] Deployment guide

## 🚧 Common Challenges & Solutions

### Challenge 1: Service Dependencies

**Problem**: Services start in wrong order
**Solution**: Use `depends_on` + health checks

```yaml
services:
  bot:
    depends_on:
      evolution-api:
        condition: service_healthy
      dify-api:
        condition: service_healthy
```

### Challenge 2: Network Communication

**Problem**: Services can't reach each other
**Solution**: Use Docker network + service names

```python
# ❌ Bad: localhost won't work between containers
EVOLUTION_URL = "http://localhost:8080"

# ✅ Good: use service name from docker-compose
EVOLUTION_URL = "http://evolution-api:8080"
```

### Challenge 3: API Key Management

**Problem**: Hardcoded secrets
**Solution**: Environment variables + .env files

```python
# ❌ Bad
API_KEY = "sk-xxx"

# ✅ Good
API_KEY = os.getenv("DIFY_API_KEY")
```

### Challenge 4: Error Propagation

**Problem**: Errors cascade through skills
**Solution**: Circuit breaker + fallbacks

```python
async def safe_skill_call(skill_func, *args, fallback=None):
    try:
        return await skill_func(*args)
    except Exception as e:
        logger.error(f"Skill error: {e}")
        return fallback
```

### Challenge 5: Data Format Mismatches

**Problem**: Skill A output doesn't match Skill B input
**Solution**: Adapter pattern

```python
class SkillAdapter:
    @staticmethod
    def graphiti_to_dify(graphiti_results):
        """Convert Graphiti results to Dify context format"""
        return {
            "conversation_history": "\n".join([
                r.content for r in graphiti_results
            ])
        }
```

## 📊 Performance Considerations

### 1. Async Operations

```python
# ✅ Good: Parallel execution
context, knowledge = await asyncio.gather(
    graphiti.search(query),
    dify.query_knowledge_base(query)
)

# ❌ Bad: Sequential execution
context = await graphiti.search(query)
knowledge = await dify.query_knowledge_base(query)
```

### 2. Caching

```python
@lru_cache(maxsize=100)
async def get_user_context(phone: str):
    return await graphiti.search(f"user {phone}")
```

### 3. Connection Pooling

```python
# Reuse HTTP connections
http_client = httpx.AsyncClient(
    limits=httpx.Limits(max_connections=100)
)
```

### 4. Background Tasks

```python
# Don't block webhook responses
@app.post("/webhook")
async def webhook(request, background_tasks):
    background_tasks.add_task(process_message, data)
    return {"status": "queued"}  # Fast response
```

## 🔐 Security Best Practices

### 1. API Key Security

```python
# ✅ Use environment variables
API_KEY = os.getenv("SECRET_API_KEY")

# ✅ Validate keys exist
if not API_KEY:
    raise ValueError("API_KEY not configured")

# ✅ Never log keys
logger.info(f"Using key: {API_KEY[:5]}***")
```

### 2. Input Validation

```python
from pydantic import BaseModel, Field

class Message(BaseModel):
    phone: str = Field(..., regex=r"^\d{10,15}$")
    text: str = Field(..., max_length=4096)
```

### 3. Rate Limiting

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/webhook")
@limiter.limit("10/minute")
async def webhook(request):
    ...
```

## 📈 Monitoring Integration

### Health Checks

```python
@app.get("/health")
async def health():
    checks = {
        "evolution": await check_evolution_api(),
        "dify": await check_dify_api(),
        "neo4j": await check_neo4j()
    }

    status = "healthy" if all(checks.values()) else "degraded"
    return {"status": status, "checks": checks}
```

### Metrics

```python
from prometheus_client import Counter, Histogram

messages_processed = Counter(
    'messages_processed_total',
    'Total messages processed'
)

response_time = Histogram(
    'response_time_seconds',
    'Response time in seconds'
)

@app.post("/webhook")
async def webhook(request):
    with response_time.time():
        await process_message(request)
        messages_processed.inc()
```

## 🎓 Learning Resources

### Skill Documentation

- **Evolution API**: `output/evolution-api/SKILL.md`
- **Dify**: `output/dify/SKILL.md`
- **Graphiti**: `output/graphiti/SKILL.md`

### Example Implementation

- **Full code**: `examples/whatsapp-knowledge-bot/src/bot.py`
- **Docker setup**: `examples/whatsapp-knowledge-bot/docker-compose.yml`
- **Documentation**: `examples/whatsapp-knowledge-bot/README.md`

### External Resources

- Microservices: https://microservices.io/patterns/
- FastAPI: https://fastapi.tiangolo.com
- Docker Compose: https://docs.docker.com/compose/
- Async Python: https://docs.python.org/3/library/asyncio.html

## 🤝 Contributing Integrations

Want to create your own multi-skill integration?

1. **Choose skills** (≥2 from `output/`)
2. **Design flow** (data flow diagram)
3. **Implement** (follow patterns above)
4. **Document** (README + architecture)
5. **Test** (all integration points)
6. **Share** (PR to repository)

## ✅ Success Metrics

Your integration is successful when:

- ✅ All skills communicate correctly
- ✅ Error handling is robust
- ✅ Performance is acceptable
- ✅ Documentation is complete
- ✅ Tests cover integration points
- ✅ Deployment is repeatable
- ✅ Monitoring is in place

---

**Integration Philosophy**: Combine skills thoughtfully, document thoroughly, test extensively.
