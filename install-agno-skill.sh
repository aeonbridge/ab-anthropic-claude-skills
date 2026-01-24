#!/bin/bash
# Install Agno skill for Claude Code
# Usage: ./install-agno-skill.sh [global|local]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_TYPE="${1:-global}"

echo "🚀 Installing Agno Skill for Claude Code"
echo "Installation type: $INSTALL_TYPE"
echo ""

# Determine installation directory
if [ "$INSTALL_TYPE" = "global" ]; then
    INSTALL_DIR="$HOME/.claude/skills"
    echo "📁 Installing to global skills directory: $INSTALL_DIR"
    echo "   (Will be available in ALL projects)"
elif [ "$INSTALL_TYPE" = "local" ]; then
    INSTALL_DIR="$(pwd)/.claude/skills"
    echo "📁 Installing to local project directory: $INSTALL_DIR"
    echo "   (Only available in this project)"
else
    echo "❌ Invalid installation type: $INSTALL_TYPE"
    echo "Usage: $0 [global|local]"
    exit 1
fi

# Create skills directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Copy Agno skill (complete structure)
echo "📦 Copying Agno skill with complete structure..."
cp -r "$SCRIPT_DIR/output/agno/" "$INSTALL_DIR/"

# Verify installation
if [ -f "$INSTALL_DIR/agno/SKILL.md" ]; then
    echo "✅ SKILL.md installed"
else
    echo "❌ SKILL.md not found!"
    exit 1
fi

if [ -d "$INSTALL_DIR/agno/references" ]; then
    REFS_COUNT=$(find "$INSTALL_DIR/agno/references" -type f | wc -l | tr -d ' ')
    echo "✅ references/ directory installed ($REFS_COUNT files)"
else
    echo "⚠️  references/ directory not found"
fi

# Check frontmatter
echo ""
echo "🔍 Validating frontmatter..."
if head -5 "$INSTALL_DIR/agno/SKILL.md" | grep -q "^name: agno$"; then
    echo "✅ Frontmatter 'name' is valid"
else
    echo "❌ Frontmatter 'name' is missing or invalid"
fi

if head -5 "$INSTALL_DIR/agno/SKILL.md" | grep -q "^description:"; then
    echo "✅ Frontmatter 'description' is present"
else
    echo "❌ Frontmatter 'description' is missing"
fi

# Calculate sizes
SKILL_SIZE=$(du -sh "$INSTALL_DIR/agno/SKILL.md" | cut -f1)
TOTAL_SIZE=$(du -sh "$INSTALL_DIR/agno" | cut -f1)

echo ""
echo "📊 Installation Summary:"
echo "   - SKILL.md size: $SKILL_SIZE"
echo "   - Total skill size: $TOTAL_SIZE"
echo "   - Location: $INSTALL_DIR/agno/"

echo ""
echo "✅ Agno skill installed successfully!"
echo ""
echo "🎯 Next Steps:"
echo "   1. Claude Code will auto-discover this skill"
echo "   2. Test with: 'Create an Agno agent that...'"
echo "   3. Check discovery: ls -la $INSTALL_DIR/agno/"
echo ""
echo "📖 For project-specific instructions, add to .claude/CLAUDE.md:"
echo "   # Agno Framework"
echo "   - Use the agno skill for AI agent development"
echo "   - Skill location: $INSTALL_DIR/agno/"