#!/usr/bin/env python3
"""
Add YAML Frontmatter to Existing Skills

This script adds proper YAML frontmatter to all existing SKILL.md files
to comply with Claude AI Skills format specification.

Usage:
    python add_frontmatter.py [--dry-run]
"""

import argparse
import re
from pathlib import Path
from typing import Dict


# Skill metadata
SKILL_METADATA = {
    "agno": {
        "name": "agno-ai-framework",
        "description": "Build and deploy multi-agent AI systems using the Agno framework. Use when working with AI agents, multi-agent teams, workflows, LLM integrations, RAG patterns, or deploying AgentOS applications. Covers agent creation, tools, knowledge bases, memory, and production deployment."
    },
    "yt-dlp": {
        "name": "yt-dlp-downloader",
        "description": "Download videos and audio from thousands of websites using yt-dlp. Use when downloading media from YouTube, TikTok, Vimeo, extracting audio, managing playlists, recording live streams, or automating video downloads. Includes format selection, metadata handling, and SponsorBlock integration."
    },
    "graphiti": {
        "name": "graphiti-zep-knowledge-graph",
        "description": "Build temporal knowledge graphs for AI agents using Graphiti and Zep. Use when implementing persistent agent memory, bi-temporal data models, hybrid search (semantic + BM25 + graph), or integrating with Neo4j, FalkorDB, Kuzu. Covers entity management, relationships, and LLM integration."
    },
    "graphrag": {
        "name": "microsoft-graphrag",
        "description": "Implement graph-based RAG using Microsoft GraphRAG with hierarchical community detection. Use when building advanced RAG systems, extracting entities and relationships, performing global/local/DRIFT queries, or analyzing private datasets with LLMs. Includes Leiden algorithm, prompt tuning, and cost management."
    },
    "evolution-api": {
        "name": "evolution-api-whatsapp",
        "description": "Integrate WhatsApp messaging using Evolution API platform. Use when building WhatsApp bots, chatbots with Typebot/Chatwoot/Dify, sending messages/media, managing groups, or deploying multi-instance WhatsApp services. Covers webhooks, message queues, and production deployment."
    },
    "mcp": {
        "name": "model-context-protocol",
        "description": "Build MCP servers and clients for LLM context integration. Use when creating tools, resources, or prompts for Claude/LLMs, implementing OAuth 2.1 security, building filesystem/API/database servers, or integrating with Claude Desktop. Covers FastMCP (Python), TypeScript SDK, STDIO/SSE transports."
    },
    "dify": {
        "name": "dify-llm-platform",
        "description": "Build LLM applications using Dify's visual workflow platform. Use when creating AI chatbots, implementing RAG pipelines, developing agents with tools, managing knowledge bases, deploying LLM apps, or building workflows with drag-and-drop. Supports hundreds of LLMs, Docker/Kubernetes deployment."
    }
}


def has_frontmatter(content: str) -> bool:
    """Check if content already has YAML frontmatter"""
    return content.strip().startswith('---')


def create_frontmatter(skill_name: str, metadata: Dict[str, str]) -> str:
    """Create YAML frontmatter for a skill"""
    name = metadata.get('name', skill_name)
    description = metadata.get('description', f'Comprehensive skill for {skill_name}')

    # Ensure name follows format requirements
    name = name.lower().replace(' ', '-')
    name = re.sub(r'[^a-z0-9-]', '', name)[:64]

    # Ensure description is within limits
    if len(description) > 1024:
        description = description[:1021] + '...'

    frontmatter = f"""---
name: {name}
description: {description}
---

"""
    return frontmatter


def add_frontmatter_to_file(skill_file: Path, skill_name: str, dry_run: bool = False):
    """Add frontmatter to a SKILL.md file if it doesn't have one"""

    # Read current content
    with open(skill_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has frontmatter
    if has_frontmatter(content):
        print(f"✓ {skill_name}: Already has frontmatter")
        return False

    # Get metadata
    metadata = SKILL_METADATA.get(skill_name, {})
    if not metadata:
        print(f"⚠️  {skill_name}: No metadata found, using defaults")
        metadata = {
            'name': skill_name,
            'description': f'Comprehensive skill for {skill_name.replace("-", " ").title()}'
        }

    # Create frontmatter
    frontmatter = create_frontmatter(skill_name, metadata)

    # Remove leading title if it exists (will be redundant with name)
    lines = content.split('\n')
    if lines and lines[0].startswith('# '):
        content = '\n'.join(lines[1:]).lstrip()

    # Combine frontmatter and content
    new_content = frontmatter + content

    if dry_run:
        print(f"🔍 {skill_name}: Would add frontmatter:")
        print(frontmatter)
        return False

    # Write updated content
    with open(skill_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ {skill_name}: Added frontmatter")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Add YAML frontmatter to existing SKILL.md files"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    args = parser.parse_args()

    base_dir = Path(__file__).parent
    output_dir = base_dir / "output"

    if not output_dir.exists():
        print(f"❌ Error: Output directory not found: {output_dir}")
        return 1

    print(f"\n{'='*60}")
    print(f"Adding YAML Frontmatter to Skills")
    print(f"{'='*60}\n")

    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be modified\n")

    # Find all SKILL.md files
    skill_files = list(output_dir.glob("*/SKILL.md"))

    if not skill_files:
        print("⚠️  No SKILL.md files found")
        return 0

    print(f"Found {len(skill_files)} skill(s):\n")

    updated = 0
    for skill_file in sorted(skill_files):
        skill_name = skill_file.parent.name
        if add_frontmatter_to_file(skill_file, skill_name, args.dry_run):
            updated += 1

    print(f"\n{'='*60}")
    if args.dry_run:
        print(f"Would update {updated} skill(s)")
    else:
        print(f"✅ Updated {updated} skill(s)")
        if updated > 0:
            print(f"\nNext steps:")
            print(f"1. Review the updated SKILL.md files")
            print(f"2. Repackage skills: cd output && zip -r <skill>.zip <skill>/")
            print(f"3. Commit changes: git add . && git commit -m 'Add YAML frontmatter to skills'")
    print(f"{'='*60}\n")

    return 0


if __name__ == "__main__":
    exit(main())
