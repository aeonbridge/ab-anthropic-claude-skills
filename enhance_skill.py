#!/usr/bin/env python3
"""
Skill Enhancement Script

This script enhances a generated SKILL.md by fetching real documentation
and examples from the provided URLs to create a comprehensive, production-quality skill.

Usage:
    python enhance_skill.py <skill_name>

Example:
    python enhance_skill.py fastapi
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List


def enhance_skill(skill_name: str, base_dir: Path = None):
    """
    Enhance a skill by providing guidance on what to research and include.

    This script provides a checklist and suggestions for manual enhancement
    of the generated SKILL.md file.
    """
    base_dir = base_dir or Path.cwd()
    skill_dir = base_dir / "output" / skill_name
    skill_file = skill_dir / "SKILL.md"
    config_file = base_dir / "configs" / f"{skill_name}_github.json"

    if not skill_file.exists():
        print(f"❌ Error: Skill file not found: {skill_file}")
        sys.exit(1)

    if not config_file.exists():
        print(f"❌ Error: Config file not found: {config_file}")
        sys.exit(1)

    # Load config to get URLs
    with open(config_file, "r") as f:
        config = json.load(f)

    print(f"\n{'='*60}")
    print(f"📝 Skill Enhancement Checklist: {skill_name}")
    print(f"{'='*60}\n")

    print("Current skill file:", skill_file)
    print(f"Current size: {skill_file.stat().st_size:,} bytes\n")

    print("📚 Resources from config:")
    for source in config.get("sources", []):
        if source["type"] == "github":
            print(f"  - GitHub: https://github.com/{source['repo']}")
        elif source["type"] == "web":
            print(f"  - Documentation: {source['url']}")
    print()

    print("✅ Enhancement Checklist:\n")

    checklist = [
        ("Read Official Documentation", [
            "Visit all documentation URLs",
            "Extract key concepts and terminology",
            "Understand architecture and design patterns",
            "Note installation and setup steps"
        ]),
        ("Extract Code Examples", [
            "Find quick start examples",
            "Collect common use cases",
            "Gather integration patterns",
            "Document API usage examples"
        ]),
        ("Review GitHub Repository", [
            "Check README.md for overview",
            "Review examples/ directory",
            "Check docs/ directory",
            "Look at tests/ for usage patterns",
            "Review issues for common problems"
        ]),
        ("Add Specific Details", [
            "Replace generic placeholders with actual code",
            "Add real configuration examples",
            "Include actual environment variables",
            "Document real API endpoints/methods"
        ]),
        ("Include Best Practices", [
            "Security considerations",
            "Performance optimization tips",
            "Production deployment advice",
            "Common pitfalls and solutions"
        ]),
        ("Add Troubleshooting", [
            "Common error messages and fixes",
            "Debugging techniques",
            "FAQ from documentation",
            "Community solutions"
        ]),
        ("Verify Completeness", [
            "All sections have real content",
            "Code examples are tested/valid",
            "Links are working",
            "Information is current"
        ])
    ]

    for i, (category, items) in enumerate(checklist, 1):
        print(f"{i}. {category}")
        for item in items:
            print(f"   ☐ {item}")
        print()

    print("💡 Tips for Enhancement:\n")
    tips = [
        "Use WebFetch to read documentation pages",
        "Clone GitHub repo to review example code",
        "Search for 'Quick Start' or 'Getting Started' sections",
        "Look for 'Examples' or 'Tutorials' directories",
        "Check for official blog posts or guides",
        "Review community resources and discussions"
    ]

    for tip in tips:
        print(f"  💡 {tip}")
    print()

    print("🚀 Next Steps:\n")
    print("1. Manually enhance SKILL.md using the checklist above")
    print("2. Or use Claude/LLM to help research and enhance:")
    print(f"   - Ask Claude to read documentation from URLs")
    print(f"   - Request specific examples and patterns")
    print(f"   - Have Claude extract key information")
    print()
    print("3. After enhancement, repackage the skill:")
    print(f"   cd {base_dir / 'output'}")
    print(f"   zip -r {skill_name}.zip {skill_name}/")
    print()

    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Skill Enhancement Helper",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "skill_name",
        help="Name of the skill to enhance"
    )

    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path.cwd(),
        help="Base directory for the project (default: current directory)"
    )

    args = parser.parse_args()

    try:
        enhance_skill(args.skill_name, args.base_dir)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
