---
name: agno
description: Comprehensive skill for building, deploying, and managing multi-agent AI systems with Agno framework
---

# Agno AI Framework Skill

Expert assistance for building production-ready multi-agent AI systems using Agno - an incredibly fast multi-agent framework with runtime and control plane.

## When to Use This Skill

This skill should be used when:
- Building AI agents or multi-agent systems
- Implementing RAG (Retrieval-Augmented Generation) solutions
- Creating autonomous AI workflows and pipelines
- Deploying agents to production with AgentOS
- Working with LLM-powered applications
- Questions about Agno framework, agents, teams, or workflows
- Implementing tools, memory, knowledge bases, or storage for agents
- Integrating with various LLM providers (Anthropic, OpenAI, Google, etc.)
- Debugging or optimizing Agno-based applications
- Setting up production deployment with authentication and monitoring

## Overview

**Agno** is an open-source framework for building, deploying, and managing multi-agent AI systems that emphasizes:
- **Performance**: 529× faster than LangGraph, 57× faster than PydanticAI
- **Production-Ready**: Complete runtime (AgentOS) and control plane for deployment
- **Security-First**: Runs entirely in your cloud infrastructure
- **Model-Agnostic**: Supports all major LLM providers (OpenAI, Anthropic, Google, etc.)

## Core Components

### 1. **Agents** - AI programs where the language model controls execution flow

```python
from agno.agent import Agent
from agno.models.anthropic import Claude

agent = Agent(
    id="my-agent",
    model=Claude(id="claude-sonnet-4"),
    instructions="You are a helpful assistant.",
    markdown=True,
)

# Run synchronously
agent.run("Hello, how can you help?")

# Run asynchronously
await agent.arun("Hello, how can you help?")
```

**Key Agent Features:**
- **Tools**: Enable agents to take actions and interact with external systems
- **Memory**: Store and recall information from previous interactions
- **Knowledge**: Vector database integration for RAG patterns
- **Storage**: Save session history and state in a database
- **Reasoning**: Analyze action results before responding

### 2. **Teams** - Collections of agents working together

```python
from agno.team import Team

team = Team(
    id="research-team",
    agents=[researcher, writer, editor],
    instructions="Collaborate to create research articles.",
)

# Agents can delegate work to each other
team.run("Research AI trends and write an article")
```

### 3. **Workflows** - Orchestrated sequences of agents and logic

```python
from agno.workflow import Workflow, RunResponse

workflow = Workflow(
    id="content-workflow",
    steps=[
        {"agent": researcher, "message": "Research topic"},
        {"agent": writer, "message": "Write draft"},
        {"agent": editor, "message": "Edit and polish"},
    ]
)

workflow.run("Create content about AI agents")
```

### 4. **AgentOS** - Production runtime for deployment

```python
from agno.os import AgentOS
from agno.db.postgres import PostgresDb

# Setup database
db = PostgresDb(
    id="production-db",
    db_url="postgresql+psycopg://user:pass@localhost:5432/agno"
)

# Create AgentOS instance
agent_os = AgentOS(
    description="Production Multi-Agent System",
    agents=[agent1, agent2],
    teams=[team1],
    workflows=[workflow1],
    db=db,
)

# Get FastAPI app
app = agent_os.get_app()

# Serve with uvicorn
if __name__ == "__main__":
    agent_os.serve(app="main:app", reload=True, port=7777)
```

## Quick Start Guide

### Installation

```bash
pip install agno
```

### Create Your First Agent

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.duckduckgo import DuckDuckGoTools

# Create an agent with web search capability
agent = Agent(
    id="web-search-agent",
    model=Claude(id="claude-sonnet-4"),
    tools=[DuckDuckGoTools()],
    instructions="Search the web and provide accurate information.",
    show_tool_calls=True,
    markdown=True,
)

# Run the agent
response = agent.run("What are the latest AI trends?")
print(response.content)
```

### Add Memory and Storage

```python
from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.memory import AgentMemory

# Setup database for persistence
db = PostgresDb(
    id="agent-db",
    db_url="postgresql+psycopg://ai:ai@localhost:5532/ai"
)

# Create agent with memory
agent = Agent(
    id="memory-agent",
    model=Claude(id="claude-sonnet-4"),
    db=db,
    memory=AgentMemory(create_user_memories=True),
    storage={"messages": True, "sessions": True},
    instructions="Remember user preferences and context.",
)

# Conversations persist across sessions
agent.run("My name is John", session_id="session_123")
agent.run("What's my name?", session_id="session_123")  # Remembers "John"
```

### Build a RAG Agent with Knowledge

```python
from agno.agent import Agent
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.pgvector import PgVector

# Setup vector database
vector_db = PgVector(
    db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    table_name="agno_knowledge"
)

# Create knowledge base from PDFs
knowledge = PDFKnowledgeBase(
    path="docs/",
    vector_db=vector_db,
)

# Load documents into vector database
knowledge.load(recreate=False)

# Create RAG agent
rag_agent = Agent(
    id="rag-agent",
    model=Claude(id="claude-sonnet-4"),
    knowledge=knowledge,
    search_knowledge=True,
    instructions="Answer questions using the knowledge base. Cite sources.",
)

# Agent searches knowledge base before responding
rag_agent.run("What does our documentation say about agents?")
```

## Common Patterns

### 1. Structured Output with Pydantic

```python
from pydantic import BaseModel, Field
from agno.agent import Agent

class MovieReview(BaseModel):
    title: str = Field(..., description="Movie title")
    rating: float = Field(..., ge=0, le=10)
    summary: str = Field(..., description="Brief summary")
    pros: list[str]
    cons: list[str]

agent = Agent(
    model=Claude(id="claude-sonnet-4"),
    output_model=MovieReview,
    structured_output=True,
)

response = agent.run("Review the movie Inception")
review: MovieReview = response.output  # Type-safe structured output
```

### 2. Human-in-the-Loop (HITL)

```python
from agno.agent import Agent
from agno.tools import tool

@tool
def execute_trade(stock: str, amount: int) -> str:
    """Execute a stock trade (requires approval)."""
    return f"Executed trade: {amount} shares of {stock}"

agent = Agent(
    model=Claude(id="claude-sonnet-4"),
    tools=[execute_trade],
    require_approval_for_tools=True,  # Requires human approval
)

# Agent will pause and wait for approval before executing trade
agent.run("Buy 100 shares of AAPL")
```

### 3. Multi-Agent Collaboration

```python
from agno.team import Team

# Define specialized agents
researcher = Agent(
    id="researcher",
    role="Research specialist",
    tools=[DuckDuckGoTools()],
    instructions="Find accurate information on topics.",
)

writer = Agent(
    id="writer",
    role="Content writer",
    instructions="Write engaging, well-structured content.",
)

editor = Agent(
    id="editor",
    role="Editor",
    instructions="Review and improve content quality.",
)

# Create team
content_team = Team(
    id="content-team",
    agents=[researcher, writer, editor],
    leader=researcher,  # Lead agent coordinates
    instructions="""
    1. Researcher finds information
    2. Writer creates content
    3. Editor reviews and finalizes
    """,
)

# Team collaborates automatically
content_team.run("Create an article about quantum computing")
```

### 4. Context Injection and Dependencies

```python
# Pass dynamic context to agents
agent.run(
    "Write a story about {character}",
    dependencies={"character": "a brave robot named Anna"}
)

# Pass runtime metadata
agent.run(
    "Generate report",
    metadata={"user_id": "123", "department": "engineering"}
)

# Manage session state
agent.run(
    "Continue our conversation",
    session_id="user_123",
    session_state={"preferences": {"theme": "dark"}}
)
```

### 5. Streaming Responses

```python
# Stream agent responses
for chunk in agent.run_stream("Tell me a story"):
    if chunk.content:
        print(chunk.content, end="", flush=True)

# Async streaming
async for chunk in agent.arun_stream("Tell me a story"):
    if chunk.content:
        print(chunk.content, end="", flush=True)
```

## AgentOS API Deployment

### Run Agents via REST API

```bash
# Start AgentOS server
python main.py

# Run agent via API
curl --location 'http://localhost:7777/agents/my-agent/runs' \
    --header 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode 'message=Tell me about Agno' \
    --data-urlencode 'stream=True' \
    --data-urlencode 'user_id=user@example.com' \
    --data-urlencode 'session_id=session_123'

# Pass dependencies via API
curl --location 'http://localhost:7777/agents/my-agent/runs' \
    --data-urlencode 'message=Write a story' \
    --data-urlencode 'dependencies={"character_name": "Anna"}'

# Pass structured output schema
curl --location 'http://localhost:7777/agents/my-agent/runs' \
    --data-urlencode 'message=Generate data' \
    --data-urlencode 'output_schema={"type":"object","properties":{"name":{"type":"string"}}}'
```

### Authentication

```python
# Secure AgentOS with API keys
agent_os = AgentOS(
    agents=[agent],
    security_key="your-secret-key",
)

# Client requests
curl --location 'http://localhost:7777/agents/my-agent/runs' \
    --header 'Authorization: Bearer your-secret-key' \
    --data-urlencode 'message=Hello'
```

## Advanced Features

### Hooks and Background Tasks

```python
from agno.hooks import hook

# Pre-run hook
@hook
def validate_input(run_input, agent):
    """Validate input before agent runs."""
    if "forbidden" in run_input.message:
        raise ValueError("Forbidden content detected")
    return run_input

# Post-run hook (background)
@hook(run_in_background=True)
async def log_response(run_output, agent):
    """Log responses without blocking."""
    await analytics_service.log(run_output)

agent = Agent(
    model=Claude(id="claude-sonnet-4"),
    pre_run_hooks=[validate_input],
    post_run_hooks=[log_response],
)

# Enable background hooks globally in AgentOS
agent_os = AgentOS(
    agents=[agent],
    run_hooks_in_background=True,
)
```

### Reasoning and Model Controls

```python
# Enable reasoning
agent = Agent(
    model=Claude(id="claude-sonnet-4"),
    reasoning=True,  # Agent thinks before responding
    instructions="Think carefully about each question.",
)

# Control model parameters
agent = Agent(
    model=Claude(
        id="claude-sonnet-4",
        temperature=0.7,
        max_tokens=2000,
    ),
)
```

### Context Management

```python
# Automatic context compression
agent = Agent(
    model=Claude(id="claude-sonnet-4"),
    compress_context=True,  # Automatically compress long contexts
    max_context_length=100000,
)
```

## Model Provider Support

Agno supports all major LLM providers:

```python
# Anthropic Claude
from agno.models.anthropic import Claude
model = Claude(id="claude-sonnet-4")

# OpenAI
from agno.models.openai import OpenAIChat
model = OpenAIChat(id="gpt-4o")

# Google Gemini
from agno.models.google import Gemini
model = Gemini(id="gemini-2.0-flash-exp")

# AWS Bedrock
from agno.models.bedrock import Bedrock
model = Bedrock(id="anthropic.claude-3-5-sonnet-20241022-v2:0")

# Azure OpenAI
from agno.models.azure import AzureOpenAIChat
model = AzureOpenAIChat(id="gpt-4o")
```

## Built-in Tools and Integrations

Agno includes 100+ pre-built tool integrations:

```python
# Web Search
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.tavily import TavilyTools

# File Operations
from agno.tools.file import FileTools

# APIs
from agno.tools.github import GitHubTools
from agno.tools.slack import SlackTools

# Data Analysis
from agno.tools.pandas import PandasTools
from agno.tools.sql import SQLTools

# Web Scraping
from agno.tools.newspaper import NewspaperToolkit
from agno.tools.beautifulsoup import BeautifulSoupTools

# And many more...
```

### Create Custom Tools

```python
from agno.tools import tool

@tool
def calculate_roi(investment: float, return_value: float) -> dict:
    """
    Calculate return on investment.

    Args:
        investment: Initial investment amount
        return_value: Final return value

    Returns:
        Dictionary with ROI percentage and profit
    """
    profit = return_value - investment
    roi_percentage = (profit / investment) * 100

    return {
        "profit": profit,
        "roi_percentage": roi_percentage,
        "investment": investment,
        "return": return_value,
    }

# Use in agent
agent = Agent(
    model=Claude(id="claude-sonnet-4"),
    tools=[calculate_roi],
    show_tool_calls=True,
)
```

## Best Practices

### 1. **Use Structured Instructions**

```python
agent = Agent(
    instructions="""
    You are a customer support agent. Follow these rules:
    1. Always greet users warmly
    2. Ask clarifying questions if needed
    3. Provide step-by-step solutions
    4. Verify customer satisfaction before closing
    5. Escalate complex issues to human agents
    """,
)
```

### 2. **Implement Proper Error Handling**

```python
try:
    response = agent.run(user_input)
except Exception as e:
    logger.error(f"Agent error: {e}")
    # Implement fallback logic
```

### 3. **Use Session Management**

```python
# Maintain conversation context
agent.run(message, session_id=f"user_{user_id}")
```

### 4. **Monitor and Evaluate**

```python
# Use hooks for monitoring
@hook
def track_usage(run_output, agent):
    """Track agent usage and performance."""
    metrics.record({
        "agent_id": agent.id,
        "response_time": run_output.metrics.time_to_first_token,
        "tokens_used": run_output.metrics.output_tokens,
    })
```

### 5. **Optimize for Production**

```python
# Use database for persistence
db = PostgresDb(db_url=os.getenv("DATABASE_URL"))

# Enable caching
agent = Agent(
    db=db,
    storage={"messages": True, "sessions": True},
)

# Deploy with AgentOS
agent_os = AgentOS(
    agents=[agent],
    db=db,
    security_key=os.getenv("API_SECRET_KEY"),
)
```

## Performance Benchmarks

Agno is optimized for production use:

- **Agent instantiation**: ~3 microseconds
- **Memory per agent**: ~6.6 KiB
- **Throughput**: 529× faster than LangGraph, 57× faster than PydanticAI

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **llms-full.md** - Complete Agno documentation (4.8MB)
- **llms-txt.md** - Condensed documentation (3.1MB)
- **llms.md** - Quick reference (203KB)
- **index.md** - Documentation index

## Use Cases and Examples

### 1. **Documentation Assistant (RAG)**
Build an AI assistant that answers questions from your knowledge base using vector search.

### 2. **Competitor Analysis**
Automated competitive intelligence through web search and content analysis.

### 3. **Research Agent**
Create research articles with web search, fact-checking, and writing capabilities.

### 4. **Web Data Extraction**
Transform unstructured web content into organized, structured data.

### 5. **Content Generation Pipeline**
Multi-agent workflow for researching, writing, and editing content.

## Common Issues and Solutions

### Issue: Agent not using tools
**Solution**: Ensure `show_tool_calls=True` and verify tool descriptions are clear.

### Issue: Context too long
**Solution**: Enable `compress_context=True` or implement context summarization.

### Issue: Slow responses
**Solution**: Use streaming (`run_stream()`) and optimize tool execution.

### Issue: Lost conversation context
**Solution**: Implement proper session management with `session_id` and database storage.

## Resources

- **Documentation**: https://docs.agno.com
- **GitHub**: https://github.com/agno-agi/agno
- **Community**: https://community.agno.com
- **Discord**: Join the Agno Discord community
- **Examples**: https://github.com/agno-agi/agno/tree/main/cookbook

## License

Apache-2.0

---

**Note**: This skill was generated from official Agno documentation. For the most up-to-date information, always refer to the official docs at https://docs.agno.com
