# Quick Start Guide

Get the WhatsApp Knowledge Bot running in **5 minutes**.

## Prerequisites

- Docker and Docker Compose installed
- 8GB RAM minimum
- Ports available: 3000, 5001, 7474, 7687, 8000, 8080

## Step 1: Setup (2 minutes)

```bash
# Navigate to project
cd examples/whatsapp-knowledge-bot

# Copy environment file
cp .env.example .env

# Start all services
docker-compose up -d
```

## Step 2: Configure Dify (2 minutes)

```bash
# Wait for services to start (check with docker-compose ps)
# Then open Dify web interface
open http://localhost:3000
```

1. **Create account** - First time setup
2. **Create Chatbot app** - Click "Create Application" → "Chatbot"
3. **Add Knowledge Base**:
   - Go to "Knowledge" section
   - Click "Create Knowledge Base"
   - Upload a PDF or text file
   - Wait for processing
4. **Get API Key**:
   - Go to app Settings → API Access
   - Copy API key
   - Update `.env`: `DIFY_API_KEY=app-xxxxx`

## Step 3: Configure Evolution API (1 minute)

```bash
# Generate strong API key
EVOLUTION_KEY=$(openssl rand -hex 32)

# Update .env
echo "EVOLUTION_API_KEY=$EVOLUTION_KEY" >> .env

# Restart services
docker-compose restart
```

### Connect WhatsApp

1. Open http://localhost:8080
2. Create instance named "whatsapp-bot"
3. Use API key from `.env`
4. Scan QR code with WhatsApp
5. Wait for "Connected" status

## Step 4: Test (30 seconds)

```bash
# Check health
curl http://localhost:8000/health

# Send test message via WhatsApp
# Text your connected number: "Hello!"

# Check logs
docker-compose logs -f bot
```

You should see:
```
📨 Processing message from 5511999999999: Hello!
📚 Retrieved 0 context items for 5511999999999
✅ Dify response generated for 5511999999999
📤 Message sent to 5511999999999
💾 Stored interaction in Graphiti for 5511999999999
✅ Message handled successfully for 5511999999999
```

## Verify Integration

### 1. Check Evolution API

```bash
curl http://localhost:8080/instance/whatsapp-bot
```

Should show connected instance.

### 2. Check Dify

```bash
curl -X POST http://localhost:5001/v1/chat-messages \
  -H "Authorization: Bearer $DIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": {},
    "query": "test",
    "response_mode": "blocking",
    "user": "test"
  }'
```

Should return AI response.

### 3. Check Graphiti/Neo4j

```bash
# Open Neo4j Browser
open http://localhost:7474
# Login: neo4j / password123
# Run: MATCH (n) RETURN count(n)
```

Should show nodes created.

### 4. Check Bot Stats

```bash
# Replace with your phone number
curl http://localhost:8000/stats/5511999999999
```

Should show interaction count.

## Next Steps

### Customize Dify

1. **Add System Prompt**:
   ```
   You are a helpful WhatsApp assistant.
   Always be friendly and concise.
   Use conversation history to provide context-aware responses.
   ```

2. **Configure Knowledge Retrieval**:
   - Top K: 3-5 results
   - Score threshold: 0.7
   - Enable reranking

3. **Add Tools** (optional):
   - Weather API
   - Calendar integration
   - Database queries

### Monitor Conversations

```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f bot
docker-compose logs -f evolution-api
docker-compose logs -f dify-api

# View Neo4j graph
open http://localhost:7474
```

### Scale Up

For production:

1. **Add Load Balancer**: nginx/Caddy
2. **Enable HTTPS**: Let's Encrypt
3. **Add Monitoring**: Prometheus + Grafana
4. **Backup Database**: PostgreSQL + Neo4j backups
5. **Rate Limiting**: In bot code
6. **Error Recovery**: Retry logic + dead letter queue

## Troubleshooting

### Services not starting

```bash
# Check Docker resources
docker system df

# Increase Docker memory (Docker Desktop)
# Settings → Resources → Memory → 8GB

# Restart clean
docker-compose down -v
docker-compose up -d
```

### Bot not receiving messages

```bash
# Check webhook configuration
docker-compose exec evolution-api \
  curl http://bot:8000/health

# Should return {"status": "healthy"}

# Verify network
docker network inspect whatsapp-knowledge-bot_bot-network
```

### Dify API errors

```bash
# Check Dify logs
docker-compose logs dify-api | tail -50

# Verify API key
curl http://localhost:5001/v1/info \
  -H "Authorization: Bearer $DIFY_API_KEY"
```

### Neo4j connection errors

```bash
# Wait for Neo4j to fully start
docker-compose logs neo4j | grep "Started"

# Check connectivity
docker-compose exec bot \
  python -c "from neo4j import GraphDatabase; \
    driver = GraphDatabase.driver('bolt://neo4j:7687', \
    auth=('neo4j', 'password123')); driver.verify_connectivity()"
```

## Common Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f [service]

# Restart specific service
docker-compose restart bot

# Check status
docker-compose ps

# Clean everything (WARNING: deletes data)
docker-compose down -v

# Rebuild bot
docker-compose build bot
docker-compose up -d bot
```

## Success Criteria

✅ All services running (`docker-compose ps`)
✅ Dify web UI accessible (http://localhost:3000)
✅ Evolution API connected (QR scanned)
✅ Bot health check passing (http://localhost:8000/health)
✅ Test message processed successfully
✅ Neo4j storing conversations
✅ Dify RAG responding with knowledge base

## Getting Help

- Review full documentation: `README.md`
- Check architecture: `ARCHITECTURE.md`
- View skill docs: `../../output/*/SKILL.md`
- Debug logs: `docker-compose logs -f`

---

**Time to first message**: ~5 minutes ⚡
