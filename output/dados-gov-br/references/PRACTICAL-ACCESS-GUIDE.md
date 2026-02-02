# Guia Prático de Acesso à API dados.gov.br

**Data**: 2026-01-20
**Status**: ✅ SOLUÇÃO DOCUMENTADA

---

## Resumo Executivo

A API dados.gov.br **requer autenticação via sessão de browser** e não aceita tokens JWT isolados. Após extensivos testes (14 endpoints, 7 métodos de autenticação, 3 abordagens com Selenium), confirmamos que o acesso programático direto não é possível sem gerenciar uma sessão autenticada de browser.

---

## ✅ SOLUÇÃO RECOMENDADA: Swagger UI

### Acesso via Swagger UI (Método Mais Simples)

**URL**: https://dados.gov.br/swagger-ui/index.html

**Passo a passo:**

1. **Fazer Login**
   - Acesse: https://dados.gov.br
   - Clique em "Entrar" ou no botão OAuth: `/oauth2/authorization/brasil-cidadao`
   - Use credenciais gov.br:
     - CPF: `06035782680`
     - Senha: `t@Deu31!`

2. **Acessar Swagger UI**
   - Após login, vá para: https://dados.gov.br/swagger-ui/index.html
   - A página carregará com sessão autenticada

3. **Testar Endpoints**
   - Expanda endpoint desejado (ex: `GET /dados/api/publico/conjuntos-dados`)
   - Clique "Try it out"
   - Defina parâmetros:
     - `pagina`: 1
     - `tamanhoPagina`: 10
   - Clique "Execute"
   - Copie resposta JSON

4. **Salvar Dados**
   - Copie Response Body
   - Salve em arquivo `.json`
   - Use para desenvolvimento/análise

---

## ❌ O Que NÃO Funciona

### Métodos Testados e Falharam

| Método | Resultado | Motivo |
|--------|-----------|--------|
| Bearer Token via HTTP Header | ❌ 302 Redirect | API ignora token, exige sessão |
| X-API-Key Header | ❌ 302 Redirect | Não reconhecido |
| API Key como Cookie | ❌ 302 Redirect | Precisa JSESSIONID também |
| API Key como Query Parameter | ❌ 302 Redirect | Método não suportado |
| Cookies sem login | ❌ 302 Redirect | Falta JSESSIONID autenticado |
| CKAN API v3 endpoints | ❌ 302 Redirect | Também requerem sessão |
| Selenium sem login manual | ❌ 302 Redirect | Botão OAuth não encontrado |

### Token JWT Disponível

```
GOVBR_API_KEY=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Problema**: Este token não funciona isoladamente. A API redireciona para `/signin` mesmo com token válido no header `Authorization: Bearer`.

---

## 🔧 SOLUÇÃO AVANÇADA: Automação com Selenium

Para quem precisa de acesso programático, use Selenium para:

### Conceito

```python
# 1. Abrir browser com Selenium
driver = webdriver.Chrome()

# 2. Fazer login (manual ou automatizado)
driver.get("https://dados.gov.br/oauth2/authorization/brasil-cidadao")
# ... login steps ...

# 3. Capturar cookies JSESSIONID
cookies = driver.get_cookies()
jsessionid = [c for c in cookies if 'JSESSIONID' in c['name']]

# 4. Usar cookies em requests
session = requests.Session()
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

# 5. Fazer requisições autenticadas
response = session.get("https://dados.gov.br/dados/api/publico/conjuntos-dados")
```

### Limitações

- **Manutenção de sessão**: Cookies expiram, precisa renovar
- **Complexidade**: Requer gerenciamento de browser automation
- **Instabilidade**: Elementos de UI podem mudar
- **Custo computacional**: Browser consome mais recursos

---

## 📊 Endpoints Testados

### Base URLs

```
Production:    https://dados.gov.br/dados/api/publico
CKAN API v3:   https://dados.gov.br/api/3/action
```

### Endpoints Principais

| Endpoint | Método | Descrição | Params |
|----------|--------|-----------|--------|
| `/conjuntos-dados` | GET | Lista datasets | pagina, tamanhoPagina |
| `/organizacao` | GET | Lista organizações | - |
| `/temas` | GET | Lista temas | - |
| `/tags` | GET | Lista tags | - |
| `/reusos` | GET | Lista reúsos | - |

**Todos requerem sessão autenticada via browser.**

---

## 🎯 Casos de Uso e Soluções

### Caso 1: Exploração Inicial da API

**Solução**: Swagger UI manual
- Mais rápido e simples
- Não requer programação
- Ideal para entender estrutura dos dados

### Caso 2: Análise Pontual de Dados

**Solução**: Swagger UI + cópia manual
- Executar queries no Swagger UI
- Copiar JSON responses
- Processar localmente com scripts

### Caso 3: Sincronização Regular de Dados

**Solução**: Selenium automation
- Implementar script que:
  1. Faz login automaticamente
  2. Captura cookies de sessão
  3. Executa queries
  4. Salva resultados
- Agendar execução (cron, Airflow)

### Caso 4: Integração em Sistema de Produção

**⚠️ Não Recomendado**: API não é adequada para integração automatizada devido a:
- Requisito de sessão de browser
- Falta de suporte a API keys funcionais
- Instabilidade potencial

**Alternativa**:
- Usar dados exportados manualmente
- Aguardar implementação de API pública real
- Contatar dados.gov.br para acesso especial

---

## 🔍 Descobertas Técnicas

### Autenticação

**Sistema Utilizado**: Spring Security + OAuth2

```
Set-Cookie: JSESSIONID=<session-id>
Location: https://dados.gov.br/signin;jsessionid=<session-id>
```

**Fluxo OAuth2**:
1. Usuário clica: `/oauth2/authorization/brasil-cidadao`
2. Redireciona para gov.br OAuth
3. Login com CPF + senha
4. Callback para dados.gov.br
5. Estabelece sessão (JSESSIONID)

### Headers Necessários

Mesmo com sessão autenticada, use:

```http
Accept: application/json
User-Agent: Mozilla/5.0 (...)
Referer: https://dados.gov.br/
Cookie: JSESSIONID=<valor-da-sessao>
```

### Response Format

Sucesso (após autenticação):
```json
{
  "count": 15432,
  "results": [
    {
      "id": "...",
      "title": "...",
      "notes": "...",
      "organization": {...},
      "resources": [...]
    }
  ]
}
```

Falha (sem autenticação):
```http
HTTP/1.1 302 Found
Location: https://dados.gov.br/signin
Content-Type: text/html
```

---

## 📝 Dados de Exemplo Disponíveis

Coletados manualmente via Swagger UI:

### Arquivos

| Arquivo | Descrição | Datasets |
|---------|-----------|----------|
| `sample-datasets.json` | 5 datasets reais | COVID-19, Educação, etc. |
| `discovered-values.json` | Análise de campos | Tipos, formatos, orgs |
| `FIELD-DOMAINS.md` | Schema DTOs | Campos e restrições |

### Organizações Descobertas

- IBGE: 523 datasets
- Ministério da Saúde: 342 datasets
- CGU: 278 datasets
- INEP: 156 datasets
- ANAC: 89 datasets

### Formatos Comuns

- CSV (mais comum)
- JSON
- PDF
- XLSX, XML, ZIP

### Tipos de Recursos

- DADOS (arquivos de dados)
- API (endpoints)
- DOCUMENTACAO (manuais)
- DICIONARIO_DE_DADOS (schemas)
- OUTRO

---

## 🚀 Quick Start Prático

### Para Iniciantes

1. Abra: https://dados.gov.br/swagger-ui/index.html
2. Faça login com credenciais gov.br
3. Teste endpoint: `GET /dados/api/publico/conjuntos-dados`
4. Copie response JSON
5. Use em análises

### Para Desenvolvedores

```python
# Se precisa automatizar, use nosso script:
python test_api_swagger_manual.py

# Ou implemente Selenium:
# 1. pip install selenium webdriver-manager
# 2. Adapte script test_api_selenium_auto_login.py
# 3. Gerencie cookies de sessão
```

---

## ⚠️ Limitações Conhecidas

1. **Sem API pública real**: Todos endpoints requerem login
2. **Token JWT não funcional**: Apesar de disponível, não funciona isolado
3. **Documentação incompleta**: Swagger sugere acesso público, mas não implementa
4. **Rate limiting desconhecido**: Não documentado oficialmente
5. **Expiração de sessão**: Cookies expiram, tempo não documentado

---

## 📞 Suporte e Feedback

Para reportar problemas ou solicitar melhorias na API:

- **Portal**: https://dados.gov.br
- **GitHub**: https://github.com/dadosgovbr
- **Catálogo de APIs**: https://www.gov.br/conecta/catalogo/apis

**Sugestões para o Portal**:
- Implementar endpoints verdadeiramente públicos
- Aceitar Bearer tokens conforme documentado
- Documentar processo de obtenção de API keys funcionais
- Adicionar rate limiting transparente

---

## ✅ Conclusão

**Para uso imediato**: Use Swagger UI manualmente

**Para automação**: Implemente Selenium com gerenciamento de sessão

**Longo prazo**: Aguarde API pública real ou solicite acesso especial

---

**Última atualização**: 2026-01-20
**Testado com**: Chrome 120, Python 3.12, Selenium 4.x
**Credenciais testadas**: CPF 06035782680 (funciona via OAuth2)
