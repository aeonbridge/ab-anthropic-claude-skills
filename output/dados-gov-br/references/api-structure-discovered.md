# Dados.gov.br API - Discovered Structure

**Date**: 2026-01-20
**Discovery Method**: Swagger UI exploration at https://dados.gov.br/swagger-ui/index.html

## Important Discovery

The dados.gov.br API is **NOT** based on CKAN as initially assumed. It has a custom REST API with a different structure.

## Correct Base URL

```
https://dados.gov.br/dados/api/publico
```

## API Information

- **Title**: API REST do Portal de Dados Abertos
- **Version**: 1.0
- **OAS Version**: OAS 3.1
- **References**:
  - Diretoria de Tecnologia da Informação - DTI - Website
  - Send email to Diretoria de Tecnologia da Informação - DTI
  - Decreto nº 8.777, de 11 de maio de 2016
  - Changelog

## API Endpoint Categories

### 1. Conjuntos de dados (Datasets)

Main entity for accessing government datasets.

**Endpoints:**

- `GET /dados/api/publico/conjuntos-dados/{id}` - Get dataset details
- `PUT /dados/api/publico/conjuntos-dados/{id}` - Update dataset (Admin only)
- `DELETE /dados/api/publico/conjuntos-dados/{id}` - Delete dataset (Admin only)
- `PATCH /dados/api/publico/conjuntos-dados/{id}` - Partial update (Admin only)
- `GET /dados/api/publico/conjuntos-dados` - List datasets ✅ PUBLIC
  - Parameters:
    - `nomeConjuntoDados` (string, query): Dataset name filter
    - `dadosAbertos` (boolean, query): Filter open data
    - `isPrivado` (string, query, default: false): Filter private datasets
    - `idOrganizacao` (string, query): Organization ID filter
    - `pagina` (integer, query, **required**): Page number
    - `tamanhoPagina` (integer, query): Page size
    - `ordenacao` (string, query): Sort order
- `POST /dados/api/publico/conjuntos-dados` - Create dataset (Admin only)
- `GET /dados/api/publico/conjuntos-dados/{id}/tag` - List dataset tags
- `GET /dados/api/publico/conjuntos-dados/observancia-legal` - Legal compliance datasets
- `GET /dados/api/publico/conjuntos-dados/objetivos-desenvolvimento-sustentavel` - Sustainable development datasets
- `GET /dados/api/publico/conjuntos-dados/formatos` - List available formats

### 2. Solicitações (Requests/Applications)

Manage data requests.

**Endpoints:**

- `POST /dados/api/solicitacoes/resposta` - Respond to request (Admin only)
- `GET /dados/api/solicitacoes` - List requests

### 3. Reúsos (Reuses)

Track how datasets are being reused.

**Endpoints:**

- `POST /dados/api/reuso/salvar` - Save new reuse
- `PATCH /dados/api/reuso/atualiza/{id}` - Update reuse
- `PATCH /dados/api/publico/reusos/homologacao/pendente/{idReuso}` - Submit for approval
- `GET /dados/api/publico/reusos` - List reuses
- `GET /dados/api/publico/reuso/{id}` - Get reuse details
- `DELETE /dados/api/publico/reusos/{idReuso}` - Delete reuse

### 4. Recursos (Resources)

Manage dataset resources (files, APIs, etc.).

**Endpoints:**

- `POST /dados/api/recurso/salvar` - Save resource (Admin only)
- `DELETE /dados/api/recurso/{id}` - Delete resource (Admin only)

### 5. Temas (Themes)

Thematic categorization.

**Endpoints:**

- `GET /dados/api/temas` - List themes

### 6. Tags

Keyword tags for datasets.

**Endpoints:**

- `GET /dados/api/tags` - List tags

### 7. Organização (Organizations)

Government organizations publishing datasets.

**Endpoints:**

- `GET /dados/api/publico/organizacao` - List organizations
- `GET /dados/api/publico/organizacao/{id}` - Get organization details

## Authentication

Based on the token provided:
```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJPaEx6RktTZWNUR1c0V25KT1NLbjFuYU5NTWxTSWxEX29RUGxpZHk5NXN3OUYtT2Zadm9sZnVjX0UtdlZyTzRNT2FTcGNHUGNOMzN4VXNpNiIsImlhdCI6MTc0MjI0Njk4N30.LOboeht1ujLjjS3Qsyn3nlGXbguCN4sb2xIsIenK52s
```

This appears to be a JWT (JSON Web Token) with:
- Type: JWT
- Algorithm: HS256
- Issued at: 1742246987 (Unix timestamp)

**Header format** (to be tested):
```
Authorization: Bearer {token}
```

Or possibly:
```
X-API-Key: {token}
```

## Public vs. Protected Endpoints

- 🔓 **Public endpoints** (no lock icon in Swagger UI):
  - `GET /dados/api/publico/conjuntos-dados` - List datasets
  - `GET /dados/api/publico/organizacao` - List organizations
  - `GET /dados/api/temas` - List themes
  - `GET /dados/api/tags` - List tags
  - `GET /dados/api/publico/reusos` - List reuses

- 🔒 **Protected endpoints** (lock icon in Swagger UI):
  - All POST, PUT, PATCH, DELETE operations
  - Admin-only dataset management
  - Request responses
  - Resource management

## Data Models (Schemas)

The API defines several data transfer objects (DTOs):

1. **ErroDTO** - Error responses
2. **ArquivoCodificado** - Encoded file data
3. **AutocompleteOption** - Autocomplete suggestions
4. **AvaliacaoConjuntoDadosDTO** - Dataset evaluation
5. **AvaliacaoConjuntoDadosForm** - Dataset evaluation form
6. **ConjuntoDadosApiView** - Dataset API view model
7. **ConjuntoDadosCadastroForm** - Dataset registration form
8. **ConjuntoDadosDTO** - Dataset data transfer object
9. **ConjuntoDadosEdicaoDTO** - Dataset edit model

(More schemas visible in Swagger UI Schemas section)

## Key Differences from CKAN API

1. **URL Structure**: Custom `/dados/api/publico/` instead of `/api/3/action/`
2. **Endpoint Names**: Portuguese names (conjuntos-dados, organizacao) instead of CKAN's English (package, organization)
3. **Parameters**: Different parameter names and structure
4. **Authentication**: JWT-based instead of CKAN API keys
5. **Response Format**: Custom JSON structure (to be determined from actual calls)

## Next Steps for Testing

1. Test public endpoints without authentication:
   - `GET https://dados.gov.br/dados/api/publico/conjuntos-dados?pagina=1`
   - `GET https://dados.gov.br/dados/api/publico/organizacao`
   - `GET https://dados.gov.br/dados/api/temas`
   - `GET https://dados.gov.br/dados/api/tags`

2. Test authentication with provided JWT token:
   - Try `Authorization: Bearer {token}` header
   - Try `X-API-Key: {token}` header

3. Document actual response formats

4. Test pagination parameters

5. Document error responses

## Observations

- The API is well-structured with clear separation between public and admin endpoints
- Most data modification operations require authentication
- The API follows RESTful principles
- Swagger UI is comprehensive and well-documented
- All text is in Portuguese (pt-BR)