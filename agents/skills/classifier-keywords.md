---
name: classifier-keywords
description: Tabela canônica de tipos de teste, palavras-chave semânticas e executor mapeado. Fonte de verdade para o classifier-testes na etapa de classificação por tipo.
---

## Tipos de teste e palavras-chave

Use esta tabela como base de classificação. As palavras-chave são indicadores — não é exigido que apareçam literalmente, mas o conteúdo semântico do teste deve convergir para o tipo.

| Tipo | Palavras-chave e indicadores semânticos | Executor (resolvido via config) |
|---|---|---|
| `smoke` | "smoke", "saúde", "health", "health check", "básico funciona", "sistema sobe", "validação mínima", "crítico", "principal funcionalidade", "disponível", "funcionando" | `executor-browser` ou `executor-api` |
| `sanity` | "sanity", "cordura", "após o fix", "após deploy", "após a correção", "área afetada", "verificação pontual", "rápida validação" | `executor-browser` ou `executor-api` |
| `regressão` | "regressão", "regression", "não quebrou", "continua funcionando", "comportamento anterior", "suite de regressão", "antes e depois", "nada foi quebrado" | `executor-browser` ou `executor-api` |
| `e2e` | "end to end", "e2e", "ponta a ponta", "fluxo completo", "jornada do usuário", "do início ao fim", "fluxo de negócio", "múltiplos sistemas" | `executor-browser` |
| `integração` | "integração", "integration", "entre serviços", "comunicação entre componentes", "serviço A chama B", "API externa", "endpoint REST", "requisição HTTP" | `executor-api` |
| `contrato` | "contrato", "contract", "schema", "pact", "breaking change", "versionamento de API", "estrutura da resposta", "campos obrigatórios", "produtor e consumidor", "consumer-driven", "provider state" | `executor-contrato` |
| `visual` | "visual", "screenshot", "aparência", "layout", "cor", "fonte", "design", "UI", "interface", "pixel", "regressão visual", "não mudou visualmente", "diferença visual" | `executor-visual` |
| `acessibilidade` | "acessibilidade", "accessibility", "WCAG", "aria", "leitor de tela", "screen reader", "contraste", "a11y", "deficiência", "acessível" | `executor-acessibilidade` |
| `performance` | "performance", "desempenho", "tempo de resposta", "latência", "ms", "milissegundos", "SLA", "p95", "p99", "rápido", "lento", "velocidade de resposta" | `executor-performance` |
| `carga` | "carga", "load", "usuários simultâneos", "concorrência", "requisições por segundo", "rps", "pico de acesso", "throughput", "volume de acessos" | `executor-performance` |
| `stress` | "stress", "estresse", "além do limite", "ponto de ruptura", "degradação", "sobrecarga", "colapso", "capacidade máxima", "limite do sistema" | `executor-performance` |
| `soak` | "soak", "longo prazo", "execução prolongada", "24h", "horas", "memory leak", "vazamento de memória", "estabilidade ao longo do tempo" | `executor-performance` |
| `segurança` | "segurança", "security", "autenticação", "autorização", "401", "403", "permissão negada", "acesso negado", "CORS", "headers de segurança", "token inválido", "endpoint exposto", "vulnerabilidade" | `executor-seguranca` |
| `banco` | "banco de dados", "banco", "database", "db", "tabela", "registro", "query", "SQL", "dados persistidos", "migração", "schema do banco", "integridade dos dados" | `executor-banco` |
| `cross-browser` | "cross-browser", "Chrome", "Firefox", "Safari", "Edge", "WebKit", "múltiplos navegadores", "compatibilidade entre navegadores" | `executor-browser` |
| `mobile` (web) | "responsivo", "mobile web", "PWA", "viewport mobile", "tela pequena", "adaptativo", "layout mobile", "celular", "smartphone" — **sem** menção a app nativo, APK, IPA ou Appium | `executor-browser` |
| `mobile` (nativo) | "app nativo", "app móvel", "APK", "IPA", "Appium", "emulador", "device", "gestos nativos", "push notification", "notificação", "instalado no dispositivo", "Android", "iOS" — com ação que só faz sentido em app instalado | `executor-mobile` |
| `data-driven` | "Scenario Outline", "Examples:", "parametrizado", "dataset", "múltiplas linhas", "múltiplos datasets", "data driven", "iteração sobre dados", "CSV de casos", "para cada linha", "tabela de inputs", "múltiplos conjuntos de dados", "para cada", "combinações de dados", "iteração com dados" | `executor-datadrive` |
| `websocket` | "WebSocket", "ws://", "wss://", "socket", "conexão persistente", "mensagem em tempo real", "evento push", "handshake", "frame", "chat em tempo real" | `executor-websocket` |
| `grpc` | "gRPC", "protobuf", "proto", "RPC", "server streaming", "client streaming", "bidirectional stream", "unary call", "grpcurl", "serviço gRPC", "método RPC" | `executor-grpc` |
| `graphql` | "GraphQL", "query", "mutation", "subscription", "resolver", "schema GraphQL", "introspection", "fragments", "GQL", "__schema", "variáveis GraphQL" | `executor-graphql` |
| `email` | "email enviado", "verificar email", "email de boas-vindas", "email de confirmação", "email chegou", "caixa de entrada", "assunto do email", "corpo do email", "link de reset", "Mailhog", "Mailtrap", "IMAP", "email transacional" | `executor-email` |
| `webhook` | "webhook entregue", "webhook chegou", "callback HTTP", "evento enviado para URL", "payload do webhook", "assinatura HMAC", "X-Hub-Signature", "webhook de pagamento", "notificação webhook", "delivery do webhook" | `executor-webhook` |
| `queue` | "fila de mensagens", "Kafka", "RabbitMQ", "SQS", "Service Bus", "evento publicado", "mensagem na fila", "consumer", "producer", "tópico", "publish", "consume", "event-driven", "mensagem assíncrona", "broker de mensagens" | `executor-queue` |
| `i18n` | "tradução", "idioma", "locale", "internacionalização", "i18n", "l10n", "localização", "strings traduzidas", "texto em português", "formato de data por locale", "moeda local", "hardcoded strings", "pt-BR", "en-US", "de-DE", "multilíngue" | `executor-i18n` |
| `chaos` | "resiliência", "degradação graciosa", "serviço fora do ar", "injeção de falha", "chaos", "Toxiproxy", "timeout do serviço", "circuit breaker", "fallback", "comportamento com dependência indisponível", "latência injetada", "falha de rede simulada", "recuperação após falha" | `executor-chaos` |

## Excluídos da classificação

Não inclua na saída os seguintes tipos — eles não são testes de ambiente:

- **Unitário:** testa lógica isolada, usa mocks/stubs, não depende de ambiente externo. Sinais: "mock", "stub", "função retorna", "método X", "unitário", "isolado".
- **Manual/exploratório:** verificação subjetiva, investigação livre, sem passos determinísticos. Sinais: "explorar", "verificar se parece correto", "análise heurística", "teste exploratório".
