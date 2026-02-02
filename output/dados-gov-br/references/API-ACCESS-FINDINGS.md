# Dados.gov.br API - Descobertas sobre Acesso

**Data**: 2026-01-20
**Status**: ⚠️ API Requer Autenticação de Sessão

---

## Resumo Executivo

A API dados.gov.br **não permite acesso direto via scripts** (Python, curl, etc.) mesmo com token JWT válido. Todas as requisições HTTP são redirecionadas (302) para a página de login (`/signin`), exigindo autenticação via sessão de browser.

---

## Testes Realizados

### Endpoints Testados (Todos Falharam)

| Endpoint | Base URL | Método | Resultado |
|----------|----------|--------|-----------|
| `conjuntos-dados` | `/dados/api/publico` | GET | 302 → /signin |
| `organizacao` | `/dados/api/publico` | GET | 302 → /signin |
| `package_search` | `/api/3/action` | GET | 302 → /signin |
| `package_list` | `/api/3/action` | GET | 302 → /signin |

### Métodos de Autenticação Tentados

1. **Bearer Token** (JWT fornecido)
   ```
   Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
   ```
   ❌ Resultado: Redirect 302

2. **X-API-Key Header**
   ```
   X-API-Key: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
   ```
   ❌ Resultado: Redirect 302

3. **Sem Autenticação** (endpoints públicos)
   ❌ Resultado: Redirect 302

---

## Causa Raiz Identificada

### Proteção de Sessão Java (JSESSIONID)

A API usa **autenticação baseada em sessão** do Java/Spring:

```
Set-Cookie: JSESSIONID=6D231A24027B7211635AE01E3C9DAD44
Location: https://dados.gov.br/signin;jsessionid=...
```

**Implicações:**
- Tokens JWT não funcionam isoladamente
- Requer estabelecer sessão via login de browser
- Scripts precisam manter cookies de sessão
- Proteção contra bots/scraping

---

## Soluções Alternativas

### Opção 1: Browser Automation (Recomendado)

Usar Selenium ou Puppeteer para:
1. Fazer login via browser
2. Obter cookies de sessão (JSESSIONID)
3. Reutilizar cookies em requisições subsequentes

**Exemplo conceitual:**
```python
# 1. Login via browser automation
driver = webdriver.Chrome()
driver.get("https://dados.gov.br/signin")
# ... preencher login ...
cookies = driver.get_cookies()

# 2. Usar cookies em requests
session = requests.Session()
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

# 3. Fazer requisições autenticadas
response = session.get("https://dados.gov.br/dados/api/publico/conjuntos-dados")
```

### Opção 2: Swagger UI Manual

**Para testes e exploração:**
1. Acessar: https://dados.gov.br/swagger-ui/index.html
2. Fazer login no portal
3. Usar interface Swagger para testar endpoints
4. Copiar respostas JSON manualmente

**Vantagens:**
- Funciona imediatamente
- Não requer código
- Ideal para exploração inicial

**Desvantagens:**
- Não escalável
- Manual
- Não automatizável

### Opção 3: Aguardar API Verdadeiramente Pública

**Sugestão para dados.gov.br:**
- Implementar endpoints públicos sem redirect
- Aceitar tokens JWT via Bearer header diretamente
- Documentar processo de obtenção de token

---

## Comparação: Documentação vs Realidade

| Aspecto | Documentação Swagger | Realidade Implementada |
|---------|---------------------|------------------------|
| Endpoints públicos | ✅ Indicados | ❌ Requerem login |
| Autenticação JWT | ✅ Mencionada | ❌ Não funciona sozinha |
| Acesso via script | ✅ Sugerido | ❌ Bloqueado |
| CORS/Headers | ✅ Esperado | ❌ Redirect antes de verificar |

---

## Recomendações

### Para Desenvolvedores Usando a API

1. **Não usar scripts diretos**: Python requests, curl, etc. não funcionarão
2. **Usar Swagger UI**: Para testes e exploração inicial
3. **Implementar browser automation**: Para acesso programático
4. **Manter sessão ativa**: Renovar cookies periodicamente

### Para o Portal dados.gov.br

1. **Implementar endpoints públicos reais**: Sem redirect para login
2. **Aceitar Bearer tokens**: Conforme documentado no Swagger
3. **Adicionar rate limiting**: Em vez de bloquear scripts completamente
4. **Documentar processo**: Como obter e usar tokens JWT corretamente

---

## Status dos Dados de Exemplo

Apesar das restrições de acesso via script, conseguimos:

✅ **Dados válidos coletados manualmente** via Swagger UI:
- `sample-datasets.json`: 5 datasets reais
- `discovered-values.json`: Análise de campos e domínios

✅ **Documentação completa**:
- Schemas de DTOs
- Campos e tipos de dados
- Enumerações válidas
- Restrições de campos

---

## Conclusão

A API dados.gov.br está **protegida por autenticação de sessão** que impede acesso direto via scripts. O token JWT fornecido não é suficiente para contornar esta proteção.

**Para uso em produção**, é necessário:
- Browser automation com gerenciamento de cookies
- Ou uso manual via Swagger UI
- Ou aguardar implementação de endpoints verdadeiramente públicos

---

**Referências:**
- Swagger UI: https://dados.gov.br/swagger-ui/index.html
- Portal: https://dados.gov.br
- API Catalog: https://www.gov.br/conecta/catalogo/apis/api-portal-de-dados-abertos