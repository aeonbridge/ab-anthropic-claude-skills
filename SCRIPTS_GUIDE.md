# Skill Generation Scripts Guide

This guide explains how to use the automated skill generation scripts in this repository.

## Overview

This repository provides two main scripts for creating Claude skills:

1. **`create_skill.py`** - Automated skill generation from URLs
2. **`enhance_skill.py`** - Helper for enhancing generated skills

## create_skill.py

### Description

Automates the entire skill creation process, following the established pattern used in this repository:
- Creates configuration files
- Generates directory structure
- Creates SKILL.md template
- Packages as .zip file
- Updates README.md
- Commits and pushes to git

### Usage

```bash
python create_skill.py <skill_name> <url1> [url2] [url3] ... [options]
```

### Arguments

- `skill_name`: Name of the skill (e.g., 'fastapi', 'redis-cache')
- `urls`: One or more URLs for documentation, GitHub repos, etc.

### Options

- `--skip-git`: Skip git commit and push operations
- `--base-dir PATH`: Base directory for the project (default: current directory)

### Examples

#### Example 1: Create FastAPI skill

```bash
python create_skill.py fastapi \
  https://fastapi.tiangolo.com \
  https://github.com/tiangolo/fastapi
```

#### Example 2: Create Redis skill with multiple docs

```bash
python create_skill.py "redis cache" \
  https://redis.io/docs \
  https://redis.io/docs/getting-started/ \
  https://github.com/redis/redis-py
```

#### Example 3: Create skill without git operations

```bash
python create_skill.py langchain \
  https://docs.langchain.com \
  https://github.com/langchain-ai/langchain \
  --skip-git
```

#### Example 4: Create Docker skill

```bash
python create_skill.py docker \
  https://docs.docker.com \
  https://docs.docker.com/get-started/ \
  https://github.com/docker/cli
```

### What It Does

The script performs these steps:

1. **Configuration Creation**
   - Analyzes URLs (GitHub vs docs vs web)
   - Creates `configs/{skill_name}_github.json`
   - Categorizes sources appropriately

2. **Directory Structure**
   - Creates `output/{skill_name}/` directory
   - Creates subdirectories: `assets/`, `scripts/`, `references/`
   - Adds `.gitkeep` files for empty directories

3. **SKILL.md Generation**
   - Creates comprehensive template
   - Includes all standard sections
   - References provided URLs
   - Ready for enhancement

4. **Packaging**
   - Creates `output/{skill_name}.zip`
   - Includes all files and subdirectories

5. **README Update**
   - Adds new skill section to README.md
   - Updates configuration files list
   - Adds resources section

6. **Git Operations** (unless `--skip-git`)
   - Commits all changes
   - Pushes to current branch
   - Includes detailed commit message
   - Retries on network failures

### Output Structure

```
output/
  {skill_name}/
    SKILL.md              # Main skill file
    assets/               # Images, diagrams
      .gitkeep
    scripts/              # Helper scripts
      .gitkeep
    references/           # Additional docs
      .gitkeep
  {skill_name}.zip        # Packaged skill

configs/
  {skill_name}_github.json  # Configuration file
```

### Important Notes

⚠️ **Template Output**: The generated SKILL.md is a template. For production-quality skills, you need to enhance it with:
- Real code examples from documentation
- Detailed API references
- Actual use cases and patterns
- Community best practices

Use `enhance_skill.py` for guidance on enhancement.

## enhance_skill.py

### Description

Provides a comprehensive checklist and guidance for enhancing generated skills with real documentation and examples.

### Usage

```bash
python enhance_skill.py <skill_name> [options]
```

### Arguments

- `skill_name`: Name of the skill to enhance

### Options

- `--base-dir PATH`: Base directory for the project (default: current directory)

### Example

```bash
python enhance_skill.py fastapi
```

### Output

The script provides:
- Current skill file location and size
- List of resources from configuration
- Comprehensive enhancement checklist
- Tips for effective enhancement
- Next steps and commands

### Enhancement Checklist

The script guides you through:

1. **Reading Official Documentation**
   - Key concepts and terminology
   - Architecture and design patterns
   - Installation and setup

2. **Extracting Code Examples**
   - Quick start examples
   - Common use cases
   - Integration patterns

3. **Reviewing GitHub Repository**
   - README and documentation
   - Examples directory
   - Tests for usage patterns

4. **Adding Specific Details**
   - Real code instead of placeholders
   - Actual configuration examples
   - Real API documentation

5. **Including Best Practices**
   - Security considerations
   - Performance optimization
   - Production deployment

6. **Adding Troubleshooting**
   - Common errors and fixes
   - Debugging techniques
   - FAQ and solutions

7. **Verifying Completeness**
   - All sections filled
   - Examples tested
   - Links working

## Workflow Examples

### Complete Workflow: Create and Enhance

```bash
# Step 1: Generate skill
python create_skill.py redis \
  https://redis.io/docs \
  https://github.com/redis/redis-py \
  --skip-git

# Step 2: Get enhancement guidance
python enhance_skill.py redis

# Step 3: Manually enhance SKILL.md
# - Read documentation from URLs
# - Extract real examples
# - Add detailed content

# Step 4: Repackage
cd output
rm redis.zip
zip -r redis.zip redis/

# Step 5: Commit and push
cd ..
git add configs/redis_github.json output/redis/ output/redis.zip README.md
git commit -m "Add comprehensive Redis skill"
git push
```

### Batch Creation

Create multiple skills at once:

```bash
# Create FastAPI skill
python create_skill.py fastapi \
  https://fastapi.tiangolo.com \
  https://github.com/tiangolo/fastapi

# Create Django skill
python create_skill.py django \
  https://docs.djangoproject.com \
  https://github.com/django/django

# Create Flask skill
python create_skill.py flask \
  https://flask.palletsprojects.com \
  https://github.com/pallets/flask
```

## Integration with Claude

You can use Claude to help enhance skills:

```bash
# Generate skill
python create_skill.py fastapi https://fastapi.tiangolo.com --skip-git

# Then ask Claude:
# "Please enhance the FastAPI skill at output/fastapi/SKILL.md by:
# 1. Reading the documentation at https://fastapi.tiangolo.com
# 2. Adding real code examples
# 3. Including actual API patterns
# 4. Adding comprehensive best practices"
```

## Tips and Best Practices

### Skill Naming

- Use lowercase with hyphens: `my-skill-name`
- Be specific: `redis-cache` instead of just `redis`
- Use full names: `microsoft-graphrag` not `graphrag`

### URL Selection

Include diverse sources:
- Official documentation (most important)
- GitHub repository
- Tutorial/getting started pages
- API reference pages
- Community resources

### Git Branch Management

The script pushes to your current branch:
```bash
# Check current branch
git branch --show-current

# Create feature branch if needed
git checkout -b claude/new-skill-name

# Then run script
python create_skill.py myskill https://example.com
```

### Enhancement Priority

Focus enhancement efforts on:
1. **Quick Start** - Make it easy to begin
2. **Common Patterns** - Most frequently used features
3. **Best Practices** - Security, performance, production
4. **Troubleshooting** - Common issues and solutions

## Troubleshooting

### Script Issues

**Issue**: `ModuleNotFoundError: No module named 'skill_seekers'`
```bash
# Solution: Install skill-seekers
pip install skill-seekers
```

**Issue**: `zip command not found`
```bash
# Solution: Install zip utility
# Ubuntu/Debian:
sudo apt-get install zip

# macOS:
brew install zip
```

**Issue**: Git push fails with 403
```bash
# Solution: Ensure branch starts with 'claude/' and matches session
# Check current branch requirements in task description
```

### Skill Quality Issues

**Issue**: Generated SKILL.md is too generic

**Solution**: This is expected. The script creates templates. Use `enhance_skill.py` for guidance on enhancement, then:
- Manually read documentation
- Extract real examples
- Add technology-specific details
- Or use Claude/LLM to help research and enhance

**Issue**: Missing important sections

**Solution**: Edit SKILL.md and add:
- Security considerations
- Performance tips
- Production deployment
- Integration examples

## Advanced Usage

### Custom Base Directory

```bash
python create_skill.py myskill \
  https://example.com \
  --base-dir /path/to/skills/repo
```

### Programmatic Usage

```python
from pathlib import Path
from create_skill import SkillGenerator

generator = SkillGenerator(
    skill_name="myskill",
    urls=["https://example.com", "https://github.com/example/repo"],
    base_dir=Path("/path/to/skills")
)

generator.generate(skip_git=False)
```

### Custom Configuration

After generation, you can modify the config file:

```json
{
  "name": "myskill",
  "output_dir": "output",
  "sources": [
    {
      "type": "github",
      "repo": "example/repo",
      "include_issues": true,
      "include_prs": true
    }
  ]
}
```

Then rerun skill-seekers if needed:
```bash
skill-seekers scrape --config configs/myskill_github.json
```

## Contributing

When creating new skills:
1. Follow the established patterns
2. Use the automation scripts
3. Enhance with real documentation
4. Test examples before committing
5. Update README.md appropriately

## Support

For issues or questions:
- Check this guide first
- Review existing skills for examples
- Consult official skill-seekers documentation
- Review the code in `create_skill.py`

---

**Last Updated**: 2025-12-15
**Script Version**: 1.0.0
