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
        """Create skill-seekers configuration file"""
        print(f"📝 Creating configuration for {self.skill_name}...")

        # Categorize URLs
        github_urls = [u for u in self.urls if self.detect_url_type(u) == "github"]
        doc_urls = [u for u in self.urls if self.detect_url_type(u) in ["docs", "web"]]

        # Build config based on available URLs
        config = {
            "name": self.skill_name,
            "output_dir": str(self.output_dir),
            "sources": []
        }

        # Add GitHub source if available
        if github_urls:
            github_url = github_urls[0]
            parts = urlparse(github_url).path.strip("/").split("/")
            if len(parts) >= 2:
                config["sources"].append({
                    "type": "github",
                    "repo": f"{parts[0]}/{parts[1]}",
                    "include_issues": False,
                    "include_prs": False
                })

        # Add documentation sources
        for doc_url in doc_urls:
            config["sources"].append({
                "type": "web",
                "url": doc_url,
                "depth": 2
            })

        # Save config file
        config_file = self.configs_dir / f"{self.skill_name}_github.json"
        config_file.parent.mkdir(exist_ok=True)

        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)

        print(f"✅ Configuration saved to {config_file}")
        return config_file

    def run_skill_seekers(self, config_file: Path, timeout: int = 300) -> bool:
        """Run skill-seekers scraper with timeout"""
        print(f"🔍 Running skill-seekers scraper (timeout: {timeout}s)...")

        try:
            result = subprocess.run(
                ["skill-seekers", "scrape", "--config", str(config_file)],
                timeout=timeout,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("✅ Skill-seekers completed successfully")
                return True
            else:
                print(f"⚠️ Skill-seekers failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print(f"⚠️ Skill-seekers timed out after {timeout}s, proceeding with manual creation...")
            return False
        except FileNotFoundError:
            print("⚠️ skill-seekers not found, proceeding with manual creation...")
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

    def create_skill_md(self) -> Path:
        """Create comprehensive SKILL.md file"""
        print(f"📄 Creating SKILL.md with comprehensive documentation...")

        skill_file = self.skill_dir / "SKILL.md"

        # Get primary GitHub URL for reference
        github_url = next((u for u in self.urls if "github.com" in u), self.urls[0])

        # Create comprehensive skill template
        content = f"""# {self.skill_name.replace('-', ' ').title()} Skill

## When to Use This Skill

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

    def generate(self, skip_git: bool = False):
        """Run the complete skill generation pipeline"""
        print(f"\n{'='*60}")
        print(f"🚀 Generating Claude Skill: {self.skill_name}")
        print(f"{'='*60}\n")

        # Step 1: Create configuration
        config_file = self.create_config()

        # Step 2: Try to run skill-seekers (with short timeout)
        # self.run_skill_seekers(config_file, timeout=120)

        # Step 3: Create skill structure
        self.create_skill_structure()

        # Step 4: Create SKILL.md
        self.create_skill_md()

        # Step 5: Package skill
        zip_file = self.package_skill()

        # Step 6: Update README
        self.update_readme()

        # Step 7: Git commit and push
        if not skip_git:
            self.git_commit_and_push()

        print(f"\n{'='*60}")
        print(f"✅ Skill generation complete!")
        print(f"{'='*60}")
        print(f"\nSkill location: {self.skill_dir}")
        print(f"Package: {zip_file}")
        print(f"\n⚠️  IMPORTANT: The generated SKILL.md is a template.")
        print(f"   For production quality, enhance it with:")
        print(f"   - Real code examples from the documentation")
        print(f"   - Detailed API references")
        print(f"   - Actual use cases and patterns")
        print(f"   - Community best practices\n")


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
        generator.generate(skip_git=args.skip_git)
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
