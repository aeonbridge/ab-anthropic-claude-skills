# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains a comprehensive collection of Claude AI Skills created for various AI frameworks, tools, and platforms. It uses Python automation scripts to generate, validate, and package skills that comply with the official Claude AI Skills format specification.

## Architecture

### Core Components

1. **Skill Generation Pipeline** (`create_skill.py`)
   - Automated skill generation from documentation URLs
   - YAML frontmatter creation following Claude AI format spec
   - Directory structure generation (SKILL.md, assets/, scripts/, references/)
   - ZIP packaging for distribution
   - Automatic README.md updates
   - Git integration with commit and push

2. **Skill Enhancement System** (`enhance_skill.py`)
   - Provides enhancement checklist for generated skills
   - Guides through documentation reading and code extraction
   - Ensures production-quality skill content

3. **Frontmatter Validation** (`add_frontmatter.py`)
   - Adds/validates YAML frontmatter to existing skills
   - Ensures compliance with Claude AI format (name ≤64 chars, description ≤1024 chars)

4. **Configuration System** (`configs/`)
   - JSON configuration files for each skill
   - Defines source URLs (documentation, GitHub repos)
   - Specifies scraping parameters and enhancement focus areas

5. **Skill Collection** (`output/`)
   - Each skill has its own directory: `output/{skill-name}/`
   - Structure: SKILL.md (with frontmatter), assets/, scripts/, references/
   - Packaged as `{skill-name}.zip` for distribution

### Directory Structure

```
ab-anthropic-claude-skills/
├── create_skill.py          # Main skill generation script
├── enhance_skill.py         # Enhancement guidance script
├── add_frontmatter.py       # Frontmatter validation tool
├── configs/                 # JSON configuration files
│   ├── agno_unified.json
│   ├── dify_github.json
│   └── ...
├── output/                  # Generated skills
│   ├── agno/
│   │   ├── SKILL.md        # Main skill file with YAML frontmatter
│   │   ├── assets/
│   │   ├── scripts/
│   │   └── references/
│   ├── agno.zip            # Packaged skill
│   └── ...
├── examples/               # Multi-skill integration examples
│   └── whatsapp-knowledge-bot/
└── docs/
    ├── README.md
    ├── SCRIPTS_GUIDE.md    # Complete automation guide
    ├── VALIDATION.md       # Format compliance validation
    └── INTEGRATION_GUIDE.md # Multi-skill integration patterns
```

## Common Development Commands

### Creating a New Skill

```bash
# Basic skill creation
./create_skill.py <skill-name> <url1> [url2] [url3] ...

# Example: Create FastAPI skill
./create_skill.py fastapi \
  https://fastapi.tiangolo.com \
  https://github.com/tiangolo/fastapi

# Skip git operations (useful during development)
./create_skill.py myskill https://example.com --skip-git
```

### Enhancing a Generated Skill

```bash
# Get enhancement guidance
./enhance_skill.py <skill-name>

# Example
./enhance_skill.py fastapi
```

### Validating Skills

```bash
# Add/validate frontmatter for all skills
python add_frontmatter.py

# Dry run to preview changes
python add_frontmatter.py --dry-run
```

### Repackaging After Manual Edits

```bash
# After editing a skill's SKILL.md
cd output
rm {skill-name}.zip
zip -r {skill-name}.zip {skill-name}/
```

### Git Workflow

```bash
# The create_skill.py script automatically commits and pushes
# It uses the current branch name
git checkout -b claude/new-skill-name
./create_skill.py myskill https://example.com

# For manual commits
git add configs/{skill-name}_github.json output/{skill-name}/ output/{skill-name}.zip README.md
git commit -m "Add comprehensive {skill-name} skill"
git push -u origin $(git branch --show-current)
```

## Key Architectural Patterns

### 1. Claude AI Skills Format Compliance

All skills MUST have YAML frontmatter in SKILL.md:

```yaml
---
name: skill-name              # lowercase, hyphens only, max 64 chars
description: Brief description of what this skill does and when to use it  # max 1024 chars
---
```

**Critical**: The `create_skill.py` script automatically generates compliant frontmatter. Never manually create skills without using the script or ensuring frontmatter compliance.

### 2. Skill Generation Workflow

The standard workflow implemented in `create_skill.py`:
1. Categorize URLs (GitHub vs docs vs web)
2. Create configuration JSON in `configs/`
3. Create directory structure with .gitkeep files
4. Generate SKILL.md with frontmatter + comprehensive template
5. Package as .zip
6. Update README.md
7. Git commit and push (with retry logic)

### 3. Template vs Production Skills

- Scripts generate **template** SKILL.md files
- Templates contain placeholder sections
- Production skills require manual enhancement with:
  - Real code examples from documentation
  - Actual API references
  - Specific use cases and patterns
  - Technology-specific details

**Important**: Always enhance templates before considering them production-ready.

### 4. Multi-Skill Integration Pattern

See `examples/whatsapp-knowledge-bot/` for reference:
- Combines multiple skills (Evolution API + Dify + Graphiti)
- Uses Docker Compose for service orchestration
- Implements skill chaining pattern (input → skill A → skill B → skill C → output)
- Includes health checks, error handling, and monitoring

Key integration patterns:
- **Skill Chaining**: Linear data flow through skills
- **Skill Branching**: Conditional skill selection
- **Parallel Execution**: Independent skill operations
- **Event-Driven**: Asynchronous, decoupled services

## Important Implementation Details

### Python Script Best Practices

1. **Always use Path objects** from `pathlib` for file paths
2. **Error handling**: Scripts include comprehensive try/except blocks
3. **Git retry logic**: Push operations retry with exponential backoff (2s, 4s, 8s, 16s)
4. **Subprocess calls**: Use `capture_output=True, text=True` for readable output

### Configuration File Structure

JSON configs support:
- GitHub repositories (repo owner/name)
- Web documentation (URL + depth)
- Enhancement focus areas
- Metadata (tags, category, license)

Example from `agno_unified.json`:
```json
{
  "name": "agno",
  "sources": {
    "documentation": { "base_url": "...", "max_depth": 3 },
    "github": { "repository": "owner/repo", "include_readme": true }
  },
  "enhancement": { "focus_areas": [...] }
}
```

### Skill Naming Conventions

- Use lowercase with hyphens: `my-skill-name`
- Be specific: `redis-cache` not just `redis`
- Include platform for clarity: `evolution-api-whatsapp`, `dify-llm-platform`
- Max 64 characters (enforced by Claude AI format)

### URL Categorization Logic

In `create_skill.py`:
- `github.com` in netloc → GitHub source
- `docs.`, `doc.`, `/docs/` in URL → Documentation source
- Everything else → Web source

## Testing and Validation

### Validate Frontmatter

```bash
# Check all skills have valid frontmatter
python add_frontmatter.py --dry-run
```

### Verify Skill Structure

```bash
# Extract and verify a skill
cd output
unzip skill-name.zip
tree skill-name/

# Should show:
# skill-name/
# ├── SKILL.md (with frontmatter)
# ├── assets/
# ├── scripts/
# └── references/
```

### Check Skill Size

```bash
# Skills should be comprehensive but not bloated
ls -lh output/*.zip

# SKILL.md should typically be 5-50 KB
# ZIP files vary widely (agno is 1.7MB due to extensive docs)
```

## Troubleshooting Common Issues

### Issue: Script can't find skill-seekers

The `skill-seekers` tool is optional. Scripts will proceed with manual creation if not found.

```bash
# Install if needed
pip install skill-seekers
```

### Issue: Git push fails with 403

Ensure you're on a branch that starts with `claude/`:

```bash
git checkout -b claude/my-feature
```

### Issue: Generated SKILL.md is too generic

This is expected. Use enhancement workflow:

```bash
./enhance_skill.py <skill-name>
# Then manually enhance with real documentation
```

### Issue: Frontmatter validation fails

Check format:
- Name must be lowercase, hyphens only, max 64 chars
- Description max 1024 chars
- Must have `---` delimiters

```bash
# Re-validate
python add_frontmatter.py --dry-run
```

## Documentation References

- **Scripts Guide**: `SCRIPTS_GUIDE.md` - Detailed usage of automation scripts
- **Validation Guide**: `VALIDATION.md` - Claude AI format compliance details
- **Integration Guide**: `INTEGRATION_GUIDE.md` - Multi-skill patterns and examples
- **Examples Guide**: `EXAMPLES.md` - 50+ skill creation examples
- **Claude AI Skills Docs**: https://code.claude.com/docs/en/skills

## Current Skills

The repository includes production-ready skills for:
- **Agno**: Multi-agent AI framework (1.7MB - most comprehensive)
- **Dify**: LLM application platform with visual workflows
- **Evolution API**: WhatsApp integration platform
- **Graphiti/Zep**: Temporal knowledge graphs for AI agents
- **Microsoft GraphRAG**: Graph-based RAG system
- **MCP**: Model Context Protocol for LLM integration
- **yt-dlp**: Video/audio downloader

All skills are validated for Claude AI format compliance (see VALIDATION.md).

## Code Quality Standards

- Python 3.6+ required for pathlib and f-strings
- Use subprocess.run() with timeouts for external commands
- Include comprehensive error messages
- Never hardcode paths - use Path objects and base_dir parameter
- All scripts should be executable: `chmod +x script.py`
- Use shebang: `#!/usr/bin/env python3`

## Integration with Claude

Skills are designed for use with:
- **Claude Desktop**: Upload .zip files
- **Claude Code**: Automatic skill discovery via frontmatter
- **Agent Frameworks**: MCP servers and protocol integrations

Claude discovers skills by:
1. Reading YAML frontmatter
2. Matching description to user queries
3. Loading SKILL.md content as instructions
4. Using specified tools (if allowed-tools defined)