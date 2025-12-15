---
name: graphiti
description: Comprehensive skill for Graphiti and Zep - temporal knowledge graph framework for AI agents with dynamic context engineering
version: 1.0.0
---

# Graphiti & Zep Knowledge Graph Skill

Expert assistance for building AI agents with temporal knowledge graphs using Graphiti and Zep's context engineering platform for dynamic, personalized agent memory and context assembly.

## When to Use This Skill

This skill should be used when:
- Building AI agents that need persistent memory across conversations
- Implementing knowledge graphs for agent applications
- Creating personalized user experiences with context awareness
- Managing evolving relationships and historical context
- Integrating enterprise data with agent systems
- Building Graph RAG (Retrieval-Augmented Generation) applications
- Tracking user preferences, traits, and interaction history
- Querying temporal data with point-in-time accuracy
- Reducing hallucinations through structured context
- Implementing multi-user agent systems with individual memory
- Working with Zep's context engineering platform
- Integrating with LangGraph, CrewAI, Autogen, or other agent frameworks

## Overview

### Graphiti - Temporal Knowledge Graph Framework

**Graphiti** is an open-source framework for constructing and querying time-aware knowledge graphs optimized for AI agents in dynamic environments.

**Key Characteristics:**
- **Temporal**: Bi-temporal data model tracking both event occurrence and ingestion times
- **Incremental**: Real-time data integration without batch reprocessing
- **Hybrid Search**: Combines semantic embeddings, BM25 keyword matching, and graph traversal
- **Low Latency**: Sub-second query performance without LLM-dependent summarization
- **Flexible**: Customizable entity definitions via Pydantic models
- **Scalable**: Enterprise-scale parallel processing

### Zep - Context Engineering Platform

**Zep** is a production-ready platform built on Graphiti that provides:
- Agent memory management
- Graph RAG optimization
- User and conversation management
- Developer dashboards and monitoring
- Enterprise features (RBAC, BYOK, BYOLLM)
- Integration with major agent frameworks

**Core Value Proposition:**
> "Assembles personalized context—including user preferences, traits, and business data—for reliable agent applications"

## Core Concepts

### 1. Temporal Knowledge Graphs

Graphiti creates time-stamped relationship networks that:
- Maintain historical context
- Track changes over time
- Support point-in-time queries
- Preserve relationship evolution

**Bi-Temporal Model:**
- **Valid Time**: When an event actually occurred
- **Transaction Time**: When the data was ingested into the system

### 2. Entities and Relations

**Entities**: Objects or concepts in your knowledge graph
- Users, products, concepts, locations, etc.
- Customizable via Pydantic models
- Can have attributes and properties
- Time-stamped for historical tracking

**Relations**: Connections between entities
- Typed relationships (e.g., "likes", "purchased", "mentioned")
- Directional (from entity A to entity B)
- Can have weights, properties, and metadata
- Temporal tracking of relationship changes

### 3. Facts and Summaries

**Facts**: Extracted information from conversations and data
- Automatically extracted from chat history
- Derived from structured/unstructured business data
- Form the basis of the knowledge graph
- Time-stamped and attributed to sources

**Summaries**: Condensed representations of interactions
- Generated as conversations unfold
- Capture key points and themes
- Enable efficient context retrieval
- Maintain temporal coherence

### 4. Hybrid Search

Graphiti uses three complementary search methods:

**Semantic Search**:
- Vector embeddings for conceptual similarity
- Finds semantically related entities and facts

**Keyword Search (BM25)**:
- Traditional text matching
- Precise term-based retrieval

**Graph Traversal**:
- Follow relationships between entities
- Discover connected information
- Navigate the knowledge network

## Installation

### Graphiti (Open Source)

```bash
# Install from PyPI
pip install graphiti-core

# Or from source
git clone https://github.com/getzep/graphiti.git
cd graphiti
pip install -e .
```

### Zep (Platform)

```bash
# Python SDK
pip install zep-cloud

# TypeScript SDK
npm install @getzep/zep-cloud

# Go SDK
go get github.com/getzep/zep-go
```

### Database Requirements

Graphiti supports multiple graph database backends:

**Neo4j** (Recommended)
```bash
# Docker
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:5.26
```

**FalkorDB**
```bash
docker run -d \
  --name falkordb \
  -p 6379:6379 \
  falkordb/falkordb:1.1.2
```

**Kuzu**
```bash
pip install kuzu
```

**Amazon Neptune** (Enterprise)
- Use with OpenSearch Serverless
- See AWS documentation for setup

### LLM Configuration

Graphiti works with various LLM providers:

```python
# OpenAI (default)
import os
os.environ["OPENAI_API_KEY"] = "your-key"

# Anthropic Claude
os.environ["ANTHROPIC_API_KEY"] = "your-key"

# Google Gemini
os.environ["GOOGLE_API_KEY"] = "your-key"

# Azure OpenAI
os.environ["AZURE_OPENAI_API_KEY"] = "your-key"
os.environ["AZURE_OPENAI_ENDPOINT"] = "your-endpoint"
```

## Quick Start with Graphiti

### Basic Setup

```python
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType

# Initialize Graphiti with Neo4j
graphiti = Graphiti(
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password"
)

# Initialize the graph
await graphiti.build_indices_and_constraints()
```

### Adding Episodes (Messages/Events)

```python
# Add a conversation message
await graphiti.add_episode(
    name="User Message",
    episode_body="I love hiking in the mountains, especially in Colorado.",
    source_description="User conversation",
    reference_time=datetime.now(),
    episode_type=EpisodeType.message
)

# Add business data
await graphiti.add_episode(
    name="Purchase Event",
    episode_body="User purchased hiking boots size 10",
    source_description="E-commerce transaction",
    reference_time=datetime.now(),
    episode_type=EpisodeType.json
)

# Add document/file content
await graphiti.add_episode(
    name="User Profile",
    episode_body="John is a 35-year-old software engineer based in Denver",
    source_description="User profile document",
    reference_time=datetime.now(),
    episode_type=EpisodeType.text
)
```

### Querying the Graph

```python
# Search for relevant context
results = await graphiti.search(
    query="What outdoor activities does the user enjoy?",
    num_results=10
)

for result in results:
    print(f"Entity: {result.name}")
    print(f"Content: {result.content}")
    print(f"Relevance: {result.score}")
    print("---")

# Point-in-time query (historical data)
from datetime import datetime, timedelta

past_time = datetime.now() - timedelta(days=30)
historical_results = await graphiti.search(
    query="User preferences",
    reference_time=past_time,
    num_results=5
)
```

### Custom Entity Types

```python
from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    """Custom product entity"""
    name: str = Field(description="Product name")
    category: str = Field(description="Product category")
    price: Optional[float] = Field(description="Product price")
    in_stock: bool = Field(default=True, description="Availability status")

class Customer(BaseModel):
    """Custom customer entity"""
    name: str = Field(description="Customer name")
    email: str = Field(description="Customer email")
    tier: str = Field(description="Customer tier: basic, premium, enterprise")
    lifetime_value: Optional[float] = Field(description="Total customer value")

# Register custom entity types
graphiti.register_entity_type(Product)
graphiti.register_entity_type(Customer)

# Add episodes with custom entities
await graphiti.add_episode(
    name="Product Purchase",
    episode_body="Customer john@example.com purchased Premium Hiking Boots for $150",
    source_description="Transaction log",
    reference_time=datetime.now(),
    entity_types=[Customer, Product]
)
```

## Working with Zep Platform

### Python SDK

```python
from zep_cloud.client import AsyncZep
from zep_cloud import Message

# Initialize Zep client
zep = AsyncZep(api_key="your-api-key")

# Create a user
user = await zep.user.add(
    user_id="user_123",
    email="user@example.com",
    first_name="John",
    last_name="Doe",
    metadata={"plan": "premium"}
)

# Create a session (conversation thread)
session = await zep.memory.add_session(
    session_id="session_456",
    user_id="user_123",
    metadata={"channel": "web"}
)

# Add messages to build memory
await zep.memory.add_memory(
    session_id="session_456",
    messages=[
        Message(
            role="user",
            content="I'm planning a hiking trip to Colorado next month"
        ),
        Message(
            role="assistant",
            content="That sounds great! What areas are you considering?"
        )
    ]
)

# Retrieve relevant context
memory = await zep.memory.get_memory(
    session_id="session_456"
)

# Get facts from the knowledge graph
facts = memory.facts

# Get user summary
summary = memory.summary

# Search across user's graph
search_results = await zep.memory.search_memory(
    user_id="user_123",
    text="outdoor activities and preferences",
    search_scope="facts"
)
```

### TypeScript SDK

```typescript
import { ZepClient } from "@getzep/zep-cloud";

// Initialize client
const zep = new ZepClient({ apiKey: "your-api-key" });

// Create user
const user = await zep.user.add({
  userId: "user_123",
  email: "user@example.com",
  firstName: "John",
  lastName: "Doe"
});

// Add messages
await zep.memory.addMemory("session_456", {
  messages: [
    { role: "user", content: "I love mountain biking" },
    { role: "assistant", content: "Great! Where do you usually ride?" }
  ]
});

// Get memory with context
const memory = await zep.memory.getMemory("session_456");
console.log("Facts:", memory.facts);
console.log("Summary:", memory.summary);

// Search user's knowledge graph
const results = await zep.memory.searchMemory({
  userId: "user_123",
  text: "outdoor hobbies",
  searchScope: "facts"
});
```

## Advanced Features

### 1. Batch Data Ingestion

```python
# Add multiple episodes efficiently
episodes = [
    {
        "name": f"Message {i}",
        "episode_body": f"Content {i}",
        "source_description": "Batch import",
        "reference_time": datetime.now(),
        "episode_type": EpisodeType.message
    }
    for i in range(100)
]

# Process in parallel
for episode in episodes:
    await graphiti.add_episode(**episode)
```

### 2. Custom Ontologies

```python
# Define domain-specific relationships
ontology = {
    "entities": ["Customer", "Product", "Order", "Support Ticket"],
    "relations": [
        {"type": "purchased", "from": "Customer", "to": "Product"},
        {"type": "contains", "from": "Order", "to": "Product"},
        {"type": "created", "from": "Customer", "to": "Support Ticket"},
        {"type": "related_to", "from": "Support Ticket", "to": "Product"}
    ]
}

# Use ontology in episode processing
await graphiti.add_episode(
    name="Customer Support",
    episode_body="Customer had issue with hiking boots, opened ticket",
    source_description="Support system",
    reference_time=datetime.now(),
    ontology=ontology
)
```

### 3. Graph Traversal Queries

```python
# Find connected entities
from graphiti_core.search import GraphTraversal

# Find all products a user has purchased
traversal = GraphTraversal(
    start_entity="user_123",
    relationship_types=["purchased"],
    max_depth=2
)

related_products = await graphiti.traverse(traversal)

# Find similar users based on preferences
similar_users = await graphiti.find_similar_entities(
    entity_id="user_123",
    entity_type="Customer",
    similarity_threshold=0.7
)
```

### 4. Context Assembly

```python
# Assemble comprehensive context for agent
context = await zep.memory.get_memory(
    session_id="session_456",
    memory_type="perpetual"  # Includes full user graph
)

# Build agent prompt with context
system_prompt = f"""
You are a helpful assistant. Here's what you know about the user:

User Summary: {context.summary}

Recent Facts:
{chr(10).join(f"- {fact}" for fact in context.facts[:5])}

User Preferences:
{chr(10).join(f"- {pref}" for pref in context.relevant_facts)}
"""

# Use in your agent framework
from langchain.chat_models import ChatAnthropic

llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
response = llm.invoke([
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "Recommend some activities for my trip"}
])
```

### 5. Temporal Queries

```python
# Query what was known at a specific time
from datetime import datetime, timedelta

# What did we know 7 days ago?
past_date = datetime.now() - timedelta(days=7)
past_context = await graphiti.search(
    query="user preferences",
    reference_time=past_date
)

# Track how knowledge evolved
current_context = await graphiti.search(
    query="user preferences",
    reference_time=datetime.now()
)

# Compare past vs current
print("7 days ago:", past_context)
print("Current:", current_context)
```

## Integration with Agent Frameworks

### LangGraph Integration

```python
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from zep_cloud.client import AsyncZep

# Initialize
zep = AsyncZep(api_key="your-key")
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# Define agent state
class AgentState(TypedDict):
    messages: list
    user_id: str
    session_id: str
    context: str

# Context retrieval node
async def get_context(state: AgentState):
    memory = await zep.memory.get_memory(state["session_id"])
    context = f"Summary: {memory.summary}\nFacts: {memory.facts}"
    return {"context": context}

# LLM node with context
async def call_llm(state: AgentState):
    system_msg = f"Context: {state['context']}"
    messages = [{"role": "system", "content": system_msg}] + state["messages"]
    response = await llm.ainvoke(messages)
    return {"messages": state["messages"] + [response]}

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("get_context", get_context)
workflow.add_node("call_llm", call_llm)
workflow.add_edge("get_context", "call_llm")
workflow.add_edge("call_llm", END)
workflow.set_entry_point("get_context")

app = workflow.compile()

# Run agent
result = await app.ainvoke({
    "messages": [{"role": "user", "content": "Plan my trip"}],
    "user_id": "user_123",
    "session_id": "session_456",
    "context": ""
})
```

### CrewAI Integration

```python
from crewai import Agent, Task, Crew
from zep_cloud.client import AsyncZep

# Initialize Zep
zep = AsyncZep(api_key="your-key")

# Custom tool for memory retrieval
from crewai_tools import tool

@tool("get_user_context")
async def get_user_context(user_id: str) -> str:
    """Retrieve user context from Zep knowledge graph"""
    results = await zep.memory.search_memory(
        user_id=user_id,
        text="preferences and history",
        search_scope="facts"
    )
    return "\n".join([r.content for r in results])

# Create agent with memory
planning_agent = Agent(
    role="Travel Planner",
    goal="Create personalized travel plans",
    backstory="Expert at creating customized itineraries",
    tools=[get_user_context],
    verbose=True
)

# Define task
task = Task(
    description="Plan a hiking trip for user_123 based on their preferences",
    agent=planning_agent,
    expected_output="Detailed 3-day itinerary"
)

# Create crew
crew = Crew(
    agents=[planning_agent],
    tasks=[task]
)

# Execute with context
result = crew.kickoff()
```

## Use Cases and Examples

### 1. E-commerce Personalization

```python
# Track customer behavior
await graphiti.add_episode(
    name="Product View",
    episode_body="Customer viewed Premium Hiking Boots, spent 5 minutes",
    source_description="Analytics",
    reference_time=datetime.now()
)

await graphiti.add_episode(
    name="Cart Addition",
    episode_body="Customer added Premium Hiking Boots size 10 to cart",
    source_description="E-commerce",
    reference_time=datetime.now()
)

# Retrieve personalized recommendations
context = await graphiti.search(
    query="Products customer is interested in",
    num_results=5
)

# Use for recommendation agent
recommendations = llm.invoke(f"""
Based on this context: {context}
Recommend 3 products the customer might like.
""")
```

### 2. Customer Support Agent

```python
# Build comprehensive support context
support_context = await zep.memory.get_memory(session_id="support_789")

# Include:
# - Past issues and resolutions
# - Product ownership
# - Communication preferences
# - Account history

system_prompt = f"""
You are a customer support agent.

Customer History:
{support_context.summary}

Previous Issues:
{support_context.facts}

Provide helpful, personalized support.
"""

# Support agent with full context
support_agent = Agent(
    model="claude-3-5-sonnet-20241022",
    system=system_prompt
)
```

### 3. Healthcare Assistant (HIPAA-Compliant)

```python
# Track patient information securely
await graphiti.add_episode(
    name="Patient Visit",
    episode_body="Patient reported back pain, prescribed physical therapy",
    source_description="EMR System",
    reference_time=datetime.now(),
    metadata={"confidential": True, "hipaa_compliant": True}
)

# Retrieve medical history for treatment
medical_history = await graphiti.search(
    query="patient symptoms and treatments",
    filters={"metadata.confidential": True}
)

# Use Zep's enterprise features for compliance
# - RBAC for access control
# - Audit logging
# - Data encryption
# - BYOK (Bring Your Own Key)
```

### 4. Multi-User Chat Application

```python
# Track individual user contexts in group chat
users = ["user_1", "user_2", "user_3"]

for user_id in users:
    # Each user has their own knowledge graph
    await zep.user.add(user_id=user_id)

# Add messages with user attribution
await zep.memory.add_memory(
    session_id="group_chat_123",
    messages=[
        Message(role="user", content="I prefer morning meetings",
                metadata={"user_id": "user_1"}),
        Message(role="user", content="I'm usually free after 2pm",
                metadata={"user_id": "user_2"})
    ]
)

# Retrieve context for each user
for user_id in users:
    user_context = await zep.memory.search_memory(
        user_id=user_id,
        text="scheduling preferences"
    )
    print(f"{user_id} preferences: {user_context}")
```

## Best Practices

### 1. Efficient Data Ingestion

```python
# Batch episodes for better performance
async def batch_ingest(episodes, batch_size=50):
    for i in range(0, len(episodes), batch_size):
        batch = episodes[i:i + batch_size]
        await asyncio.gather(*[
            graphiti.add_episode(**ep) for ep in batch
        ])
```

### 2. Context Window Management

```python
# Limit context to most relevant information
def assemble_context(memory, max_facts=10, max_tokens=4000):
    facts = memory.facts[:max_facts]
    context = f"Summary: {memory.summary}\n\nKey Facts:\n"

    for fact in facts:
        context += f"- {fact}\n"
        if len(context) > max_tokens:
            break

    return context[:max_tokens]
```

### 3. Entity Resolution

```python
# Handle entity variations and aliases
entity_aliases = {
    "Colorado": ["CO", "Colorful Colorado", "Centennial State"],
    "hiking": ["trekking", "backpacking", "trail walking"]
}

# Normalize entities before ingestion
def normalize_episode(text):
    for canonical, aliases in entity_aliases.items():
        for alias in aliases:
            text = text.replace(alias, canonical)
    return text
```

### 4. Privacy and Security

```python
# Implement data retention policies
from datetime import timedelta

async def cleanup_old_data(user_id, retention_days=90):
    cutoff_date = datetime.now() - timedelta(days=retention_days)

    # Delete old episodes
    await graphiti.delete_episodes(
        user_id=user_id,
        before_date=cutoff_date
    )

# Redact sensitive information
def redact_pii(text):
    import re
    # Redact email addresses
    text = re.sub(r'\b[\w.-]+@[\w.-]+\.\w+\b', '[EMAIL]', text)
    # Redact phone numbers
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
    return text
```

### 5. Monitoring and Debugging

```python
# Log graph operations
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("graphiti")

async def add_episode_with_logging(graphiti, **kwargs):
    logger.info(f"Adding episode: {kwargs['name']}")
    try:
        result = await graphiti.add_episode(**kwargs)
        logger.info(f"Successfully added episode: {result}")
        return result
    except Exception as e:
        logger.error(f"Failed to add episode: {e}")
        raise

# Track performance metrics
import time

async def search_with_metrics(graphiti, query):
    start = time.time()
    results = await graphiti.search(query)
    latency = time.time() - start
    logger.info(f"Search latency: {latency:.3f}s, Results: {len(results)}")
    return results
```

## Troubleshooting

### Common Issues

#### "Connection to graph database failed"
```python
# Verify database is running
# For Neo4j:
docker ps | grep neo4j

# Test connection
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "password")
)

with driver.session() as session:
    result = session.run("RETURN 1 as num")
    print(result.single()["num"])  # Should print 1
```

#### "Rate limit exceeded"
```python
# Implement exponential backoff
import asyncio

async def add_episode_with_retry(graphiti, max_retries=3, **kwargs):
    for attempt in range(max_retries):
        try:
            return await graphiti.add_episode(**kwargs)
        except RateLimitError:
            wait_time = 2 ** attempt
            await asyncio.sleep(wait_time)
    raise Exception("Max retries exceeded")
```

#### "Search returns no results"
```python
# Debug search configuration
results = await graphiti.search(
    query="user preferences",
    num_results=20,  # Increase number
    search_config={
        "semantic_weight": 0.5,  # Adjust weights
        "bm25_weight": 0.3,
        "graph_weight": 0.2
    }
)

# Check if data exists
all_nodes = await graphiti.get_all_nodes(limit=10)
print(f"Total nodes in graph: {len(all_nodes)}")
```

## Configuration Options

### Graphiti Configuration

```python
from graphiti_core import Graphiti
from graphiti_core.llm import OpenAIClient

graphiti = Graphiti(
    # Database
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password",

    # LLM
    llm_client=OpenAIClient(
        model="gpt-4o",
        temperature=0.7
    ),

    # Search configuration
    search_config={
        "semantic_weight": 0.5,
        "bm25_weight": 0.3,
        "graph_weight": 0.2
    },

    # Processing
    max_workers=4,  # Parallel processing
    batch_size=50,  # Batch size for ingestion

    # Embeddings
    embedding_model="text-embedding-3-small",
    embedding_dim=1536
)
```

### Zep Platform Configuration

```python
from zep_cloud.client import AsyncZep

zep = AsyncZep(
    api_key="your-api-key",

    # Optional: Custom endpoint
    base_url="https://api.getzep.com",

    # Timeout settings
    timeout=30.0,

    # Retry configuration
    max_retries=3
)
```

## Performance Optimization

### 1. Indexing Strategy

```python
# Create optimal indices
await graphiti.build_indices_and_constraints()

# Custom indices for frequently queried properties
await graphiti.create_index("User", "email")
await graphiti.create_index("Product", "sku")
```

### 2. Query Optimization

```python
# Use filters to narrow search scope
results = await graphiti.search(
    query="hiking products",
    filters={
        "entity_type": "Product",
        "category": "outdoor",
        "price_range": {"min": 50, "max": 200}
    },
    num_results=5
)

# Limit traversal depth for graph queries
results = await graphiti.traverse(
    start_node="user_123",
    max_depth=2,  # Limit depth
    relationship_types=["purchased", "viewed"]
)
```

### 3. Caching

```python
from functools import lru_cache
import hashlib

# Cache frequent searches
@lru_cache(maxsize=100)
def cache_key(query, user_id):
    return hashlib.md5(f"{query}:{user_id}".encode()).hexdigest()

async def cached_search(graphiti, query, user_id):
    key = cache_key(query, user_id)
    # Implement your caching logic
    return await graphiti.search(query)
```

## Resources

### Documentation
- **Graphiti GitHub**: https://github.com/getzep/graphiti
- **Zep Documentation**: https://help.getzep.com/
- **Zep Concepts**: https://help.getzep.com/concepts
- **SDK Reference**: https://help.getzep.com/sdk-reference

### Supported Databases
- Neo4j 5.26+
- FalkorDB 1.1.2+
- Kuzu 0.11.2+
- Amazon Neptune with OpenSearch Serverless

### Supported LLM Providers
- OpenAI (GPT-4, GPT-4o, GPT-3.5)
- Anthropic (Claude 3.5 Sonnet, Claude 3 Opus/Sonnet/Haiku)
- Google (Gemini Pro, Gemini Flash)
- Groq
- Azure OpenAI

### Integration Partners
- LangGraph
- LangChain
- CrewAI
- Microsoft Autogen
- NVIDIA NeMo
- LiveKit (voice)

## License

Graphiti is open-source. Zep offers both open-source and commercial licensing options.

---

**Note**: This skill provides comprehensive guidance for building AI agents with temporal knowledge graphs using Graphiti and Zep. Always ensure proper data handling, privacy compliance, and security measures for production applications.
