# Skill Generation Examples

This document provides practical examples of using the skill generation scripts for various popular technologies.

## Quick Reference

```bash
# Basic usage
./create_skill.py <name> <url1> [url2] ...

# With options
./create_skill.py <name> <url1> --skip-git --base-dir /path

# Enhance existing skill
./enhance_skill.py <name>
```

## Web Frameworks

### FastAPI

```bash
./create_skill.py fastapi \
  https://fastapi.tiangolo.com \
  https://fastapi.tiangolo.com/tutorial/ \
  https://github.com/tiangolo/fastapi
```

### Django

```bash
./create_skill.py django \
  https://docs.djangoproject.com \
  https://docs.djangoproject.com/en/stable/intro/tutorial01/ \
  https://github.com/django/django
```

### Flask

```bash
./create_skill.py flask \
  https://flask.palletsprojects.com \
  https://flask.palletsprojects.com/en/stable/quickstart/ \
  https://github.com/pallets/flask
```

### Express.js

```bash
./create_skill.py expressjs \
  https://expressjs.com \
  https://expressjs.com/en/starter/installing.html \
  https://github.com/expressjs/express
```

## Databases

### PostgreSQL

```bash
./create_skill.py postgresql \
  https://www.postgresql.org/docs/ \
  https://www.postgresql.org/docs/current/tutorial.html \
  https://github.com/postgres/postgres
```

### MongoDB

```bash
./create_skill.py mongodb \
  https://www.mongodb.com/docs/ \
  https://www.mongodb.com/docs/manual/tutorial/getting-started/ \
  https://github.com/mongodb/mongo
```

### Redis

```bash
./create_skill.py redis \
  https://redis.io/docs/ \
  https://redis.io/docs/getting-started/ \
  https://github.com/redis/redis \
  https://github.com/redis/redis-py
```

## AI/ML Frameworks

### LangChain

```bash
./create_skill.py langchain \
  https://docs.langchain.com \
  https://docs.langchain.com/docs/get-started/introduction \
  https://github.com/langchain-ai/langchain
```

### LlamaIndex

```bash
./create_skill.py llamaindex \
  https://docs.llamaindex.ai \
  https://docs.llamaindex.ai/en/stable/getting_started/starter_example.html \
  https://github.com/run-llama/llama_index
```

### Transformers (Hugging Face)

```bash
./create_skill.py transformers \
  https://huggingface.co/docs/transformers \
  https://huggingface.co/docs/transformers/quicktour \
  https://github.com/huggingface/transformers
```

### PyTorch

```bash
./create_skill.py pytorch \
  https://pytorch.org/docs/stable/index.html \
  https://pytorch.org/tutorials/beginner/basics/intro.html \
  https://github.com/pytorch/pytorch
```

## DevOps Tools

### Docker

```bash
./create_skill.py docker \
  https://docs.docker.com \
  https://docs.docker.com/get-started/ \
  https://github.com/docker/cli
```

### Kubernetes

```bash
./create_skill.py kubernetes \
  https://kubernetes.io/docs/ \
  https://kubernetes.io/docs/tutorials/kubernetes-basics/ \
  https://github.com/kubernetes/kubernetes
```

### Terraform

```bash
./create_skill.py terraform \
  https://developer.hashicorp.com/terraform/docs \
  https://developer.hashicorp.com/terraform/tutorials/aws-get-started \
  https://github.com/hashicorp/terraform
```

## Testing Frameworks

### Pytest

```bash
./create_skill.py pytest \
  https://docs.pytest.org \
  https://docs.pytest.org/en/stable/getting-started.html \
  https://github.com/pytest-dev/pytest
```

### Jest

```bash
./create_skill.py jest \
  https://jestjs.io/docs/getting-started \
  https://github.com/jestjs/jest
```

## API Tools

### Postman

```bash
./create_skill.py postman \
  https://learning.postman.com/docs/getting-started/introduction/ \
  https://learning.postman.com/docs/sending-requests/requests/
```

### Swagger/OpenAPI

```bash
./create_skill.py openapi \
  https://swagger.io/docs/ \
  https://swagger.io/docs/specification/about/ \
  https://github.com/OAI/OpenAPI-Specification
```

## Data Processing

### Pandas

```bash
./create_skill.py pandas \
  https://pandas.pydata.org/docs/ \
  https://pandas.pydata.org/docs/getting_started/index.html \
  https://github.com/pandas-dev/pandas
```

### Apache Spark

```bash
./create_skill.py spark \
  https://spark.apache.org/docs/latest/ \
  https://spark.apache.org/docs/latest/quick-start.html \
  https://github.com/apache/spark
```

### Polars

```bash
./create_skill.py polars \
  https://docs.pola.rs \
  https://docs.pola.rs/user-guide/getting-started/ \
  https://github.com/pola-rs/polars
```

## Message Queues

### RabbitMQ

```bash
./create_skill.py rabbitmq \
  https://www.rabbitmq.com/documentation.html \
  https://www.rabbitmq.com/tutorials/tutorial-one-python.html \
  https://github.com/rabbitmq/rabbitmq-server
```

### Apache Kafka

```bash
./create_skill.py kafka \
  https://kafka.apache.org/documentation/ \
  https://kafka.apache.org/quickstart \
  https://github.com/apache/kafka
```

## Cloud Platforms

### AWS SDK (Boto3)

```bash
./create_skill.py boto3 \
  https://boto3.amazonaws.com/v1/documentation/api/latest/index.html \
  https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html \
  https://github.com/boto/boto3
```

### Google Cloud Python

```bash
./create_skill.py google-cloud \
  https://cloud.google.com/python/docs \
  https://cloud.google.com/python/docs/setup \
  https://github.com/googleapis/google-cloud-python
```

## Complete Workflow Example

Here's a complete example of creating and enhancing a skill:

### 1. Generate Skill

```bash
./create_skill.py streamlit \
  https://docs.streamlit.io \
  https://docs.streamlit.io/get-started \
  https://github.com/streamlit/streamlit \
  --skip-git
```

**Output:**
```
====================================================================
🚀 Generating Claude Skill: streamlit
====================================================================

📝 Creating configuration for streamlit...
✅ Configuration saved to configs/streamlit_github.json
📁 Creating skill directory structure...
✅ Directory structure created
📄 Creating SKILL.md with comprehensive documentation...
✅ SKILL.md created (8,234 bytes)
⚠️  Note: This is a template. For production-quality skills, enhance with:
   - Detailed examples from actual documentation
   - Code snippets from GitHub repository
   - Real-world use cases and patterns
📦 Packaging skill...
✅ Skill packaged as output/streamlit.zip (3,421 bytes)
📝 Updating README.md...
✅ README.md updated

====================================================================
✅ Skill generation complete!
====================================================================

Skill location: output/streamlit
Package: output/streamlit.zip
```

### 2. Check Enhancement Checklist

```bash
./enhance_skill.py streamlit
```

**Output:**
```
====================================================================
📝 Skill Enhancement Checklist: streamlit
====================================================================

Current skill file: output/streamlit/SKILL.md
Current size: 8,234 bytes

📚 Resources from config:
  - Documentation: https://docs.streamlit.io
  - Documentation: https://docs.streamlit.io/get-started
  - GitHub: https://github.com/streamlit/streamlit

✅ Enhancement Checklist:

1. Read Official Documentation
   ☐ Visit all documentation URLs
   ☐ Extract key concepts and terminology
   ...
```

### 3. Enhance with Claude

Use Claude to enhance the skill:

```
"Please enhance the Streamlit skill by:
1. Reading https://docs.streamlit.io
2. Adding real code examples for creating dashboards
3. Including widget usage patterns
4. Adding deployment best practices
5. Including troubleshooting for common issues"
```

### 4. Verify and Repackage

```bash
# Check the enhanced content
cat output/streamlit/SKILL.md | wc -c

# Repackage
cd output
rm streamlit.zip
zip -r streamlit.zip streamlit/
cd ..
```

### 5. Commit and Push

```bash
git add configs/streamlit_github.json output/streamlit/ output/streamlit.zip README.md
git commit -m "Add comprehensive Streamlit skill

- Complete documentation and examples
- Real code patterns for dashboard creation
- Widget usage and best practices
- Deployment and troubleshooting guides

Resources:
- https://docs.streamlit.io
- https://github.com/streamlit/streamlit"

git push -u origin claude/create-skills
```

## Batch Creation Script

Create multiple related skills:

```bash
#!/bin/bash
# create_ml_skills.sh

# Create ML/AI related skills
./create_skill.py scikit-learn \
  https://scikit-learn.org/stable/ \
  https://github.com/scikit-learn/scikit-learn

./create_skill.py tensorflow \
  https://www.tensorflow.org/api_docs \
  https://github.com/tensorflow/tensorflow

./create_skill.py keras \
  https://keras.io/api/ \
  https://github.com/keras-team/keras

./create_skill.py xgboost \
  https://xgboost.readthedocs.io/ \
  https://github.com/dmlc/xgboost

echo "✅ All ML skills created!"
```

## Tips for Different Types of Technologies

### For Python Libraries

```bash
./create_skill.py <library> \
  https://<library>.readthedocs.io/ \
  https://github.com/<org>/<library>
```

### For JavaScript Frameworks

```bash
./create_skill.py <framework> \
  https://<framework>.dev \
  https://github.com/<org>/<framework>
```

### For Cloud Services

```bash
./create_skill.py <service> \
  https://docs.<cloud>.com/<service> \
  https://github.com/<org>/<sdk>
```

### For APIs/Protocols

```bash
./create_skill.py <api> \
  https://spec.<api>.io \
  https://github.com/<org>/<implementation>
```

## Common Patterns

### Documentation Heavy

```bash
./create_skill.py <name> \
  https://docs.example.com \
  https://docs.example.com/guides \
  https://docs.example.com/api \
  https://github.com/example/repo
```

### GitHub Heavy

```bash
./create_skill.py <name> \
  https://github.com/example/repo \
  https://github.com/example/repo/wiki \
  https://example.github.io
```

### Multi-source

```bash
./create_skill.py <name> \
  https://official-docs.com \
  https://github.com/official/repo \
  https://tutorial-site.com \
  https://community.example.com/docs
```

## Verification Checklist

After creating a skill, verify:

```bash
# 1. Check files exist
ls -lh output/<skill_name>/
ls -lh output/<skill_name>.zip
ls -lh configs/<skill_name>_github.json

# 2. Check SKILL.md size (should be > 5KB for good skills)
wc -c output/<skill_name>/SKILL.md

# 3. Verify README was updated
grep -A 5 "<skill_name>" README.md

# 4. Test the zip
unzip -t output/<skill_name>.zip

# 5. Check git status
git status
```

## Troubleshooting Examples

### Issue: Network timeout during creation

```bash
# Solution: Skip git operations and do manually
./create_skill.py <name> <url> --skip-git

# Then manually:
git add .
git commit -m "Add <name> skill"
git push
```

### Issue: Skill already exists

```bash
# Solution: Remove old skill first
rm -rf output/<name>
rm output/<name>.zip
rm configs/<name>_github.json

# Then recreate
./create_skill.py <name> <url>
```

### Issue: Want to recreate with new URLs

```bash
# Solution: Delete and regenerate
rm -rf output/<name> output/<name>.zip

# Edit config if you want to keep it
vim configs/<name>_github.json

# Or delete and recreate
rm configs/<name>_github.json
./create_skill.py <name> <new_url1> <new_url2>
```

---

**Last Updated**: 2025-12-15
**Examples Version**: 1.0.0
