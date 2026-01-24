# Testing Agno Skill Auto-Discovery in Claude Code

This guide helps you verify that Claude Code automatically uses the Agno skill when needed.

## Pre-Test Checklist

### 1. Verify Skill Installation

```bash
# Check global installation
ls -la ~/.claude/skills/agno/

# Expected output:
# drwxr-xr-x  agno/
# -rw-r--r--  SKILL.md
# drwxr-xr-x  references/
# drwxr-xr-x  scripts/
# drwxr-xr-x  assets/

# Check specific files
ls -la ~/.claude/skills/agno/SKILL.md
ls -la ~/.claude/skills/agno/references/llms.md
```

### 2. Validate Frontmatter

```bash
# Check YAML frontmatter
head -5 ~/.claude/skills/agno/SKILL.md

# Expected output:
# ---
# name: agno
# description: Comprehensive skill for building, deploying, and managing multi-agent AI systems with Agno framework
# ---
```

### 3. Check Sizes

```bash
# Verify complete structure
du -sh ~/.claude/skills/agno/*

# Expected:
# 20K    SKILL.md
# 8.0M   references/
# 4.0K   scripts/
# 4.0K   assets/
```

## Test Cases

### Test 1: Simple Agent Creation (Basic Trigger)

**User prompt:**
```
Create a simple Agno agent that responds to greetings
```

**Expected behavior:**
- ✅ Claude Code identifies "Agno agent" in prompt
- ✅ Loads `~/.claude/skills/agno/SKILL.md`
- ✅ Generates code using Agno framework
- ✅ Includes imports: `from agno.agent import Agent`

**Validation:**
- Check if generated code matches Agno patterns
- Verify imports are correct
- Ensure code is runnable

---

### Test 2: Advanced Features (Reference Loading)

**User prompt:**
```
Create an Agno agent with OpenAI model, tools, and memory. Show me all configuration options.
```

**Expected behavior:**
- ✅ Loads SKILL.md initially
- ✅ Mentions "see references/llms.md" for detailed config
- ✅ Loads `references/llms.md` for complete API
- ✅ Provides comprehensive configuration example

**Validation:**
- Code includes model configuration
- Tools are properly defined
- Memory setup is included
- Response cites reference files

---

### Test 3: Multi-Agent System (Team/Workflow)

**User prompt:**
```
Build a multi-agent research system with Agno that has a researcher, writer, and editor
```

**Expected behavior:**
- ✅ Claude uses Agno skill automatically
- ✅ Creates `Team` or `Workflow` structure
- ✅ Defines multiple agents
- ✅ Shows agent collaboration pattern

**Validation:**
- Uses `from agno.team import Team` or `from agno.workflow import Workflow`
- Multiple agents defined
- Delegation/orchestration logic present

---

### Test 4: RAG Implementation

**User prompt:**
```
Create an Agno agent that uses RAG with a knowledge base
```

**Expected behavior:**
- ✅ Claude loads Agno skill
- ✅ Includes knowledge base setup
- ✅ Vector database integration
- ✅ Search and retrieval patterns

**Validation:**
- Imports include `from agno.knowledge import Knowledge`
- Vector DB configuration present
- Search/retrieval code included

---

### Test 5: Without Agno Keyword (Context Detection)

**User prompt:**
```
I need to build a multi-agent AI system for customer support
```

**Expected behavior:**
- ✅ Claude recognizes "multi-agent AI system"
- ✅ Loads Agno skill based on description match
- ✅ Suggests Agno framework
- ✅ Provides implementation

**Validation:**
- Skill is used even without "Agno" keyword
- Framework suggestion is appropriate

---

## Test Results Template

```markdown
## Test Execution: [Date]

### Test 1: Simple Agent Creation
- [ ] Skill auto-loaded
- [ ] Correct imports
- [ ] Code is runnable
- [ ] Notes:

### Test 2: Advanced Features
- [ ] Reference files loaded
- [ ] Complete configuration
- [ ] API details accurate
- [ ] Notes:

### Test 3: Multi-Agent System
- [ ] Team/Workflow used
- [ ] Multiple agents
- [ ] Collaboration pattern
- [ ] Notes:

### Test 4: RAG Implementation
- [ ] Knowledge base setup
- [ ] Vector DB integration
- [ ] Search patterns
- [ ] Notes:

### Test 5: Context Detection
- [ ] Skill loaded without keyword
- [ ] Framework suggested
- [ ] Implementation correct
- [ ] Notes:

### Overall Assessment
- Skills working: [ ] Yes [ ] No
- Issues found:
- Improvements needed:
```

---

## Debugging Failed Tests

### Issue: Skill Not Loading

**Check:**
```bash
# 1. Verify installation path
ls -la ~/.claude/skills/agno/SKILL.md

# 2. Check frontmatter format
head -5 ~/.claude/skills/agno/SKILL.md

# 3. Validate YAML syntax
python3 -c "
import yaml
with open('$HOME/.claude/skills/agno/SKILL.md') as f:
    content = f.read()
    frontmatter = content.split('---')[1]
    yaml.safe_load(frontmatter)
print('✅ Frontmatter valid')
"
```

**Fix:**
```bash
# Reinstall skill
cd ~/Documents/COMPANIES/AB/repos/public/ab-anthropic-claude-skills
./install-agno-skill.sh global
```

---

### Issue: References Not Found

**Check:**
```bash
# Verify references exist
ls -la ~/.claude/skills/agno/references/

# Check file sizes
du -h ~/.claude/skills/agno/references/*
```

**Fix:**
```bash
# Copy complete structure
cp -r output/agno/ ~/.claude/skills/
```

---

### Issue: Wrong Framework Suggested

**Check description:**
```bash
# Extract description
grep "^description:" ~/.claude/skills/agno/SKILL.md
```

**Expected:**
```
description: Comprehensive skill for building, deploying, and managing multi-agent AI systems with Agno framework
```

**If different:**
- Description might not match your use case
- Consider adding keywords: "agents", "multi-agent", "RAG", "AI workflows"

---

## Advanced Testing: Skill Priority

If you have multiple agent frameworks installed (LangChain, CrewAI, etc.), test that Agno is chosen when appropriate:

**Test:**
```
Compare Agno and LangChain for building a multi-agent system
```

**Expected:**
- ✅ Claude loads both skills (if LangChain skill exists)
- ✅ Provides comparison
- ✅ Uses Agno skill when you choose it

---

## Continuous Validation

Add to your project's CI/CD:

```bash
#!/bin/bash
# .github/workflows/validate-skills.yml (or similar)

# Validate Agno skill is present and valid
if [ ! -f "$HOME/.claude/skills/agno/SKILL.md" ]; then
    echo "❌ Agno skill not installed"
    exit 1
fi

# Validate frontmatter
if ! head -5 "$HOME/.claude/skills/agno/SKILL.md" | grep -q "^name: agno$"; then
    echo "❌ Agno skill frontmatter invalid"
    exit 1
fi

echo "✅ Agno skill validation passed"
```

---

## Performance Benchmarks

Track skill loading performance:

1. **Initial Load Time**: Time from prompt to first response
2. **Reference Load Time**: Time to load additional reference files
3. **Code Quality**: % of generated code that runs without modification

**Expected:**
- Initial load: < 1 second
- Reference load: < 2 seconds
- Code quality: > 95% (minimal fixes needed)

---

## Feedback Loop

After testing, improve skill effectiveness:

1. **Add examples** to SKILL.md for common patterns
2. **Update description** if certain queries aren't triggering the skill
3. **Expand references/** with more detailed API docs
4. **Create shortcuts** in `.claude/CLAUDE.md` for frequent patterns

---

## Success Criteria

The Agno skill is working correctly when:

- ✅ Auto-loads for "Agno agent" prompts
- ✅ Auto-loads for "multi-agent system" prompts (context detection)
- ✅ Provides correct imports and code structure
- ✅ Loads reference files when needed
- ✅ Generated code runs without major modifications
- ✅ Suggests best practices (async, type hints, etc.)

---

## Next Steps

Once testing passes:

1. **Document patterns** in project's `.claude/CLAUDE.md`
2. **Create templates** for common agent types
3. **Add more skills** (Dify, Graphiti) for integration
4. **Build examples** showing skill composition

---

**Last Updated:** 2026-01-24
**Tested With:** Claude Code CLI
**Skill Version:** agno-2026-01