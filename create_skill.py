#!/usr/bin/env python3
"""
Automated Claude Skill Generator

This script automates the creation of comprehensive Claude skills using skill-seekers
and web research. It follows the established pattern used in this repository.

Usage:
    python create_skill.py <skill_name> <url1> [url2] [url3] ...

Example:
    python create_skill.py fastapi https://fastapi.tiangolo.com https://github.com/tiangolo/fastapi
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Dict
from urllib.parse import urlparse


class SkillGenerator:
    """Automated skill generator following established patterns"""

    def __init__(self, skill_name: str, urls: List[str], base_dir: Path = None):
        self.skill_name = skill_name.lower().replace(" ", "-")
        self.urls = urls
        self.base_dir = base_dir or Path.cwd()
        self.configs_dir = self.base_dir / "configs"
        self.output_dir = self.base_dir / "output"
        self.skill_dir = self.output_dir / self.skill_name

    def detect_url_type(self, url: str) -> str:
        """Detect if URL is GitHub, docs, or other"""
        parsed = urlparse(url)

        if "github.com" in parsed.netloc:
            return "github"
        elif any(doc in url.lower() for doc in ["docs.", "doc.", "documentation", "/docs/"]):
            return "docs"
        else:
            return "web"

    def create_config(self) -> Path:
        """Create skill-seekers configuration file in unified format"""
        print(f"📝 Creating configuration for {self.skill_name}...")

        # Categorize URLs
        github_urls = [u for u in self.urls if self.detect_url_type(u) == "github"]
        doc_urls = [u for u in self.urls if self.detect_url_type(u) in ["docs", "web"]]

        # Build config in "unified" format compatible with skill-seekers
        skill_title = self.skill_name.replace('-', ' ').title()

        config = {
            "name": self.skill_name,
            "display_name": skill_title,
            "description": f"Comprehensive skill for {skill_title}",
            "sources": {},
            "output_dir": str(self.skill_dir),
            "metadata": {
                "author": "skill-seekers",
                "category": "Development Tools"
            }
        }

        # Add GitHub source if available
        if github_urls:
            github_url = github_urls[0]
            parts = urlparse(github_url).path.strip("/").split("/")
            if len(parts) >= 2:
                config["sources"]["github"] = {
                    "enabled": True,
                    "repository": f"{parts[0]}/{parts[1]}",
                    "include_readme": True,
                    "include_code_samples": True,
                    "max_files": 200,
                    "file_patterns": [
                        "*.md",
                        "*.py",
                        "*.js",
                        "*.ts",
                        "README*",
                        "examples/**/*"
                    ],
                    "exclude_patterns": [
                        "tests/",
                        "__pycache__/",
                        "*.pyc",
                        ".git/",
                        "node_modules/"
                    ]
                }

        # Add documentation sources
        if doc_urls:
            base_url = doc_urls[0]
            config["sources"]["documentation"] = {
                "enabled": True,
                "base_url": base_url,
                "start_urls": doc_urls,
                "max_depth": 3,
                "max_pages": 500,
                "extract_api": True
            }

        # Save config file
        config_file = self.configs_dir / f"{self.skill_name}_unified.json"
        config_file.parent.mkdir(exist_ok=True)

        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)

        print(f"✅ Configuration saved to {config_file}")
        print(f"   Format: unified (compatible with skill-seekers)")
        return config_file

    def run_skill_seekers(self, config_file: Path, timeout: int = 600) -> bool:
        """Run skill-seekers unified scraper with timeout"""
        print(f"🔍 Running skill-seekers unified scraper...")
        print(f"   Timeout: {timeout}s ({timeout//60} minutes)")
        print(f"   This may take a while for large documentation sites...")

        try:
            # Use "unified" command for multi-source scraping
            result = subprocess.run(
                ["skill-seekers", "unified", "--config", str(config_file)],
                timeout=timeout,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("✅ Skill-seekers completed successfully")
                print(f"   Output: {result.stdout[:200] if result.stdout else 'No output'}")
                return True
            else:
                print(f"⚠️ Skill-seekers failed with return code {result.returncode}")
                if result.stderr:
                    print(f"   Error: {result.stderr[:500]}")
                if result.stdout:
                    print(f"   Output: {result.stdout[:500]}")
                return False

        except subprocess.TimeoutExpired:
            print(f"⚠️ Skill-seekers timed out after {timeout}s ({timeout//60} minutes)")
            print(f"   This can happen with very large documentation sites.")
            print(f"   Proceeding with manual creation...")
            return False
        except FileNotFoundError:
            print("⚠️ skill-seekers command not found")
            print("   Install with: pip install skill-seekers")
            print("   Proceeding with manual creation...")
            return False
        except Exception as e:
            print(f"⚠️ Unexpected error running skill-seekers: {e}")
            print("   Proceeding with manual creation...")
            return False

    def create_skill_structure(self):
        """Create skill directory structure"""
        print(f"📁 Creating skill directory structure...")

        self.skill_dir.mkdir(parents=True, exist_ok=True)
        (self.skill_dir / "assets").mkdir(exist_ok=True)
        (self.skill_dir / "scripts").mkdir(exist_ok=True)
        (self.skill_dir / "references").mkdir(exist_ok=True)

        # Create .gitkeep files
        for subdir in ["assets", "scripts", "references"]:
            (self.skill_dir / subdir / ".gitkeep").touch()

        print("✅ Directory structure created")

    def create_frontmatter(self) -> str:
        """Create YAML frontmatter for SKILL.md"""
        # Ensure name follows Claude AI format requirements
        # lowercase letters, numbers, and hyphens only, max 64 chars
        skill_title = self.skill_name.replace('-', ' ').title()

        description = (
            f"Comprehensive skill for {skill_title}. "
            f"Use when working with {self.skill_name}, implementing features, "
            f"deploying applications, or troubleshooting. "
            f"Includes installation, configuration, best practices, and examples."
        )

        # Ensure description is within 1024 character limit
        if len(description) > 1024:
            description = description[:1021] + "..."

        frontmatter = f"""---
name: {self.skill_name}
description: {description}
---

"""
        return frontmatter

    def create_skill_md(self) -> Path:
        """Create comprehensive SKILL.md file"""
        print(f"📄 Creating SKILL.md with comprehensive documentation...")

        skill_file = self.skill_dir / "SKILL.md"

        # Get primary GitHub URL for reference
        github_url = next((u for u in self.urls if "github.com" in u), self.urls[0])

        # Create YAML frontmatter
        frontmatter = self.create_frontmatter()

        # Create comprehensive skill template
        content = frontmatter + f"""## When to Use This Skill

Use this skill when you need to work with {self.skill_name}, including:
- Understanding core concepts and architecture
- Implementing features and integrations
- Configuring and deploying applications
- Troubleshooting common issues
- Following best practices

## Overview

This skill provides comprehensive guidance for working with {self.skill_name}.

**Key Resources:**
{chr(10).join(f"- {url}" for url in self.urls)}

## Installation

### Prerequisites

Check the official documentation for specific prerequisites.

### Basic Installation

```bash
# Installation instructions will vary by technology
# Refer to official documentation
```

## Quick Start

### Basic Example

```python
# Example code for {self.skill_name}
# This will be technology-specific
```

## Core Concepts

### Architecture

{self.skill_name.replace('-', ' ').title()} follows modern architecture patterns.

### Key Components

1. **Component 1**: Description
2. **Component 2**: Description
3. **Component 3**: Description

## Configuration

### Basic Configuration

```yaml
# Example configuration
# Technology-specific settings
```

### Environment Variables

Common environment variables:
- `VAR_NAME`: Description

## Common Patterns

### Pattern 1: Basic Usage

```python
# Example implementation
```

### Pattern 2: Advanced Usage

```python
# Advanced example
```

## API Reference

### Core APIs

Refer to official documentation for complete API reference:
{chr(10).join(f"- {url}" for url in self.urls)}

## Integration Examples

### Example 1: Basic Integration

```python
# Integration example
```

### Example 2: Advanced Integration

```python
# Advanced integration
```

## Best Practices

### Development

1. **Follow conventions**: Adhere to community standards
2. **Use type hints**: Improve code quality
3. **Write tests**: Ensure reliability
4. **Document code**: Help future maintainers

### Production

1. **Security**: Implement proper authentication and authorization
2. **Performance**: Optimize for production workloads
3. **Monitoring**: Set up logging and metrics
4. **Scalability**: Design for growth

### Common Pitfalls

1. **Issue**: Description
   - **Solution**: How to fix

2. **Issue**: Description
   - **Solution**: How to fix

## Troubleshooting

### Common Issues

#### Issue 1: Problem Description

**Symptoms:**
- Symptom description

**Solution:**
```bash
# Solution command or code
```

#### Issue 2: Problem Description

**Symptoms:**
- Symptom description

**Solution:**
- Resolution steps

### Debugging Tips

1. Check logs for error messages
2. Verify configuration settings
3. Ensure dependencies are installed
4. Review documentation for updates

## Advanced Topics

### Topic 1: Advanced Feature

Description and implementation details.

### Topic 2: Optimization

Performance optimization techniques.

### Topic 3: Scaling

Scaling strategies for production.

## Resources

### Official Documentation
{chr(10).join(f"- {url}" for url in self.urls)}

### Community Resources
- Community forums and discussions
- Example repositories
- Video tutorials

### Related Tools
- Tool 1: Description
- Tool 2: Description

## Contributing

Refer to the official repository for contribution guidelines:
{github_url}

## Version Information

**Last Updated**: {time.strftime("%Y-%m-%d")}
**Skill Version**: 1.0.0

---

*Note: This skill is generated from official documentation and community resources. Always refer to the latest official documentation for the most up-to-date information.*
"""

        with open(skill_file, "w") as f:
            f.write(content)

        file_size = skill_file.stat().st_size
        print(f"✅ SKILL.md created ({file_size:,} bytes)")
        print(f"⚠️  Note: This is a template. For production-quality skills, enhance with:")
        print(f"   - Detailed examples from actual documentation")
        print(f"   - Code snippets from GitHub repository")
        print(f"   - Real-world use cases and patterns")

        return skill_file

    def package_skill(self) -> Path:
        """Package skill as zip file"""
        print(f"📦 Packaging skill...")

        zip_file = self.output_dir / f"{self.skill_name}.zip"

        # Remove existing zip if present
        if zip_file.exists():
            zip_file.unlink()

        # Create zip
        result = subprocess.run(
            ["zip", "-r", str(zip_file.name), str(self.skill_dir.name)],
            cwd=self.output_dir,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            file_size = zip_file.stat().st_size
            print(f"✅ Skill packaged as {zip_file} ({file_size:,} bytes)")
            return zip_file
        else:
            print(f"❌ Failed to create zip: {result.stderr}")
            return None

    def update_readme(self):
        """Update README.md with new skill"""
        print(f"📝 Updating README.md...")

        readme_file = self.base_dir / "README.md"

        if not readme_file.exists():
            print("⚠️ README.md not found, skipping update")
            return

        # Read current README
        with open(readme_file, "r") as f:
            content = f.read()

        # Check if skill already exists in README
        if self.skill_name in content.lower():
            print(f"⚠️ Skill {self.skill_name} already exists in README.md")
            return

        # Create skill section
        skill_title = self.skill_name.replace('-', ' ').title()
        github_url = next((u for u in self.urls if "github.com" in u), self.urls[0])

        new_section = f"""
### {skill_title} Skill

**Version:** 1.0.0
**Description:** Comprehensive skill for {skill_title}.

**What's Included:**
- Complete documentation and examples
- API reference and best practices
- Integration guides
- Troubleshooting tips

**Usage:**
1. Use the packaged skill: `output/{self.skill_name}.zip`
2. Or explore the skill directory: `output/{self.skill_name}/`
3. Main skill file: `output/{self.skill_name}/SKILL.md`

**Key Features:**
- Feature 1
- Feature 2
- Feature 3

"""

        # Find insertion point (before "## How to Create Skills")
        insertion_marker = "## How to Create Skills"

        if insertion_marker in content:
            parts = content.split(insertion_marker, 1)
            updated_content = parts[0] + new_section + insertion_marker + parts[1]

            # Add to config files list
            config_section = "## Configuration Files"
            if config_section in updated_content:
                # Find the last config line
                lines = updated_content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith('- `') and '_github.json`' in line:
                        last_config_line = i

                # Insert new config line after the last one
                new_config_line = f"- `{self.skill_name}_github.json` - GitHub configuration for {skill_title}"
                lines.insert(last_config_line + 1, new_config_line)
                updated_content = '\n'.join(lines)

            # Add to resources section
            resource_section = f"""
### {skill_title}
{chr(10).join(f"- **URL**: {url}" for url in self.urls)}
"""

            if "### Tools" in updated_content:
                parts = updated_content.split("### Tools", 1)
                updated_content = parts[0] + resource_section + "\n### Tools" + parts[1]

            with open(readme_file, "w") as f:
                f.write(updated_content)

            print("✅ README.md updated")
        else:
            print("⚠️ Could not find insertion point in README.md")

    def git_commit_and_push(self):
        """Commit and push changes to git"""
        print(f"🔄 Committing and pushing to git...")

        # Check if we're in a git repository
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=self.base_dir,
            capture_output=True
        )

        if result.returncode != 0:
            print("⚠️ Not a git repository, skipping git operations")
            return

        # Get current branch
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=self.base_dir,
            capture_output=True,
            text=True
        )
        current_branch = result.stdout.strip()

        # Add files
        files_to_add = [
            f"configs/{self.skill_name}_github.json",
            f"output/{self.skill_name}/",
            f"output/{self.skill_name}.zip",
            "README.md"
        ]

        subprocess.run(
            ["git", "add"] + files_to_add,
            cwd=self.base_dir
        )

        # Create commit message
        commit_msg = f"""Add comprehensive {self.skill_name.replace('-', ' ').title()} skill

This commit adds a new Claude skill for {self.skill_name.replace('-', ' ')}.

Changes:
- Created configs/{self.skill_name}_github.json configuration file
- Created output/{self.skill_name}/SKILL.md with comprehensive guide
- Packaged skill as output/{self.skill_name}.zip
- Updated README.md with {self.skill_name} skill documentation

Resources:
{chr(10).join(f"- {url}" for url in self.urls)}
"""

        # Commit
        result = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=self.base_dir,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"✅ Changes committed")

            # Push with retry logic
            max_retries = 4
            retry_delays = [2, 4, 8, 16]

            for attempt in range(max_retries):
                print(f"📤 Pushing to {current_branch} (attempt {attempt + 1}/{max_retries})...")

                result = subprocess.run(
                    ["git", "push", "-u", "origin", current_branch],
                    cwd=self.base_dir,
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    print(f"✅ Pushed to {current_branch}")
                    return
                else:
                    if attempt < max_retries - 1:
                        delay = retry_delays[attempt]
                        print(f"⚠️ Push failed, retrying in {delay}s...")
                        time.sleep(delay)
                    else:
                        print(f"❌ Push failed after {max_retries} attempts: {result.stderr}")
        else:
            print(f"⚠️ Nothing to commit or commit failed: {result.stderr}")

    def generate(self, skip_git: bool = False, skip_skill_seekers: bool = False):
        """Run the complete skill generation pipeline with hybrid approach"""
        print(f"\n{'='*60}")
        print(f"🚀 Generating Claude Skill: {self.skill_name}")
        print(f"{'='*60}\n")

        # Step 1: Create configuration
        config_file = self.create_config()

        # Step 2: Run skill-seekers to populate references/ directory
        seekers_success = False
        if not skip_skill_seekers:
            print("\n" + "="*60)
            print("STEP 2: Running skill-seekers (Hybrid Approach)")
            print("="*60)
            seekers_success = self.run_skill_seekers(config_file, timeout=600)

            if seekers_success:
                print("✅ References populated by skill-seekers")
                print("   Check output/{}/references/ for extracted documentation".format(self.skill_name))
            else:
                print("⚠️  Skill-seekers did not complete successfully")
                print("   References will need to be populated manually or via enhancement")
        else:
            print("\n⏭️  Skipping skill-seekers (--skip-skill-seekers flag)")

        # Step 3: Create skill structure (if not already created by skill-seekers)
        print("\n" + "="*60)
        print("STEP 3: Ensuring directory structure")
        print("="*60)
        self.create_skill_structure()

        # Step 4: Create or update SKILL.md template
        print("\n" + "="*60)
        print("STEP 4: Creating SKILL.md template")
        print("="*60)

        skill_md_file = self.skill_dir / "SKILL.md"
        if skill_md_file.exists() and seekers_success:
            print("ℹ️  SKILL.md already exists (created by skill-seekers)")
            print("   Preserving existing content")
        else:
            self.create_skill_md()

        # Step 5: Package skill
        print("\n" + "="*60)
        print("STEP 5: Packaging skill")
        print("="*60)
        zip_file = self.package_skill()

        # Step 6: Update README
        print("\n" + "="*60)
        print("STEP 6: Updating README.md")
        print("="*60)
        self.update_readme()

        # Step 7: Git commit and push
        if not skip_git:
            print("\n" + "="*60)
            print("STEP 7: Git operations")
            print("="*60)
            self.git_commit_and_push()
        else:
            print("\n⏭️  Skipping git operations (--skip-git flag)")

        # Final summary
        print(f"\n{'='*60}")
        print(f"✅ Skill generation complete!")
        print(f"{'='*60}")
        print(f"\nSkill location: {self.skill_dir}")
        print(f"Package: {zip_file}")

        # Check references directory
        refs_dir = self.skill_dir / "references"
        if refs_dir.exists():
            ref_files = list(refs_dir.glob("*.md"))
            if ref_files:
                print(f"\n📚 References populated: {len(ref_files)} files")
                for ref_file in ref_files[:5]:  # Show first 5
                    size = ref_file.stat().st_size
                    print(f"   - {ref_file.name} ({size:,} bytes)")
                if len(ref_files) > 5:
                    print(f"   ... and {len(ref_files) - 5} more")
            else:
                print(f"\n⚠️  References directory is empty")
                print(f"   Consider running skill-seekers manually or enhancing with Claude")

        print(f"\n{'='*60}")
        print(f"NEXT STEPS")
        print(f"{'='*60}")

        if seekers_success:
            print("✅ Skill-seekers populated references successfully")
            print("\n1. Review the extracted documentation in output/{}/references/".format(self.skill_name))
            print("2. Enhance SKILL.md with specific examples and use cases")
            print("3. Run: ./enhance_skill.py {}".format(self.skill_name))
        else:
            print("⚠️  Manual enhancement required")
            print("\n1. Option A: Run skill-seekers manually:")
            print("   skill-seekers unified --config configs/{}_unified.json".format(self.skill_name))
            print("\n2. Option B: Enhance SKILL.md manually with:")
            print("   - Real code examples from the documentation")
            print("   - Detailed API references")
            print("   - Actual use cases and patterns")
            print("   - Community best practices")
            print("\n3. Repackage after enhancement:")
            print("   cd output && rm {}.zip && zip -r {}.zip {}/".format(
                self.skill_name, self.skill_name, self.skill_name))
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Automated Claude Skill Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_skill.py fastapi https://fastapi.tiangolo.com https://github.com/tiangolo/fastapi
  python create_skill.py "redis cache" https://redis.io/docs https://github.com/redis/redis-py
  python create_skill.py langchain https://docs.langchain.com --skip-git
        """
    )

    parser.add_argument(
        "skill_name",
        help="Name of the skill to generate (e.g., 'fastapi', 'redis-cache')"
    )

    parser.add_argument(
        "urls",
        nargs="+",
        help="URLs for documentation, GitHub repos, etc."
    )

    parser.add_argument(
        "--skip-git",
        action="store_true",
        help="Skip git commit and push operations"
    )

    parser.add_argument(
        "--skip-skill-seekers",
        action="store_true",
        help="Skip skill-seekers execution (manual mode only)"
    )

    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path.cwd(),
        help="Base directory for the project (default: current directory)"
    )

    args = parser.parse_args()

    # Validate base directory
    if not args.base_dir.exists():
        print(f"❌ Error: Base directory does not exist: {args.base_dir}")
        sys.exit(1)

    # Create generator and run
    generator = SkillGenerator(
        skill_name=args.skill_name,
        urls=args.urls,
        base_dir=args.base_dir
    )

    try:
        generator.generate(
            skip_git=args.skip_git,
            skip_skill_seekers=args.skip_skill_seekers
        )
    except KeyboardInterrupt:
        print("\n\n⚠️ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during skill generation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
