---
name: mcp
description: Comprehensive skill for Model Context Protocol (MCP) - building servers and clients for LLM context integration
---

# Model Context Protocol (MCP) Skill

Expert assistance for building MCP servers and clients to extend LLM capabilities with custom context, tools, and resources using the standardized Model Context Protocol.

## When to Use This Skill

This skill should be used when:
- Building MCP servers to expose tools, resources, or prompts to LLMs
- Creating MCP clients to integrate with Claude or other LLM applications
- Extending Claude Desktop with custom functionality
- Implementing standardized LLM context protocols
- Developing plugins for AI applications
- Creating reusable AI tool integrations
- Building enterprise AI integrations with security
- Implementing OAuth 2.1 authorization for MCP
- Debugging MCP servers with the Inspector tool
- Questions about MCP architecture and best practices
- Integrating external APIs with LLMs
- Building knowledge bases accessible to AI assistants

## Overview

### What is MCP?

**Model Context Protocol (MCP)** is a standardized protocol that enables:
- LLMs to access external tools and data sources
- Bidirectional communication between AI applications and integrations
- Unified interface for context providers
- Secure, scalable AI integrations

**Core Value:**
> "MCP standardizes how LLMs access context, enabling reusable integrations across applications."

### MCP Architecture

```
┌─────────────────┐
│   LLM Client    │  (Claude Desktop, Custom Client)
│  (MCP Client)   │
└────────┬────────┘
         │ MCP Protocol
         │ (JSON-RPC)
┌────────▼────────┐
│   MCP Server    │  (Your Integration)
└────────┬────────┘
         │
┌────────▼────────┐
│  External APIs  │  (Database, APIs, Files)
│  & Data Sources │
└─────────────────┘
```

### Core Concepts

**1. Resources**: File-like data readable by clients
- Similar to GET endpoints
- Provide information without side effects
- Examples: file contents, API responses, database records

**2. Tools**: Functions callable by LLMs
- Similar to POST endpoints
- Execute code and produce side effects
- Require user approval
- Examples: send email, create file, call API

**3. Prompts**: Pre-written templates
- Reusable interaction patterns
- Consistent user-model interactions
- Examples: code review template, data analysis prompt

## Installation

### Python SDK

```bash
# Using uv (recommended)
uv add "mcp[cli]"

# Or using pip
pip install "mcp[cli]"

# For development
pip install "mcp[cli,dev]"
```

**Requirements:**
- Python 3.10+
- MCP SDK 1.2.0+

### TypeScript SDK

```bash
# Install SDK and Zod (peer dependency)
npm install @modelcontextprotocol/sdk zod

# For TypeScript projects
npm install --save-dev typescript @types/node
```

**Requirements:**
- Node.js 16+
- Zod v3.25+

### MCP Inspector

```bash
# No installation needed - run with npx
npx @modelcontextprotocol/inspector <command>
```

## Building MCP Servers

### Python Server (FastMCP)

**Basic Structure:**

```python
from mcp import FastMCP

# Create MCP server
mcp = FastMCP("my-server")

# Define a resource
@mcp.resource("file://readme")
def get_readme() -> str:
    """Provide README contents"""
    with open("README.md") as f:
        return f.read()

# Define a tool
@mcp.tool()
async def add_numbers(a: int, b: int) -> int:
    """Add two numbers together
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        Sum of a and b
    """
    return a + b

# Define a prompt
@mcp.prompt()
def code_review_prompt(language: str = "python") -> list[dict]:
    """Generate code review prompt"""
    return [
        {
            "role": "user",
            "content": f"Review this {language} code for best practices"
        }
    ]
```

**Run Server:**

```bash
# Development
uv run mcp dev my_server.py

# Production with stdio
python -m mcp.server.stdio my_server:mcp

# Production with HTTP
python -m mcp.server.sse my_server:mcp --port 8000
```

### TypeScript Server

**Basic Structure:**

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new Server(
  {
    name: "my-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      resources: {},
      tools: {},
      prompts: {},
    },
  }
);

// Register a tool
server.setRequestHandler(
  "tools/list",
  async () => ({
    tools: [
      {
        name: "add_numbers",
        description: "Add two numbers",
        inputSchema: z.object({
          a: z.number().describe("First number"),
          b: z.number().describe("Second number"),
        }),
      },
    ],
  })
);

server.setRequestHandler(
  "tools/call",
  async (request) => {
    if (request.params.name === "add_numbers") {
      const { a, b } = request.params.arguments;
      return {
        content: [
          {
            type: "text",
            text: String(a + b),
          },
        ],
      };
    }
    throw new Error("Unknown tool");
  }
);

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

**Build and Run:**

```bash
# Build
npm run build

# Run
node build/index.js
```

### Critical Best Practices

**⚠️ NEVER write to stdout in STDIO servers!**

```python
# ❌ BAD - Breaks JSON-RPC
print("Debug message")

# ✅ GOOD - Use stderr or logging
import logging
logging.basicConfig(level=logging.INFO, handlers=[
    logging.FileHandler('server.log')
])
logger = logging.getLogger(__name__)
logger.info("Debug message")

# Or use stderr directly
import sys
print("Debug message", file=sys.stderr)
```

```typescript
// ❌ BAD
console.log("Debug message");

// ✅ GOOD
console.error("Debug message");

// Or use a logging library
import winston from 'winston';
const logger = winston.createLogger({
  transports: [new winston.transports.File({ filename: 'server.log' })]
});
logger.info("Debug message");
```

## Building MCP Clients

### Python Client

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from anthropic import Anthropic
import asyncio

class MCPClient:
    def __init__(self):
        self.anthropic = Anthropic()
        self.session = None
        
    async def connect_to_server(self, server_script_path: str):
        """Connect to MCP server"""
        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path],
            env=None
        )
        
        stdio_transport = await stdio_client(server_params)
        self.stdio, self.write = stdio_transport
        self.session = ClientSession(self.stdio, self.write)
        
        await self.session.__aenter__()
        await self.session.initialize()
        
    async def list_tools(self):
        """Get available tools from server"""
        response = await self.session.list_tools()
        return response.tools
    
    async def process_query(self, query: str):
        """Process user query with Claude"""
        tools = await self.list_tools()
        
        # Format tools for Claude
        claude_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            }
            for tool in tools
        ]
        
        messages = [{"role": "user", "content": query}]
        
        while True:
            response = self.anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                tools=claude_tools,
                messages=messages
            )
            
            if response.stop_reason != "tool_use":
                # Final answer
                return response.content[0].text
            
            # Process tool calls
            for content in response.content:
                if content.type == "tool_use":
                    result = await self.session.call_tool(
                        content.name,
                        content.input
                    )
                    
                    messages.append({
                        "role": "assistant",
                        "content": response.content
                    })
                    messages.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": result.content
                        }]
                    })

async def main():
    client = MCPClient()
    await client.connect_to_server("server.py")
    
    result = await client.process_query("Add 5 and 3")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### TypeScript Client

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import Anthropic from "@anthropic-ai/sdk";

const transport = new StdioClientTransport({
  command: "python",
  args: ["server.py"],
});

const client = new Client(
  {
    name: "my-client",
    version: "1.0.0",
  },
  {
    capabilities: {},
  }
);

await client.connect(transport);

// List tools
const toolsResponse = await client.listTools();
const tools = toolsResponse.tools.map(tool => ({
  name: tool.name,
  description: tool.description,
  input_schema: tool.inputSchema,
}));

// Use with Claude
const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const messages = [
  { role: "user" as const, content: "Add 5 and 3" }
];

while (true) {
  const response = await anthropic.messages.create({
    model: "claude-3-5-sonnet-20241022",
    max_tokens: 4096,
    tools,
    messages,
  });

  if (response.stop_reason !== "tool_use") {
    console.log(response.content[0].text);
    break;
  }

  // Handle tool calls
  for (const content of response.content) {
    if (content.type === "tool_use") {
      const result = await client.callTool({
        name: content.name,
        arguments: content.input,
      });

      messages.push({
        role: "assistant" as const,
        content: response.content,
      });
      messages.push({
        role: "user" as const,
        content: [{
          type: "tool_result" as const,
          tool_use_id: content.id,
          content: result.content,
        }],
      });
    }
  }
}
```

## Integration with Claude Desktop

### Configuration

Edit `claude_desktop_config.json`:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"]
    },
    "another-server": {
      "command": "node",
      "args": ["/absolute/path/to/server.js"]
    }
  }
}
```

**Important:**
- Use absolute paths only
- Fully restart Claude Desktop (not just close window)
- Check logs at `~/Library/Logs/Claude/` (macOS)

### Verification

1. Restart Claude Desktop completely
2. Start new conversation
3. Look for 🔨 icon indicating tools are available
4. Tools should appear in tool selection menu

## Security and Authorization

### OAuth 2.1 Implementation

MCP uses standardized OAuth 2.1 for authorization:

**When to Use:**
- Servers handle sensitive data
- Enterprise environments
- Multi-user systems
- Audit trail requirements

**Authorization Flow:**

```python
from mcp.server import Server
from mcp.server.auth import OAuth2Provider

# Configure OAuth provider
oauth_provider = OAuth2Provider(
    authorization_endpoint="https://auth.example.com/oauth/authorize",
    token_endpoint="https://auth.example.com/oauth/token",
    client_id="your-client-id",
    client_secret="your-client-secret",
    scopes=["read:data", "write:data"]
)

server = Server("secure-server", auth=oauth_provider)

@server.tool(required_scopes=["write:data"])
async def write_file(path: str, content: str):
    """Write file (requires write scope)"""
    # Verify token
    if not server.verify_scope("write:data"):
        raise PermissionError("Insufficient permissions")
    
    with open(path, 'w') as f:
        f.write(content)
    return "File written"
```

### Security Best Practices

```python
import os
from typing import Optional

# ✅ GOOD - Use environment variables for secrets
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable required")

# ✅ GOOD - Implement token validation
def validate_token(token: str) -> bool:
    # Use vetted library (e.g., PyJWT, authlib)
    try:
        # Verify signature, expiration, audience
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            audience="your-resource-server"
        )
        return True
    except jwt.InvalidTokenError:
        return False

# ✅ GOOD - Short-lived tokens
ACCESS_TOKEN_LIFETIME = 900  # 15 minutes

# ✅ GOOD - Least privilege scoping
TOOL_SCOPES = {
    "read_file": ["read:files"],
    "write_file": ["write:files"],
    "delete_file": ["write:files", "delete:files"]
}

# ❌ BAD - Never log credentials
# logger.info(f"Token: {token}")  # DON'T DO THIS

# ✅ GOOD - Log generic errors to clients
try:
    result = perform_action()
except Exception as e:
    logger.error(f"Action failed: {e}")  # Log details internally
    return {"error": "Operation failed"}  # Generic message to client

# ✅ GOOD - HTTPS in production
if not is_localhost() and not using_https():
    raise SecurityError("HTTPS required for production")
```

## MCP Inspector

### Running Inspector

```bash
# Inspect local server
npx @modelcontextprotocol/inspector python server.py

# Inspect with arguments
npx @modelcontextprotocol/inspector python server.py --arg value

# Inspect TypeScript server
npx @modelcontextprotocol/inspector node server.js

# Inspect from npm package
npx @modelcontextprotocol/inspector npx server-package
```

### Inspector Features

**Server Connection Panel:**
- Configure transport methods (stdio, HTTP, SSE)
- Customize command-line arguments
- Test connection status

**Resources Tab:**
- View all available resources
- Test resource subscriptions
- Preview resource content
- Check MIME types and metadata

**Prompts Tab:**
- List prompt templates
- Test with custom arguments
- Preview generated messages

**Tools Tab:**
- View tool schemas and descriptions
- Execute tools with custom inputs
- Test parameter validation
- Check response formats

**Notifications Pane:**
- Monitor server logs
- View real-time notifications
- Track errors and warnings

### Debugging Workflow

```bash
# 1. Start Inspector
npx @modelcontextprotocol/inspector python server.py

# 2. Test tool
# In Inspector UI:
# - Go to Tools tab
# - Select "add_numbers"
# - Enter: {"a": 5, "b": 3}
# - Click "Execute"
# - Verify result: 8

# 3. Make changes to server.py
# - Update tool implementation
# - Save file

# 4. Reconnect in Inspector
# - Click "Reconnect" button
# - Retest tool

# 5. Test edge cases
# - Invalid inputs: {"a": "not a number", "b": 3}
# - Missing parameters: {"a": 5}
# - Verify error handling
```

## Common Patterns

### File System Server

```python
from mcp import FastMCP
from pathlib import Path
import os

mcp = FastMCP("filesystem")

@mcp.tool()
async def read_file(path: str) -> str:
    """Read file contents
    
    Args:
        path: Path to file
    
    Returns:
        File contents
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    return file_path.read_text()

@mcp.tool()
async def write_file(path: str, content: str) -> str:
    """Write content to file
    
    Args:
        path: Path to file
        content: Content to write
    
    Returns:
        Success message
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)
    return f"Wrote {len(content)} bytes to {path}"

@mcp.tool()
async def list_directory(path: str) -> list[str]:
    """List directory contents
    
    Args:
        path: Directory path
    
    Returns:
        List of filenames
    """
    dir_path = Path(path)
    if not dir_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {path}")
    
    return [item.name for item in dir_path.iterdir()]
```

### API Integration Server

```python
from mcp import FastMCP
import httpx
import os

mcp = FastMCP("api-server")

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.example.com"

@mcp.tool()
async def search_api(query: str, limit: int = 10) -> dict:
    """Search API
    
    Args:
        query: Search query
        limit: Maximum results
    
    Returns:
        Search results
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/search",
            params={"q": query, "limit": limit},
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        response.raise_for_status()
        return response.json()

@mcp.resource("api://status")
async def api_status() -> dict:
    """Get API status"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/status")
        return response.json()
```

### Database Server

```python
from mcp import FastMCP
import sqlite3
from typing import List, Dict

mcp = FastMCP("database")

DB_PATH = "data.db"

@mcp.tool()
async def query_database(sql: str) -> List[Dict]:
    """Execute SQL query
    
    Args:
        sql: SQL query (SELECT only)
    
    Returns:
        Query results
    """
    if not sql.strip().upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries allowed")
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql)
        results = [dict(row) for row in cursor.fetchall()]
        return results
    finally:
        conn.close()

@mcp.tool()
async def insert_record(table: str, data: dict) -> str:
    """Insert record into table
    
    Args:
        table: Table name
        data: Column-value pairs
    
    Returns:
        Success message
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?" for _ in data])
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    
    try:
        cursor.execute(sql, list(data.values()))
        conn.commit()
        return f"Inserted record into {table}"
    finally:
        conn.close()
```

## Advanced Features

### Structured Output

```python
from mcp import FastMCP
from pydantic import BaseModel
from typing import List

mcp = FastMCP("structured-server")

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    score: float

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total: int

@mcp.tool()
async def search(query: str) -> SearchResponse:
    """Search with structured output"""
    # Perform search
    results = [
        SearchResult(
            title="Result 1",
            url="https://example.com/1",
            snippet="First result",
            score=0.95
        ),
        SearchResult(
            title="Result 2",
            url="https://example.com/2",
            snippet="Second result",
            score=0.87
        )
    ]
    
    return SearchResponse(
        query=query,
        results=results,
        total=len(results)
    )
```

### Context and Progress

```python
from mcp import FastMCP, Context
import asyncio

mcp = FastMCP("progress-server")

@mcp.tool()
async def long_running_task(ctx: Context, iterations: int) -> str:
    """Long running task with progress
    
    Args:
        ctx: MCP context (auto-injected)
        iterations: Number of iterations
    
    Returns:
        Completion message
    """
    for i in range(iterations):
        # Report progress
        await ctx.report_progress(
            progress=i,
            total=iterations,
            message=f"Processing {i}/{iterations}"
        )
        
        # Log
        ctx.logger.info(f"Iteration {i}")
        
        # Simulate work
        await asyncio.sleep(0.1)
    
    return f"Completed {iterations} iterations"
```

### Lifespan Management

```python
from mcp import FastMCP
from contextlib import asynccontextmanager
import httpx

@asynccontextmanager
async def lifespan(app):
    # Startup
    print("Starting server...")
    app.http_client = httpx.AsyncClient()
    
    yield
    
    # Shutdown
    print("Shutting down server...")
    await app.http_client.aclose()

mcp = FastMCP("lifecycle-server", lifespan=lifespan)

@mcp.tool()
async def fetch_url(ctx: Context, url: str) -> str:
    """Fetch URL using shared HTTP client
    
    Args:
        ctx: MCP context
        url: URL to fetch
    
    Returns:
        Response text
    """
    # Access lifespan context
    http_client = ctx.lifespan.http_client
    response = await http_client.get(url)
    return response.text
```

## Transport Options

### STDIO (Standard Input/Output)

**Best For:** Claude Desktop integration, CLI tools

```python
# Python
python -m mcp.server.stdio server:mcp

# TypeScript
node build/index.js
```

### SSE (Server-Sent Events)

**Best For:** Web applications, HTTP-based clients

```python
# Python
python -m mcp.server.sse server:mcp --port 8000

# With CORS
python -m mcp.server.sse server:mcp --port 8000 --cors-origin "*"
```

```typescript
// TypeScript
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";

const transport = new SSEServerTransport("/sse", res);
await server.connect(transport);
```

### HTTP (Streamable)

**Best For:** Modern web applications, recommended

```python
# Python
mcp = FastMCP("server", streamable_http=True)

# Run on port 8000
# Server automatically available at http://localhost:8000
```

```typescript
// TypeScript
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/http.js";

const transport = new StreamableHTTPServerTransport({
  endpoint: "/mcp",
});
await server.connect(transport);
```

## Troubleshooting

### Common Issues

**Server not appearing in Claude Desktop:**
```bash
# Check configuration path is correct
# macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
# Windows: %APPDATA%\Claude\claude_desktop_config.json

# Verify JSON syntax
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | python -m json.tool

# Check logs
tail -f ~/Library/Logs/Claude/mcp*.log

# Fully restart Claude Desktop
# - Quit application (not just close window)
# - Kill process if needed: killall Claude
# - Restart application
```

**STDIO Communication Broken:**
```python
# ❌ DON'T write to stdout
print("Debug message")  # Breaks JSON-RPC

# ✅ Use stderr or file logging
import logging
logging.basicConfig(
    level=logging.DEBUG,
    filename='server.log',
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

**Tool Not Executing:**
```python
# Check tool schema matches Claude's expectations
@mcp.tool()
async def my_tool(
    param1: str,  # Required parameter
    param2: int = 10  # Optional with default
) -> str:
    """Tool description must be clear
    
    Args:
        param1: First parameter description
        param2: Second parameter description (optional)
    
    Returns:
        What this tool returns
    """
    pass
```

**Connection Timeout:**
```python
# Increase timeouts for slow operations
import httpx

async with httpx.AsyncClient(timeout=30.0) as client:
    response = await client.get(url)
```

## Best Practices

### 1. Clear Documentation

```python
@mcp.tool()
async def process_data(
    data: str,
    format: str = "json",
    validate: bool = True
) -> dict:
    """Process and validate data
    
    This tool processes input data and optionally validates it
    against a schema before returning the processed result.
    
    Args:
        data: Raw input data to process
        format: Output format (json, xml, csv)
        validate: Whether to validate against schema
    
    Returns:
        Processed data with metadata
        
    Raises:
        ValueError: If data format is invalid
        ValidationError: If validation fails
    
    Examples:
        >>> process_data('{"key": "value"}', format="json")
        {"processed": true, "data": {...}}
    """
    pass
```

### 2. Error Handling

```python
@mcp.tool()
async def safe_operation(path: str) -> str:
    """Safe operation with proper error handling"""
    try:
        # Validate input
        if not path:
            raise ValueError("Path cannot be empty")
        
        # Perform operation
        result = perform_operation(path)
        
        # Return success
        return f"Success: {result}"
        
    except FileNotFoundError:
        return "Error: File not found"
    except PermissionError:
        return "Error: Permission denied"
    except Exception as e:
        # Log detailed error internally
        logger.error(f"Operation failed: {e}", exc_info=True)
        # Return generic error to user
        return "Error: Operation failed"
```

### 3. Input Validation

```python
from pydantic import BaseModel, Field, validator

class FileOperation(BaseModel):
    path: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., max_length=1000000)
    
    @validator('path')
    def validate_path(cls, v):
        # Prevent directory traversal
        if '..' in v or v.startswith('/'):
            raise ValueError("Invalid path")
        return v

@mcp.tool()
async def write_validated(operation: FileOperation) -> str:
    """Write file with validated input"""
    # Input automatically validated by Pydantic
    return write_file(operation.path, operation.content)
```

### 4. Testing

```python
import pytest
from mcp.testing import MCPTestClient

@pytest.mark.asyncio
async def test_add_numbers():
    """Test add_numbers tool"""
    async with MCPTestClient(mcp) as client:
        # List tools
        tools = await client.list_tools()
        assert "add_numbers" in [t.name for t in tools.tools]
        
        # Call tool
        result = await client.call_tool(
            "add_numbers",
            {"a": 5, "b": 3}
        )
        assert result.content[0].text == "8"
```

## Resources

### Official Documentation
- **Main Site**: https://modelcontextprotocol.io/
- **Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **TypeScript SDK**: https://github.com/modelcontextprotocol/typescript-sdk
- **Specification**: https://spec.modelcontextprotocol.io/

### Tools
- **MCP Inspector**: Debug and test servers interactively
- **Claude Desktop**: Reference implementation client

### Community
- **GitHub Discussions**: https://github.com/modelcontextprotocol/discussions
- **Examples**: https://github.com/modelcontextprotocol/servers

## License

MCP SDKs are licensed under MIT.

---

**Note**: This skill provides comprehensive guidance for building MCP servers and clients. Always follow security best practices and test thoroughly before production deployment.
