---
name: owasp-security
description: Referência OWASP Top 10 para o executor-seguranca — mapeamento de verificação para categoria, severity, critério de bloqueio e recomendação de remediação.
---

## OWASP Top 10 — Mapeamento para o Squad QA

Usado pelo `executor-seguranca` para classificar achados e pelo `reporter-qa` para renderizar a seção de segurança com contexto OWASP.

| # | Categoria OWASP | Verificações cobertas pelo executor | Severity padrão | Bloqueia deploy |
|---|---|---|---|---|
| A01 | Broken Access Control | Acesso a endpoints sem token; acesso com token de outro usuário; `403` ausente em rota protegida | Alta | Sim |
| A02 | Cryptographic Failures | HTTPS obrigatório (redirect HTTP→HTTPS); HSTS header presente; sem conteúdo sensível em GET params | Alta | Sim |
| A03 | Injection | Inputs com `'`, `"`, `<script>`, `; DROP TABLE` não causam erro 500; resposta não reflete payload bruto | Alta | Sim |
| A04 | Insecure Design | Endpoints de admin acessíveis sem auth; funcionalidades ocultas expostas via URL conhecida | Alta | Sim |
| A05 | Security Misconfiguration | Headers de segurança obrigatórios presentes; CORS não permite `*` em rotas autenticadas; debug mode desabilitado | Média | Sim |
| A06 | Vulnerable Components | (fora do escopo do executor passivo — requer DAST/SCA) | — | Não |
| A07 | Authentication Failures | `401` retornado sem token; `401` retornado com token inválido/expirado; rate limiting em `/login` | Alta | Sim |
| A08 | Software Integrity Failures | (fora do escopo do executor passivo) | — | Não |
| A09 | Logging Failures | Endpoint de logs/trace não exposto publicamente; sem stack trace em respostas de erro 5xx | Baixa | Não |
| A10 | SSRF | Parâmetros de URL não redirecionam para hosts internos (ex: `169.254.x.x`, `localhost`, `10.x.x.x`) | Alta | Sim |

## Headers de segurança obrigatórios

| Header | Valor esperado | OWASP | Severity se ausente |
|---|---|---|---|
| `Strict-Transport-Security` | `max-age≥31536000` | A02 | Alta |
| `X-Content-Type-Options` | `nosniff` | A05 | Média |
| `X-Frame-Options` | `DENY` ou `SAMEORIGIN` | A05 | Média |
| `Content-Security-Policy` | presente (qualquer valor) | A05 | Média |
| `Referrer-Policy` | presente | A05 | Baixa |
| `Permissions-Policy` | presente | A05 | Baixa |

## Critérios de bloqueio de deploy

```
deploy_blocked = True  se qualquer achado com severity == "Alta" E owasp_blocks == True
deploy_blocked = False se todos os achados forem severity == "Média" ou "Baixa"
```

## Output esperado por achado

```json
{
  "check": "CORS permite origem wildcard em rota autenticada",
  "owasp_category": "A05 — Security Misconfiguration",
  "severity": "Alta",
  "deploy_blocked": true,
  "endpoint": "GET /api/user/profile",
  "evidence": "Access-Control-Allow-Origin: *",
  "recommendation": "Restringir CORS a origens explícitas; nunca usar '*' em endpoints que retornam dados de usuário autenticado."
}
```
