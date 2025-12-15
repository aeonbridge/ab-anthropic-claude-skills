---
name: graphrag
description: Comprehensive skill for Microsoft GraphRAG - modular graph-based RAG system for reasoning over private datasets
version: 1.0.0
---

# Microsoft GraphRAG Skill

Expert assistance for using Microsoft GraphRAG, a modular graph-based Retrieval-Augmented Generation system that extracts structured knowledge from unstructured text to enhance LLM reasoning over private data.

## When to Use This Skill

This skill should be used when:
- Building RAG systems that need to "connect the dots" across dispersed information
- Querying large document collections holistically
- Extracting structured knowledge graphs from unstructured text
- Implementing graph-based retrieval for LLM applications
- Processing private datasets with enhanced reasoning capabilities
- Working with narrative, unstructured documents
- Building question-answering systems over document corpora
- Extracting entities, relationships, and claims from text
- Creating hierarchical knowledge summaries
- Implementing multi-hop reasoning over documents
- Comparing GraphRAG with traditional vector-based RAG
- Tuning prompts for domain-specific datasets
- Configuring indexing pipelines for knowledge extraction

## Overview

### What is GraphRAG?

**Microsoft GraphRAG** is a data pipeline and transformation system that:
- Extracts meaningful, structured data from unstructured text using LLMs
- Builds knowledge graph memory structures
- Enhances LLM outputs through graph-based retrieval
- Supports private data processing without external exposure

**Core Innovation:**
> "GraphRAG addresses fundamental limitations of baseline RAG: connecting the dots across disparate information pieces and holistically understanding summarized concepts over large collections."

### Key Differentiators from Baseline RAG

Traditional vector-based RAG has limitations:
- ❌ Struggles to connect information across multiple documents
- ❌ Limited holistic understanding of document collections
- ❌ Misses relationships between dispersed facts
- ❌ Poor performance on "summarize the corpus" queries

GraphRAG solves these with:
- ✅ Knowledge graph extraction from text
- ✅ Hierarchical community detection
- ✅ Multi-level summarization
- ✅ Graph-based reasoning and traversal
- ✅ Better performance on complex queries

## Core Concepts

### 1. Knowledge Graph Extraction

GraphRAG extracts three primary elements:

**Entities**: Objects, people, places, concepts
```
Examples:
- "Microsoft" (Organization)
- "Seattle" (Location)
- "Cloud Computing" (Concept)
- "Satya Nadella" (Person)
```

**Relationships**: Connections between entities
```
Examples:
- Microsoft → headquartered_in → Seattle
- Satya Nadella → is_CEO_of → Microsoft
- Microsoft → provides → Cloud Computing
```

**Claims**: Factual statements with supporting evidence
```
Examples:
- "Microsoft is the largest software company" [Source: Document X, Page 5]
- "Azure revenue grew 30% in Q4" [Source: Earnings Report]
```

### 2. Hierarchical Community Detection

GraphRAG uses the **Leiden algorithm** to:
- Cluster related entities into communities
- Create hierarchical levels of organization
- Generate summaries at each level
- Enable bottom-up reasoning

**Example Hierarchy:**
```
Level 0 (Detailed):
  Community 1: Azure services (Compute, Storage, Networking)
  Community 2: Office products (Word, Excel, PowerPoint)

Level 1 (Mid-level):
  Community A: Cloud services (includes Community 1)
  Community B: Productivity tools (includes Community 2)

Level 2 (High-level):
  Community X: Microsoft product ecosystem (includes A & B)
```

### 3. TextUnits

Documents are segmented into **TextUnits**:
- Manageable chunks for analysis
- Sized based on token limits
- Overlapping to preserve context
- Form the basis of entity extraction

### 4. Query Modes

GraphRAG offers multiple search strategies:

**Global Search**: Holistic corpus reasoning
- Best for: "Summarize the main themes"
- Uses: Community summaries at all levels
- Method: Bottom-up aggregation

**Local Search**: Entity-specific reasoning
- Best for: "Tell me about Entity X"
- Uses: Entity neighborhoods in graph
- Method: Traversal from seed entities

**DRIFT Search**: Entity reasoning with community context
- Best for: "How does X relate to broader themes?"
- Uses: Entities + community summaries
- Method: Hybrid approach

**Basic Search**: Traditional vector similarity
- Best for: Simple semantic matching
- Uses: Embedding similarity
- Method: Baseline RAG fallback

## Installation

### Prerequisites

```bash
# Python 3.10 or higher required
python --version

# Install GraphRAG
pip install graphrag

# Or install from source
git clone https://github.com/microsoft/graphrag.git
cd graphrag
pip install -e .
```

### Environment Setup

```bash
# Create environment file
cat > .env << EOF
# LLM Configuration (OpenAI)
GRAPHRAG_LLM_API_KEY=your-openai-api-key
GRAPHRAG_LLM_TYPE=openai_chat
GRAPHRAG_LLM_MODEL=gpt-4o

# Embedding Configuration
GRAPHRAG_EMBEDDING_API_KEY=your-openai-api-key
GRAPHRAG_EMBEDDING_TYPE=openai_embedding
GRAPHRAG_EMBEDDING_MODEL=text-embedding-3-small

# Optional: Azure OpenAI
# GRAPHRAG_LLM_API_BASE=https://your-resource.openai.azure.com
# GRAPHRAG_LLM_API_VERSION=2024-02-15-preview
# GRAPHRAG_LLM_DEPLOYMENT_NAME=gpt-4

# Optional: Local models
# GRAPHRAG_LLM_TYPE=ollama
# GRAPHRAG_LLM_API_BASE=http://localhost:11434
EOF
```

## Quick Start

### 1. Initialize Project

```bash
# Create new GraphRAG project
mkdir my-graphrag-project
cd my-graphrag-project

# Initialize configuration
graphrag init --root .

# This creates:
# - settings.yaml (configuration)
# - .env (environment variables)
# - prompts/ (customizable prompts)
```

### 2. Prepare Your Data

```bash
# Create input directory
mkdir -p input

# Add your documents
cp /path/to/documents/*.txt input/

# Supported formats: .txt, .pdf, .docx, .md
# Each file will be processed independently
```

### 3. Run Indexing Pipeline

```bash
# Index your data (this can take time and cost money!)
graphrag index --root .

# The indexing process will:
# 1. Load and chunk documents
# 2. Extract entities, relationships, claims
# 3. Build knowledge graph
# 4. Detect communities (Leiden algorithm)
# 5. Generate community summaries
# 6. Create embeddings
# 7. Store results in output/

# Monitor progress
graphrag index --root . --verbose
```

### 4. Query Your Data

```bash
# Global Search (holistic queries)
graphrag query --root . \
  --method global \
  --query "What are the main themes in this dataset?"

# Local Search (entity-specific queries)
graphrag query --root . \
  --method local \
  --query "Tell me about Microsoft's cloud strategy"

# DRIFT Search (entity + community context)
graphrag query --root . \
  --method drift \
  --query "How does Azure relate to the broader Microsoft ecosystem?"
```

## Configuration

### settings.yaml Structure

```yaml
# Core Configuration
llm:
  api_key: ${GRAPHRAG_LLM_API_KEY}
  type: openai_chat  # or azure_openai_chat, ollama
  model: gpt-4o
  max_tokens: 4000
  temperature: 0
  top_p: 1

embeddings:
  api_key: ${GRAPHRAG_EMBEDDING_API_KEY}
  type: openai_embedding
  model: text-embedding-3-small

# Chunking Configuration
chunks:
  size: 1200          # Token size per chunk
  overlap: 100        # Overlap between chunks
  group_by_columns: [id]

# Entity Extraction
entity_extraction:
  prompt: "prompts/entity_extraction.txt"
  max_gleanings: 1    # Re-extraction passes
  entity_types: [organization, person, location, event]

# Community Detection
community_reports:
  prompt: "prompts/community_report.txt"
  max_length: 2000
  max_input_length: 8000

# Claim Extraction
claim_extraction:
  enabled: true
  prompt: "prompts/claim_extraction.txt"
  max_gleanings: 1

# Embeddings
embed_graph:
  enabled: true
  strategy: node2vec  # or deepwalk

# Storage
storage:
  type: file          # or blob, cosmosdb
  base_dir: output

# Reporting
reporting:
  type: file
  base_dir: output/reports
```

### Advanced Configuration Options

```yaml
# Custom LLM Configuration
llm:
  type: azure_openai_chat
  api_base: https://your-resource.openai.azure.com
  api_version: "2024-02-15-preview"
  deployment_name: gpt-4
  api_key: ${AZURE_OPENAI_API_KEY}
  request_timeout: 180
  max_retries: 10
  max_retry_wait: 10

# Parallelization
parallelization:
  stagger: 0.3        # Delay between requests
  num_threads: 4      # Concurrent workers

# Cache Configuration
cache:
  type: file
  base_dir: cache

# Input Configuration
input:
  type: file
  file_type: text     # or csv, parquet
  base_dir: input
  encoding: utf-8
  file_pattern: ".*\\.txt$"
```

## Prompt Tuning

### Why Tune Prompts?

> "Using GraphRAG with your data out of the box may not yield the best possible results."

Domain-specific datasets require custom prompts for:
- Relevant entity types
- Appropriate relationship types
- Domain-specific language
- Expected output format

### Auto-Tuning Process

```bash
# Generate domain-adapted prompts
graphrag prompt-tune --root . \
  --config settings.yaml \
  --output prompts/

# This will:
# 1. Analyze your input documents
# 2. Identify domain-specific patterns
# 3. Generate custom entity extraction prompts
# 4. Generate custom summarization prompts
# 5. Save to prompts/ directory
```

### Manual Prompt Customization

```bash
# Edit generated prompts
nano prompts/entity_extraction.txt
```

**Example Entity Extraction Prompt:**

```
-Target activity-
You are an AI assistant helping to identify entities in documents about {DOMAIN}.

-Goal-
Extract all entities and relationships from the text below.

Entity Types:
{ENTITY_TYPES}

Relationship Types:
{RELATIONSHIP_TYPES}

Format your response as JSON:
{{
  "entities": [
    {{"name": "Entity Name", "type": "ENTITY_TYPE", "description": "..."}}
  ],
  "relationships": [
    {{"source": "Entity 1", "target": "Entity 2", "type": "RELATIONSHIP_TYPE", "description": "..."}}
  ]
}}

Text to analyze:
{INPUT_TEXT}
```

## Indexing Pipeline Deep Dive

### Step-by-Step Process

**1. Document Loading**
```python
# Input documents are loaded from input/ directory
# Supported formats: .txt, .pdf, .docx, .md
```

**2. Text Chunking**
```python
# Documents split into TextUnits
# Default: 1200 tokens with 100 token overlap
# Preserves context across chunk boundaries
```

**3. Entity Extraction**
```python
# For each TextUnit:
#   - Extract entities (with types and descriptions)
#   - Extract relationships (with types and weights)
#   - Extract claims (with sources and confidence)
```

**4. Graph Construction**
```python
# Build knowledge graph:
#   - Nodes = Entities
#   - Edges = Relationships
#   - Properties = Attributes and metadata
```

**5. Community Detection**
```python
# Leiden algorithm for hierarchical clustering:
#   - Level 0: Fine-grained communities
#   - Level 1: Mid-level aggregations
#   - Level 2+: High-level themes
```

**6. Community Summarization**
```python
# For each community at each level:
#   - Aggregate entity and relationship info
#   - Generate natural language summary
#   - Store for query-time retrieval
```

**7. Embedding Generation**
```python
# Create vector embeddings for:
#   - TextUnits (for similarity search)
#   - Entities (for semantic matching)
#   - Community summaries (for global search)
```

**8. Output Storage**
```python
# Results saved to output/:
#   - create_final_entities.parquet
#   - create_final_relationships.parquet
#   - create_final_communities.parquet
#   - create_final_community_reports.parquet
#   - create_final_text_units.parquet
```

## Query Modes in Detail

### Global Search

**Best For:**
- "What are the main themes?"
- "Summarize the entire dataset"
- "What are the key trends?"

**How It Works:**
1. Query is matched against community summaries
2. Relevant communities selected at all hierarchy levels
3. Summaries aggregated bottom-up
4. Final answer synthesized from multiple levels

**Example:**
```bash
graphrag query --root . \
  --method global \
  --query "What are the major technology trends discussed in these documents?"

# Behind the scenes:
# 1. Match query to relevant communities
# 2. Retrieve summaries from levels 0, 1, 2
# 3. Aggregate: AI/ML, Cloud, Cybersecurity communities
# 4. Synthesize comprehensive answer
```

**Python API:**
```python
from graphrag.query import GlobalSearch

searcher = GlobalSearch(
    llm=llm,
    context_builder=context_builder,
    map_system_prompt=map_prompt,
    reduce_system_prompt=reduce_prompt
)

result = await searcher.asearch(
    query="What are the major themes?",
    conversation_history=[]
)
print(result.response)
```

### Local Search

**Best For:**
- "Tell me about [specific entity]"
- "What is the relationship between X and Y?"
- "Find information about [topic]"

**How It Works:**
1. Identify entities mentioned in query
2. Traverse graph from those entities
3. Collect neighborhood information (N-hop)
4. Retrieve associated TextUnits
5. Synthesize answer from local context

**Example:**
```bash
graphrag query --root . \
  --method local \
  --query "What is Microsoft's strategy for artificial intelligence?"

# Behind the scenes:
# 1. Identify: "Microsoft", "artificial intelligence" entities
# 2. Traverse: Find related entities (Azure AI, OpenAI partnership, etc.)
# 3. Collect: Relationships, claims, TextUnits
# 4. Synthesize: Answer from local graph neighborhood
```

**Python API:**
```python
from graphrag.query import LocalSearch

searcher = LocalSearch(
    llm=llm,
    context_builder=context_builder,
    system_prompt=system_prompt
)

result = await searcher.asearch(
    query="Tell me about Microsoft's AI strategy",
    conversation_history=[]
)
print(result.response)
```

### DRIFT Search

**Best For:**
- "How does [entity] fit into [broader context]?"
- "What is the significance of [topic]?"
- Hybrid queries needing both local and global context

**How It Works:**
1. Identify query entities (like Local Search)
2. Find relevant communities (like Global Search)
3. Combine entity neighborhoods with community summaries
4. Synthesize answer from both perspectives

**Example:**
```bash
graphrag query --root . \
  --method drift \
  --query "How does Azure AI relate to Microsoft's overall cloud strategy?"

# Behind the scenes:
# 1. Local: Find "Azure AI" entity and neighborhood
# 2. Global: Find "cloud strategy" community summaries
# 3. Combine: Entity details + strategic context
# 4. Synthesize: Comprehensive answer
```

## Python API Usage

### Basic Setup

```python
import asyncio
from graphrag.query import LocalSearch, GlobalSearch
from graphrag.llm import create_openai_chat_llm
from graphrag.config import GraphRagConfig

# Load configuration
config = GraphRagConfig.from_file("settings.yaml")

# Create LLM
llm = create_openai_chat_llm(
    api_key=config.llm.api_key,
    model=config.llm.model,
    temperature=0.0
)
```

### Custom Indexing

```python
from graphrag.index import run_pipeline_with_config

# Run indexing programmatically
await run_pipeline_with_config(
    config_path="settings.yaml",
    verbose=True
)
```

### Advanced Query Customization

```python
from graphrag.query.context_builder import LocalContextBuilder

# Build custom context
context_builder = LocalContextBuilder(
    entities=entities_df,
    relationships=relationships_df,
    text_units=text_units_df,
    embeddings=embeddings
)

# Custom search with parameters
result = await searcher.asearch(
    query="Your question here",
    conversation_history=[
        {"role": "user", "content": "Previous question"},
        {"role": "assistant", "content": "Previous answer"}
    ],
    top_k=10,              # Number of results
    temperature=0.5,       # LLM creativity
    max_tokens=2000        # Response length
)

# Access detailed results
print("Response:", result.response)
print("Context used:", result.context_data)
print("Sources:", result.sources)
```

## Use Cases and Examples

### 1. Research Paper Analysis

```bash
# Index academic papers
mkdir -p input/papers
cp research_papers/*.pdf input/papers/

graphrag index --root .

# Global query
graphrag query --method global \
  --query "What are the main research themes across these papers?"

# Local query
graphrag query --method local \
  --query "What methodologies does the Smith et al. paper use?"
```

### 2. Legal Document Processing

```bash
# Index legal contracts
mkdir -p input/contracts
cp contracts/*.docx input/contracts/

# Tune prompts for legal domain
graphrag prompt-tune --root . --domain "legal contracts"

# Index with legal-specific entities
graphrag index --root .

# Query
graphrag query --method local \
  --query "What are the termination clauses in the Microsoft contracts?"
```

### 3. Customer Feedback Analysis

```bash
# Index customer feedback
mkdir -p input/feedback
cp feedback_*.txt input/feedback/

# Global themes
graphrag query --method global \
  --query "What are the main customer pain points?"

# Specific product feedback
graphrag query --method local \
  --query "What feedback relates to product X features?"
```

### 4. News Article Summarization

```bash
# Index news articles
mkdir -p input/news
cp articles/*.txt input/news/

graphrag index --root .

# Get comprehensive summary
graphrag query --method global \
  --query "Summarize the key events and trends from these news articles"

# Entity-specific news
graphrag query --method local \
  --query "What news relates to climate change initiatives?"
```

## Advanced Features

### 1. Incremental Indexing

```bash
# Initial indexing
graphrag index --root .

# Add new documents
cp new_documents/*.txt input/

# Re-index only new content
graphrag index --root . --incremental

# Note: Full graph may need periodic rebuilding
```

### 2. Custom Entity Types

Edit `prompts/entity_extraction.txt`:

```
Entity Types:
- PRODUCT: Software products, services
- FEATURE: Product features and capabilities
- TECHNOLOGY: Technologies and frameworks
- METRIC: Performance metrics, KPIs
- INITIATIVE: Projects and strategic initiatives
- COMPETITOR: Competing products or companies
```

### 3. Multi-Language Support

```yaml
# settings.yaml
input:
  encoding: utf-8
  language: es  # Spanish

llm:
  model: gpt-4o  # Multilingual model

# Customize prompts in target language
```

### 4. Azure OpenAI Integration

```yaml
llm:
  type: azure_openai_chat
  api_base: https://your-resource.openai.azure.com
  api_version: "2024-02-15-preview"
  deployment_name: gpt-4
  api_key: ${AZURE_OPENAI_API_KEY}

embeddings:
  type: azure_openai_embedding
  api_base: https://your-resource.openai.azure.com
  api_version: "2024-02-15-preview"
  deployment_name: text-embedding-3-small
  api_key: ${AZURE_OPENAI_API_KEY}
```

### 5. Local LLM Support (Ollama)

```yaml
llm:
  type: ollama
  api_base: http://localhost:11434
  model: llama3:70b
  temperature: 0

embeddings:
  type: ollama
  api_base: http://localhost:11434
  model: nomic-embed-text
```

## Cost Management

### Understanding Costs

GraphRAG uses LLM APIs which incur costs:

**Indexing Phase** (most expensive):
- Entity extraction: Multiple LLM calls per TextUnit
- Relationship extraction: Additional calls
- Community summarization: Calls per community
- Embedding generation: Per entity/TextUnit

**Query Phase** (less expensive):
- Context retrieval: Minimal LLM use
- Answer synthesis: Single LLM call per query

### Cost Optimization Strategies

**1. Reduce Chunk Size**
```yaml
chunks:
  size: 600  # Smaller chunks = fewer tokens
  overlap: 50
```

**2. Limit Entity Extraction Passes**
```yaml
entity_extraction:
  max_gleanings: 0  # 0 = single pass, 1 = two passes
```

**3. Use Smaller Models**
```yaml
llm:
  model: gpt-4o-mini  # Cheaper than gpt-4o

embeddings:
  model: text-embedding-3-small  # Cheaper than large
```

**4. Process Subset First**
```bash
# Test on small sample
mkdir input/sample
cp input/full/*.txt input/sample/ | head -5
graphrag index --root . --input-dir input/sample
```

**5. Cache Aggressively**
```yaml
cache:
  type: file
  base_dir: cache
```

### Cost Estimation

```python
# Estimate before indexing
from graphrag.index import estimate_index_cost

cost_estimate = estimate_index_cost(
    input_dir="input/",
    config_path="settings.yaml"
)

print(f"Estimated cost: ${cost_estimate.total_cost}")
print(f"Total tokens: {cost_estimate.total_tokens}")
print(f"Estimated time: {cost_estimate.estimated_hours} hours")
```

## Best Practices

### 1. Start Small

```bash
# Test with 5-10 documents first
# Validate outputs before scaling
# Tune prompts on small sample
# Then scale to full dataset
```

### 2. Monitor Indexing Progress

```bash
# Use verbose mode
graphrag index --root . --verbose

# Check output files periodically
ls -lh output/*.parquet

# Monitor logs
tail -f output/reports/indexing.log
```

### 3. Version Control Configuration

```bash
# Track changes
git add settings.yaml prompts/
git commit -m "Update entity types for domain X"

# Tag successful configurations
git tag -a v1.0-config -m "Working config for dataset X"
```

### 4. Validate Outputs

```python
import pandas as pd

# Check extracted entities
entities = pd.read_parquet("output/create_final_entities.parquet")
print(f"Total entities: {len(entities)}")
print(f"Entity types: {entities['type'].value_counts()}")

# Check relationships
relationships = pd.read_parquet("output/create_final_relationships.parquet")
print(f"Total relationships: {len(relationships)}")
print(f"Relationship types: {relationships['type'].value_counts()}")

# Check communities
communities = pd.read_parquet("output/create_final_communities.parquet")
print(f"Total communities: {len(communities)}")
print(f"Hierarchy levels: {communities['level'].value_counts()}")
```

### 5. Iterate on Prompts

```bash
# Run initial index
graphrag index --root .

# Evaluate quality
graphrag query --method global --query "Test query"

# If quality is poor:
# 1. Adjust entity types in prompts
# 2. Modify extraction instructions
# 3. Re-run indexing
# 4. Validate improvements
```

## Troubleshooting

### Common Issues

#### "API rate limit exceeded"

```yaml
# Add delays between requests
parallelization:
  stagger: 1.0        # Increase delay
  num_threads: 2      # Reduce concurrency

llm:
  max_retries: 20     # More retries
  max_retry_wait: 60  # Longer backoff
```

#### "Out of memory during indexing"

```yaml
# Reduce batch sizes
chunks:
  size: 600           # Smaller chunks

parallelization:
  num_threads: 2      # Less parallelism
```

#### "Poor quality entity extraction"

```bash
# Run prompt tuning
graphrag prompt-tune --root . --domain "your domain"

# Manually refine prompts
nano prompts/entity_extraction.txt

# Add domain-specific examples
# Specify expected entity types clearly
```

#### "Queries return irrelevant results"

```bash
# Check if indexing completed successfully
ls -lh output/*.parquet

# Validate extracted entities
python -c "import pandas as pd; print(pd.read_parquet('output/create_final_entities.parquet').head())"

# Try different query methods
graphrag query --method local --query "Your query"
graphrag query --method global --query "Your query"
```

#### "Version incompatibility after update"

```bash
# Reinitialize configuration
graphrag init --root . --force

# This updates settings.yaml to new schema
# Review and merge your customizations
```

## Performance Optimization

### Indexing Performance

```yaml
# Optimize for speed
parallelization:
  num_threads: 8            # Max concurrent workers
  stagger: 0.1              # Minimal delay

chunks:
  size: 1500               # Larger chunks (fewer API calls)

entity_extraction:
  max_gleanings: 0         # Single pass only
```

### Query Performance

```python
# Cache query results
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_query(query_text):
    return searcher.search(query_text)

# Pre-load data structures
entities_df = pd.read_parquet("output/create_final_entities.parquet")
relationships_df = pd.read_parquet("output/create_final_relationships.parquet")

# Keep in memory for fast access
```

### Storage Optimization

```yaml
# Use compressed storage
storage:
  type: file
  compression: gzip         # Or snappy, lz4

# Or use database storage
storage:
  type: cosmosdb
  connection_string: ${COSMOS_CONNECTION_STRING}
```

## Integration Examples

### LangChain Integration

```python
from langchain.retrievers import GraphRAGRetriever
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# Create GraphRAG retriever
retriever = GraphRAGRetriever(
    index_path="output/",
    search_method="local"
)

# Build QA chain
llm = ChatOpenAI(model="gpt-4o")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# Query
result = qa_chain("What are the main themes?")
print(result["answer"])
```

### FastAPI Service

```python
from fastapi import FastAPI
from graphrag.query import LocalSearch, GlobalSearch

app = FastAPI()

# Initialize searchers
local_searcher = LocalSearch(...)
global_searcher = GlobalSearch(...)

@app.post("/query/local")
async def query_local(query: str):
    result = await local_searcher.asearch(query)
    return {"response": result.response, "sources": result.sources}

@app.post("/query/global")
async def query_global(query: str):
    result = await global_searcher.asearch(query)
    return {"response": result.response}

# Run: uvicorn main:app --reload
```

### Streamlit UI

```python
import streamlit as st
from graphrag.query import GlobalSearch

st.title("GraphRAG Query Interface")

# Query input
query = st.text_input("Enter your question:")
method = st.selectbox("Search method:", ["global", "local", "drift"])

if st.button("Search"):
    with st.spinner("Searching..."):
        # Run query
        result = await searcher.asearch(query)

        # Display results
        st.write("### Answer")
        st.write(result.response)

        st.write("### Sources")
        st.write(result.sources)
```

## Comparison with Other Approaches

### GraphRAG vs. Vector RAG

| Feature | Vector RAG | GraphRAG |
|---------|-----------|----------|
| **Structure** | Flat embeddings | Knowledge graph |
| **Relationships** | Implicit (similarity) | Explicit (edges) |
| **Multi-hop** | Poor | Excellent |
| **Summarization** | Difficult | Natural (communities) |
| **Setup Cost** | Low | High (indexing) |
| **Query Cost** | Low | Medium |
| **Best For** | Simple lookups | Complex reasoning |

### When to Use GraphRAG

✅ Use GraphRAG when:
- Queries require connecting multiple pieces of information
- Need holistic understanding of document corpus
- Relationships between entities matter
- Multi-hop reasoning is important
- Domain has rich entity/relationship structure

❌ Use Vector RAG when:
- Simple semantic search is sufficient
- Low setup cost is priority
- Documents are independent
- Queries are straightforward lookups
- Budget is constrained

## Resources

### Documentation
- **Official Docs**: https://microsoft.github.io/graphrag/
- **GitHub**: https://github.com/microsoft/graphrag
- **Research Paper**: https://arxiv.org/abs/2404.16130

### Community
- **GitHub Discussions**: https://github.com/microsoft/graphrag/discussions
- **Issues**: https://github.com/microsoft/graphrag/issues

### Examples
- **Notebooks**: https://github.com/microsoft/graphrag/tree/main/examples
- **Sample Configs**: https://github.com/microsoft/graphrag/tree/main/examples/configs

## Important Notes

**⚠️ Not an Official Microsoft Product**
> "This codebase is a demonstration of graph-based RAG and not an officially supported Microsoft offering."

**💰 Cost Considerations**
- Indexing can be expensive (especially with GPT-4)
- Test on small samples first
- Monitor API costs closely

**🔄 Version Management**
- Configuration schemas change between versions
- Run `graphrag init --force` after updates
- Review migration guides for breaking changes

**🎯 Prompt Tuning is Critical**
- Out-of-box results may be suboptimal
- Domain-specific tuning significantly improves quality
- Invest time in prompt customization

## License

Microsoft GraphRAG is released under the MIT License.

---

**Note**: This skill provides comprehensive guidance for using Microsoft GraphRAG. Always test on small datasets first, monitor costs, and tune prompts for your specific domain.
