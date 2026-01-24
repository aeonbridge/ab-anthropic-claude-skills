# Como Claude Code Descobre e Usa Skills Automaticamente

## Overview

Claude Code escaneia automaticamente os diretórios de skills e usa **pattern matching** na descrição do frontmatter YAML para decidir quando carregar cada skill.

## Descoberta Automática

### 1. Locais de Escaneamento

Claude Code escaneia (em ordem de prioridade):

```
1. ~/.claude/skills/          # Global - todos os projetos
2. .claude/skills/             # Local - apenas este projeto
```

### 2. Detecção de Skill

Para cada diretório em `skills/`, Claude:

1. Procura por `SKILL.md`
2. Lê o frontmatter YAML
3. Extrai `name` e `description`
4. Indexa para matching posterior

**Exemplo:**

```yaml
---
name: agno
description: Comprehensive skill for building, deploying, and managing multi-agent AI systems with Agno framework
---
```

### 3. Pattern Matching

Quando você faz uma pergunta, Claude compara com as descrições:

| User Prompt | Description Match | Skill Loaded |
|-------------|-------------------|--------------|
| "Create an Agno agent" | ✅ "Agno" in description | agno |
| "Build multi-agent system" | ✅ "multi-agent AI systems" | agno |
| "Setup RAG pipeline" | ✅ Agno description mentions it | agno |
| "Deploy agents" | ✅ "deploying" in description | agno |

## Keywords que Ativam o Skill Agno

Baseado no frontmatter atual:

```yaml
description: Comprehensive skill for building, deploying, and managing multi-agent AI systems with Agno framework
```

**Triggers primários:**
- "Agno" (nome explícito)
- "multi-agent" (no description)
- "AI systems" (no description)
- "agent" (singular também funciona)
- "deploying" (no description)

**Triggers secundários (contextuais):**
- "framework" + "AI"
- "manage agents"
- "build agents"

## Melhorando a Descoberta

### Opção 1: Otimizar Description (Recomendado)

Se você quer que Claude use o skill em mais contextos, expanda a descrição:

```yaml
---
name: agno
description: Build multi-agent AI systems, RAG applications, autonomous workflows, and production-ready agents with Agno framework. Supports teams, workflows, tools, memory, and knowledge bases.
---
```

**Novos triggers:**
- "RAG" / "RAG application"
- "autonomous workflow"
- "production agent"
- "knowledge base"
- "workflow"

### Opção 2: Adicionar no CLAUDE.md do Projeto

Para garantir uso em projeto específico:

```markdown
# .claude/CLAUDE.md

## AI Agent Development

**IMPORTANT:** Use the Agno skill for all AI agent development tasks.

Triggers that should load Agno skill:
- Creating agents
- Multi-agent systems
- RAG implementations
- Autonomous workflows
- Agent teams and orchestration

Skill location: `~/.claude/skills/agno/`
```

### Opção 3: Prompt Explícito

Sempre funciona:

```
Use the Agno skill to create a customer support agent
```

## Hierarquia de Decisão

Quando Claude decide usar um skill:

```
1. Prompt explícito ("Use the agno skill")
   ↓
2. CLAUDE.md do projeto (instruções específicas)
   ↓
3. Description matching (keywords na descrição)
   ↓
4. Context analysis (entende intenção)
```

## Verificando se Skill Foi Carregado

### Indicadores

Durante a conversa, procure por:

1. **Importações específicas:**
   ```python
   from agno.agent import Agent  # ✅ Skill carregado
   ```

2. **Padrões do framework:**
   ```python
   agent = Agent(
       model=OpenAIChat(id="gpt-4"),  # ✅ Padrão Agno
       instructions="..."
   )
   ```

3. **Menções ao skill:**
   > "Using the Agno framework as specified in the skill..."

### Debug Mode (Manual)

```bash
# Verifique se Claude consegue ver o skill
# Em uma conversa, pergunte:
"What skills do you have available for building AI agents?"

# Claude deve mencionar:
# - agno skill
# - Location: ~/.claude/skills/agno/
# - Description: ...
```

## Múltiplos Skills

Se você tiver vários skills de agent frameworks:

```
~/.claude/skills/
├── agno/          # Agno framework
├── langchain/     # LangChain
├── crewai/        # CrewAI
└── autogen/       # AutoGen
```

**Como Claude escolhe:**

1. **Prompt explícito vence:**
   - "Use Agno" → carrega agno
   - "Use LangChain" → carrega langchain

2. **Description matching:**
   - "multi-agent system" → pode carregar agno OU crewai
   - Claude pode perguntar qual preferir

3. **CLAUDE.md preference:**
   ```markdown
   ## Preferred Frameworks
   - AI Agents: Agno (default)
   - RAG: Agno or LangChain
   ```

## Ordem de Carregamento

### Progressive Disclosure

Claude não carrega tudo de uma vez:

```
Etapa 1: User prompt "Create an Agno agent"
         ↓
         Scan skills → match "Agno" in description
         ↓
Etapa 2: Load SKILL.md (20KB)
         ↓
         SKILL.md tem overview suficiente
         ↓
Etapa 3: User pergunta "Show all model options"
         ↓
         SKILL.md menciona "see references/llms.md"
         ↓
Etapa 4: Load references/llms.md (203KB)
         ↓
         Retorna opções completas
```

**Benefício:** Eficiência de contexto - carrega apenas o necessário.

## Troubleshooting

### Problema: Skill não está sendo usado

**Diagnóstico:**
```bash
# 1. Verifique instalação
ls -la ~/.claude/skills/agno/SKILL.md

# 2. Valide frontmatter
head -5 ~/.claude/skills/agno/SKILL.md

# 3. Teste description
grep "^description:" ~/.claude/skills/agno/SKILL.md
```

**Soluções:**

1. **Reinstalar:**
   ```bash
   ./install-agno-skill.sh global
   ```

2. **Melhorar description:**
   - Adicione mais keywords relevantes
   - Expanda casos de uso

3. **Adicionar no CLAUDE.md:**
   - Instruções explícitas
   - Preferred frameworks

4. **Usar prompt explícito:**
   - "Use the agno skill to..."

### Problema: Skill carregado mas references/ não encontrada

**Diagnóstico:**
```bash
# Verifique estrutura completa
tree ~/.claude/skills/agno/

# Deve mostrar:
# agno/
# ├── SKILL.md
# └── references/
#     ├── llms.md
#     ├── llms-full.md
#     └── ...
```

**Solução:**
```bash
# Copie estrutura COMPLETA
cp -r output/agno/ ~/.claude/skills/
```

### Problema: Claude usa skill errado

**Exemplo:** Usa LangChain quando você queria Agno

**Solução 1 - Prompt explícito:**
```
Use the Agno skill to build a multi-agent system
```

**Solução 2 - CLAUDE.md preference:**
```markdown
## Framework Preferences
- Multi-agent systems: Always use Agno skill
```

## Performance

### Benchmarks Esperados

| Métrica | Valor Esperado |
|---------|----------------|
| Skill detection | < 100ms |
| SKILL.md load | < 500ms |
| Reference load | < 1s |
| First response | < 3s |

### Otimização

Para projetos grandes com muitos skills:

1. **Local > Global:**
   - Coloque skills usados frequentemente em `.claude/skills/`
   - Mantém outros em `~/.claude/skills/`

2. **SKILL.md conciso:**
   - < 500 linhas
   - Move detalhes para references/

3. **Description precisa:**
   - Keywords relevantes
   - Evita ambiguidade

## Exemplos Práticos

### Exemplo 1: Auto-Discovery Funcionando

```
User: "I need to build a customer support agent"

Claude internamente:
1. Scan skills → encontra agno
2. Match "agent" in description ✅
3. Load ~/.claude/skills/agno/SKILL.md
4. Gera código Agno:

from agno.agent import Agent
agent = Agent(...)
```

### Exemplo 2: Multiple Skills

```
User: "Compare Agno and LangChain for my use case"

Claude internamente:
1. Scan skills → encontra agno + langchain
2. Load ambos os SKILL.md
3. Compara baseado em descriptions
4. Apresenta comparação

User: "I'll use Agno"

Claude:
5. Foca em agno skill daqui pra frente
6. Gera código apenas Agno
```

### Exemplo 3: Progressive Disclosure

```
User: "Create an Agno agent with all bells and whistles"

Claude:
1. Load SKILL.md → overview básico
2. Vê mention: "see references/llms.md for complete API"
3. Load references/llms.md
4. Gera código com configuração avançada
5. Cita: "Based on references/llms.md, here's the full configuration..."
```

## Checklist de Validação

Use este checklist para garantir que auto-discovery está funcionando:

- [ ] Skill instalado em `~/.claude/skills/agno/` ou `.claude/skills/agno/`
- [ ] SKILL.md tem frontmatter YAML válido
- [ ] Description tem keywords relevantes
- [ ] Estrutura completa (SKILL.md + references/ + scripts/)
- [ ] Prompt de teste funciona: "Create an Agno agent"
- [ ] References são carregadas quando necessário
- [ ] Código gerado usa importações corretas do Agno

## Recursos Adicionais

- **Teste completo:** `TEST_AGNO_SKILL.md`
- **Template CLAUDE.md:** `CLAUDE.md.template`
- **Script de instalação:** `install-agno-skill.sh`
- **Documentação oficial:** https://code.claude.com/docs/en/skills

---

**Resumo:** Claude Code descobre skills automaticamente através de:
1. Escanear `~/.claude/skills/` e `.claude/skills/`
2. Ler frontmatter YAML
3. Fazer pattern matching entre user prompt e description
4. Carregar SKILL.md + references/ progressivamente

**Action:** Certifique-se que skill tem description clara com keywords relevantes!