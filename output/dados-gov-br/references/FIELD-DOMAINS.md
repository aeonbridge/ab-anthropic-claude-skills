# Dados.gov.br API - Domínios de Campos (Field Domains)

**Data**: 2026-01-20
**Fonte**: Swagger UI - Seção Schemas
**URL**: https://dados.gov.br/swagger-ui/index.html

---

## 📋 Índice

1. [ConjuntoDadosDTO (Dataset)](#conjuntodadosdto-dataset)
2. [RecursoDTO (Resource)](#recursodto-resource)
3. [OrganizacaoCkanDTO (Organization)](#organizacaockandto-organization)
4. [TagDTO (Tag)](#tagdto-tag)
5. [Enumerações Globais](#enumerações-globais)

---

## ConjuntoDadosDTO (Dataset)

Schema principal para conjuntos de dados (datasets).

### Campos e Tipos

| Campo | Tipo | Formato | Restrições | Obrigatório |
|-------|------|---------|------------|-------------|
| `id` | string | - | - | ✅ |
| `title` | string | - | - | ✅ |
| `notes` | string | - | Descrição do dataset | - |
| `dataUltimaAtualizacaoRecurso` | string | date-time | ISO 8601 | - |
| `tags` | array<object> | - | Array de TagDTO | - |
| `resources` | array<object> | - | Array de RecursoDTO | - |
| `organization` | object | - | OrganizacaoCkanDTO | - |
| `package_id` | string | - | ID do pacote | - |
| `metadata_modified` | string | - | Data última modificação | - |
| `last_modified` | string | date-time | Data última modificação | - |
| `url_check` | string | - | URL de verificação | - |
| `urlDisponivel` | boolean | - | URL está disponível | - |
| `idTipo` | integer | int32 | Tipo de dataset | - |

### Tags (Subschema)

Dentro de `tags`:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | string | ID da tag |
| `name` | string | Nome da tag |
| `display_name` | string | Nome de exibição |

### Resources (Subschema)

Dentro de `resources`:

| Campo | Tipo | Formato | Restrições |
|-------|------|---------|------------|
| `id` | string | - | ID do recurso |
| `format` | string | - | Formato do arquivo |
| `url` | string | - | URL do recurso |
| `name` | string | - | Nome do recurso |
| `description` | string | - | Descrição |
| `created` | string | date-time | Data de criação |
| `size` | integer | int64 | Tamanho em bytes |
| `tipo` | string | **ENUM** | Tipo de recurso |
| `nomeArquivo` | string | - | Nome do arquivo |
| `quantidadeDownloads` | integer | int32 | Contador de downloads |
| `numOrdem` | integer | int32 | Ordem de exibição |

#### 🔑 ENUM: tipo (Tipo de Recurso)

```json
{
  "0": "INVALIDO",
  "1": "DADOS",
  "2": "DOCUMENTACAO",
  "3": "DICIONARIO_DE_DADOS",
  "4": "API",
  "5": "OUTRO"
}
```

**Valores válidos**:
- `#0` ou `"INVALIDO"` - Tipo inválido
- `#1` ou `"DADOS"` - Dados estruturados (CSV, JSON, XML, etc.)
- `#2` ou `"DOCUMENTACAO"` - Documentação (PDF, DOC, etc.)
- `#3` ou `"DICIONARIO_DE_DADOS"` - Dicionário de dados
- `#4` ou `"API"` - Endpoint de API
- `#5` ou `"OUTRO"` - Outros tipos

### RecursoForm (Subschema detalhado)

Campos adicionais para recursos:

| Campo | Tipo | Formato | Restrições |
|-------|------|---------|------------|
| `idConjuntoDados` | string | - | ID do dataset pai |
| `titulo` | string | - | Título do recurso |
| `formato` | string | - | Formato (CSV, JSON, XML, etc.) |
| `tamanho` | integer | int64 | Tamanho em bytes |
| `metadataModifiedLocalDateTime` | string | date-time | Última modificação |
| `metadataModifiedDataFormatada` | string | - | Data formatada |
| `urlCheckFormatado` | string | - | URL verificada |
| `createdFormatado` | string | - | Data criação formatada |
| `sizeFormatado` | string | - | Tamanho formatado |
| `createdDataFormatada` | string | - | Data criação formatada |
| `lastModifiedFormatado` | string | - | Última modificação formatada |
| `lastModifiedSemHora` | string | date | Data sem hora |
| `descricao` | string | - | **[0, 1000] caracteres** |

### Organization (Subschema)

Campos da organização:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | string | ID da organização |
| `name` | string | Nome técnico (slug) |
| `quantidadeConjuntoDadosAbertos` | integer (int32) | Total de datasets abertos |
| `quantidadeConjuntoDadosNaoAbertos` | integer (int32) | Total de datasets não abertos |
| `indiceConjuntoDados` | array<object> | Índice de datasets |

#### IndiceConjuntoDados (dentro de organization)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `name` | string | Nome do dataset |
| `id` | string | ID do dataset |
| `title` | string | Título do dataset |
| `notes` | string | Descrição |
| `organizationId` | string | ID da organização |
| `organizationName` | string | Nome da organização |

---

## RecursoDTO (Resource)

Schema para recursos de dados (arquivos, APIs, etc.).

### Campos principais

| Campo | Tipo | Formato | Restrições |
|-------|------|---------|------------|
| `id` | string | - | ID único |
| `format` | string | - | Tipo de arquivo |
| `url` | string | - | URL de acesso |
| `name` | string | - | Nome do recurso |
| `description` | string | - | Descrição |
| `created` | string | date-time | Data de criação |
| `size` | integer | int64 | Tamanho em bytes |
| `tipo` | string | **ENUM** | Ver enum acima |
| `nomeArquivo` | string | - | Nome do arquivo |
| `quantidadeDownloads` | integer | int32 | Contador |
| `numOrdem` | integer | int32 | Ordem |

### Formatos comuns

Baseado na análise da API, formatos típicos incluem:

- `CSV` - Valores separados por vírgula
- `JSON` - JavaScript Object Notation
- `XML` - Extensible Markup Language
- `PDF` - Portable Document Format
- `XLS` / `XLSX` - Microsoft Excel
- `TXT` - Texto plano
- `ZIP` - Arquivo comprimido
- `API` - Endpoint de API REST
- `WMS` - Web Map Service
- `SHP` - Shapefile (dados geográficos)

---

## OrganizacaoCkanDTO (Organization)

Schema para organizações governamentais.

### Campos

| Campo | Tipo | Formato | Descrição |
|-------|------|---------|-----------|
| `id` | string | - | ID único da organização |
| `name` | string | - | Nome técnico (slug) |
| `quantidadeConjuntoDadosAbertos` | integer | int32 | Total de datasets abertos |
| `quantidadeConjuntoDadosNaoAbertos` | integer | int32 | Total de datasets fechados |
| `indiceConjuntoDados` | array<object> | - | Lista de datasets |

### Exemplos de organizações

Organizações típicas do governo federal brasileiro:

- `ministerio-da-saude` - Ministério da Saúde
- `ministerio-da-educacao` - Ministério da Educação
- `ministerio-da-economia` - Ministério da Economia
- `ibge` - Instituto Brasileiro de Geografia e Estatística
- `anac` - Agência Nacional de Aviação Civil
- `anvisa` - Agência Nacional de Vigilância Sanitária
- `cgu` - Controladoria-Geral da União
- `inep` - Instituto Nacional de Estudos e Pesquisas Educacionais

---

## TagDTO (Tag)

Schema para tags/palavras-chave.

### Campos

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | string | ID da tag |
| `name` | string | Nome da tag (lowercase) |
| `display_name` | string | Nome de exibição |

### Tags comuns

Tags frequentes no portal:

- `saúde`, `educação`, `economia`
- `COVID-19`, `vacinação`, `epidemiologia`
- `educação-superior`, `enem`, `censo-escolar`
- `dados-abertos`, `transparência`
- `sustentabilidade`, `meio-ambiente`

---

## TemaDTO (Theme)

Schema para temas/categorias.

### Estrutura

Temas são categorias amplas que agrupam datasets relacionados.

**Endpoint para listar**: `GET /dados/api/temas`

### Temas esperados

Baseado na estrutura de dados abertos brasileira:

- Agricultura
- Ciência e Tecnologia
- Cultura
- Economia e Finanças
- Educação
- Meio Ambiente
- Saúde
- Segurança Pública
- Transporte e Trânsito

---

## Enumerações Globais

### Status de Privacidade

| Campo | Tipo | Valores |
|-------|------|---------|
| `isPrivado` | string/boolean | `"true"`, `"false"`, `true`, `false` |
| `dadosAbertos` | boolean | `true` (dados abertos), `false` (dados restritos) |

### Ordenação (ordenacao)

Valores possíveis para ordenação de resultados:

- `metadata_modified desc` - Mais recentes primeiro
- `metadata_modified asc` - Mais antigos primeiro
- `title asc` - Alfabético A-Z
- `title desc` - Alfabético Z-A
- `relevance` - Por relevância (em buscas)

### Paginação

| Campo | Tipo | Formato | Restrições |
|-------|------|---------|------------|
| `pagina` | integer | int32 | **OBRIGATÓRIO**, >= 1 |
| `tamanhoPagina` | integer | int32 | Padrão: 10, Max: 1000 |

---

## Validações e Restrições

### Tamanho de Campos

| Campo | Min | Max | Observação |
|-------|-----|-----|------------|
| `descricao` | 0 | 1000 | Caracteres |
| `name` (dataset) | 2 | 100 | Apenas lowercase, hífens |
| `title` | 1 | 255 | Título do dataset |

### Formatos de Data

Todos os campos de data seguem ISO 8601:

```
2026-01-20T15:30:00Z
2026-01-20T12:30:00-03:00
```

**Campos com date-time**:
- `dataUltimaAtualizacaoRecurso`
- `created`
- `last_modified`
- `metadataModifiedLocalDateTime`
- `lastModifiedSemHora` (apenas date: `2026-01-20`)

### Formatos de Arquivo Válidos

Baseado nos dados da API:

```
CSV, JSON, XML, PDF, XLS, XLSX, ZIP, TXT,
SHP, KML, GeoJSON, WMS, WFS, API, HTML,
ODS, RDF, OWL, SPARQL
```

---

## Exemplos de Uso

### 1. Buscar datasets por tipo de recurso

```python
# Buscar apenas datasets com APIs
params = {
    "pagina": 1,
    "tamanhoPagina": 20,
    "dadosAbertos": True
}

# Depois filtrar resources onde tipo == "API" (enum #4)
```

### 2. Buscar por organização

```python
params = {
    "pagina": 1,
    "tamanhoPagina": 10,
    "idOrganizacao": "ministerio-da-saude",
    "ordenacao": "metadata_modified desc"
}
```

### 3. Filtrar dados abertos

```python
params = {
    "pagina": 1,
    "dadosAbertos": True,  # Apenas dados abertos
    "isPrivado": "false"   # Não incluir privados
}
```

---

## Testes Recomendados

### Teste 1: Descobrir IDs de Organizações

```bash
GET /dados/api/publico/organizacao
```

Capturar `id` e `name` de cada organização para usar em filtros.

### Teste 2: Listar Todos os Temas

```bash
GET /dados/api/temas
```

Capturar lista completa de temas disponíveis.

### Teste 3: Listar Todas as Tags

```bash
GET /dados/api/tags
```

Capturar tags populares para buscas.

### Teste 4: Buscar Dataset por Nome

```bash
GET /dados/api/publico/conjuntos-dados?nomeConjuntoDados=covid&pagina=1
```

### Teste 5: Listar Formatos Disponíveis

```bash
GET /dados/api/publico/conjuntos-dados/formatos
```

Retorna lista de todos os formatos de arquivo suportados.

---

## Notas Importantes

1. **Paginação Obrigatória**: O parâmetro `pagina` é **obrigatório** no endpoint de listagem de datasets

2. **IDs vs Names**:
   - `id`: UUID único (ex: `"abc123-def456-..."`)
   - `name`: Slug técnico (ex: `"ministerio-da-saude"`)

3. **Enumerações**: O campo `tipo` de recursos usa tanto números (`0-5`) quanto strings (`"DADOS"`, `"API"`, etc.)

4. **Filtros Múltiplos**: É possível combinar múltiplos filtros:
   ```
   ?dadosAbertos=true&idOrganizacao=ibge&ordenacao=title asc&pagina=1
   ```

5. **Campos Formatados**: Muitos schemas têm versões "formatadas" de campos de data/número para exibição

---

## Próximos Passos

1. ✅ Documentar domínios de campos descobertos
2. ⏭️ Testar cada endpoint com valores reais
3. ⏭️ Capturar respostas de exemplo
4. ⏭️ Validar enumerações com chamadas reais
5. ⏭️ Documentar códigos de erro

---

**Atualizado**: 2026-01-20
**Status**: Domínios mapeados via Swagger UI
**Limitação**: Testes práticos pendentes (API retorna HTML via HTTP direto)