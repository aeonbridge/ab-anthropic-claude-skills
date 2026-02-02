# Scripts de Teste - API dados.gov.br

**Diretório**: `output/dados-gov-br/scripts/`
**Criado**: 2026-01-20
**Status**: ✅ Investigação completa

---

## 📁 Inventário de Scripts

### Scripts de Teste HTTP

| Script | LOC | Propósito | Resultado |
|--------|-----|-----------|-----------|
| `test_api.py` | 180 | Teste básico inicial | ❌ 302 redirect |
| `test_api_correct.py` | 260 | Estrutura correta da API | ❌ 302 redirect |
| `test_api_simple.py` | 85 | Teste mínimo com token | ❌ 302 redirect |
| `test_api_advanced.py` | 220 | 7 métodos de autenticação | ❌ Todos falharam |
| `test_public_endpoints.py` | 110 | Teste de 14 endpoints | ❌ Todos protegidos |
| `debug_api.py` | 95 | Debug de headers e responses | ❌ HTML retornado |

**Conclusão**: Nenhum método HTTP direto funciona. API exige sessão de browser.

### Scripts Selenium (Browser Automation)

| Script | LOC | Estratégia | Resultado |
|--------|-----|------------|-----------|
| `test_api_selenium.py` | 180 | Automação básica + captura | ⚠️ Precisa login manual |
| `test_api_manual_assisted.py` | 160 | Aguarda login manual | ⚠️ Timeout, não logou |
| `test_api_selenium_auto_login.py` | 245 | Auto-login com credenciais | ❌ Botão não encontrado |
| `test_api_oauth_login.py` | 290 | OAuth2 brasil-cidadao | ❌ Elemento não localizado |

**Conclusão**: Selenium abre browser, mas login automático falha. Precisa intervenção manual.

### Scripts de Análise

| Script | LOC | Propósito | Resultado |
|--------|-----|-----------|-----------|
| `discover_field_values.py` | 295 | Análise de campos da API | ✅ Funcionou com samples |

**Conclusão**: Análise de dados de exemplo funcionou perfeitamente.

---

## 🚀 Como Usar Cada Script

### 1. test_api_correct.py

**Propósito**: Testa a estrutura correta da API dados.gov.br

**Uso**:
```bash
python test_api_correct.py
```

**O que faz**:
- Testa 8 endpoints diferentes
- Usa token JWT do `.env`
- Tenta Bearer token e X-API-Key
- Salva respostas em `references/api-responses/`

**Resultado esperado**: Todos retornam 302 redirect

---

### 2. test_api_advanced.py

**Propósito**: Testa 7 métodos diferentes de autenticação

**Uso**:
```bash
python test_api_advanced.py
```

**Métodos testados**:
1. Bearer Token (Authorization header)
2. API Key como Cookie
3. API Key como Query Parameter
4. X-API-Key header
5. X-Auth-Token header
6. access_token query parameter
7. CKAN API v3

**Resultado esperado**: Nenhum funciona (0/7 sucesso)

---

### 3. test_public_endpoints.py

**Propósito**: Testa todos os endpoints conhecidos em 3 base URLs

**Uso**:
```bash
python test_public_endpoints.py
```

**Endpoints testados**: 14 combinações
**Base URLs**:
- `/api/3/action` (CKAN)
- `/dados/api`
- `/dados/api/publico`

**Resultado esperado**: Todos retornam 302 para `/signin`

---

### 4. test_api_selenium.py

**Propósito**: Automação browser básica com captura de cookies

**Uso**:
```bash
python test_api_selenium.py
```

**Requisitos**:
```bash
pip install selenium webdriver-manager
```

**O que faz**:
1. Abre Chrome
2. Navega para Swagger UI
3. Verifica autenticação
4. Captura cookies
5. Testa API com cookies

**Nota**: Requer ChromeDriver (instalado automaticamente)

---

### 5. test_api_oauth_login.py

**Propósito**: Tenta login automático via OAuth2

**Uso**:
```bash
python test_api_oauth_login.py
```

**Credenciais** (hardcoded no script):
- CPF: 06035782680
- Senha: t@Deu31!

**Fluxo tentado**:
1. Abre dados.gov.br
2. Busca botão OAuth `/oauth2/authorization/brasil-cidadao`
3. Tenta preencher CPF e senha
4. Captura cookies
5. Testa API

**Limitação**: Botão OAuth não encontrado automaticamente

---

### 6. discover_field_values.py

**Propósito**: Analisa estrutura de dados da API

**Uso**:
```bash
python discover_field_values.py
```

**Requisito**: Arquivo `references/sample-datasets.json` deve existir

**Saída**:
- Tipos de recursos (DADOS, API, DOCUMENTACAO, etc.)
- Formatos de arquivo (CSV, JSON, PDF, etc.)
- Organizações principais
- Tags populares
- Restrições de campos (tamanhos, etc.)

**Resultado salvo em**: `references/discovered-values.json`

---

## 📊 Sumário dos Resultados

```
Total de scripts:          11
Scripts HTTP:              6  → 0% sucesso
Scripts Selenium:          4  → 0% auto-login
Scripts de análise:        1  → 100% sucesso

Endpoints testados:        14 → Todos protegidos
Métodos de auth:           7  → Nenhum funciona
Tempo total de execução:   ~30min
```

---

## 💡 Descobertas Principais

### 1. API Requer Sessão de Browser

**Evidência**:
```
HTTP/1.1 302 Found
Location: https://dados.gov.br/signin;jsessionid=...
```

**Todos** os endpoints redirecionam para login, incluindo:
- Endpoints "públicos" (`/dados/api/publico/*`)
- CKAN API v3 (`/api/3/action/*`)
- Com ou sem token JWT

### 2. Token JWT Não Funciona

Token disponível em `.env`:
```
GOVBR_API_KEY=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Testado em**:
- Authorization: Bearer
- X-API-Key
- X-Auth-Token
- Cookie
- Query parameter

**Resultado**: API ignora completamente o token

### 3. Login Requer OAuth2 Interactive

**Fluxo necessário**:
```
1. Click: /oauth2/authorization/brasil-cidadao
2. Redirect: sso.acesso.gov.br
3. Login: CPF + senha
4. Callback: dados.gov.br
5. Cookie: JSESSIONID=<session>
```

**Não pode ser automatizado facilmente** (elementos de UI não encontrados)

---

## ✅ Solução Recomendada

### Use Swagger UI Manualmente

1. **Login**:
   - Acesse: https://dados.gov.br
   - Clique "Entrar" ou OAuth button
   - Use: CPF `06035782680` | Senha `t@Deu31!`

2. **Swagger UI**:
   - Navegue: https://dados.gov.br/swagger-ui/index.html
   - Teste endpoints diretamente
   - Copie respostas JSON

3. **Análise**:
   - Salve responses em `sample-datasets.json`
   - Execute: `python discover_field_values.py`
   - Use dados localmente

---

## 📚 Documentação Relacionada

| Documento | Descrição |
|-----------|-----------|
| `../references/PRACTICAL-ACCESS-GUIDE.md` | Guia completo de uso |
| `../references/API-ACCESS-FINDINGS.md` | Descobertas técnicas |
| `../references/INVESTIGATION-SUMMARY.md` | Sumário da investigação |
| `../references/FIELD-DOMAINS.md` | Schemas da API |

---

## 🔧 Dependências

### Python Packages

```bash
# Básicas
pip install requests python-dotenv

# Selenium (opcional)
pip install selenium webdriver-manager

# Análise
pip install json  # built-in
```

### Arquivos Necessários

```
.env                          # Contém GOVBR_API_KEY
references/sample-datasets.json  # Para discover_field_values.py
```

---

## ⚠️ Limitações Conhecidas

1. **Nenhum script acessa API diretamente**: Todos requerem login manual
2. **Token JWT inútil**: Não funciona isoladamente
3. **Selenium não automatiza login**: Elementos de UI não localizados
4. **Cookies expiram**: Sessões precisam ser renovadas
5. **Rate limiting desconhecido**: Não documentado

---

## 🎯 Próximos Passos

### Para Desenvolvedores

1. Use Swagger UI manualmente
2. Colete dados de exemplo
3. Processe localmente com scripts de análise
4. Aguarde API pública real

### Para Automação (Se Necessário)

1. Implemente Selenium com pausa para login manual
2. Capture cookies JSESSIONID
3. Renove sessões periodicamente
4. Implemente fallback para coleta manual

---

## 📞 Suporte

**Problemas com scripts**: Verifique:
- Python 3.12+ instalado
- Dependências instaladas (`pip install -r requirements.txt`)
- ChromeDriver atualizado (auto-instalado pelo webdriver-manager)
- Arquivo `.env` configurado

**Dúvidas sobre API**: Consulte:
- Swagger UI: https://dados.gov.br/swagger-ui/index.html
- GitHub: https://github.com/dadosgovbr

---

**Última atualização**: 2026-01-20
**Scripts testados com**: Python 3.12.9, Chrome 120
**Status**: ✅ Completo e documentado
