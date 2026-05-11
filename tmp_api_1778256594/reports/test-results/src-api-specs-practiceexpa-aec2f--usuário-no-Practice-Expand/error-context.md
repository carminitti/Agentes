# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: src\api\specs\practiceexpand.spec.ts >> Practice Expand API @api >> TC-API-012 — Registrar usuário no Practice Expand
- Location: src\api\specs\practiceexpand.spec.ts:21:7

# Error details

```
Error: expect(received).toContain(expected) // indexOf

Expected value: 404
Received array: [200, 201, 409]
```

# Test source

```ts
  1   | import { test, expect } from '../../support/fixtures';
  2   | 
  3   | let authToken: string = '';
  4   | 
  5   | test.describe('Practice Expand API @api', () => {
  6   | 
  7   |   test('TC-API-011 — Health check da API de notas', async ({ expandApi }) => {
  8   |     let response: Awaited<ReturnType<typeof expandApi.get>>;
  9   | 
  10  |     await test.step('GET /health-check', async () => {
  11  |       response = await expandApi.get('/health-check');
  12  |     });
  13  | 
  14  |     await test.step('Validar health check', async () => {
  15  |       expect(response!.status()).toBe(200);
  16  |       const data = await response!.json();
  17  |       expect(data.message).toBe('Notes API is Running');
  18  |     });
  19  |   });
  20  | 
  21  |   test('TC-API-012 — Registrar usuário no Practice Expand', async ({ expandApi }) => {
  22  |     let response: Awaited<ReturnType<typeof expandApi.post>>;
  23  | 
  24  |     await test.step('POST /users/register', async () => {
  25  |       response = await expandApi.post('/users/register', {
  26  |         data: {
  27  |           name: 'QA Agente',
  28  |           email: 'qa_agente_v3@test.com',
  29  |           password: 'Test@1234',
  30  |         },
  31  |       });
  32  |     });
  33  | 
  34  |     await test.step('Validar registro ou usuário já existente', async () => {
  35  |       // 201 = criado com sucesso; 409 = usuário já existe (aceitável em re-execução)
> 36  |       expect([200, 201, 409]).toContain(response!.status());
      |                               ^ Error: expect(received).toContain(expected) // indexOf
  37  |       if (response!.status() === 201) {
  38  |         const data = await response!.json();
  39  |         expect(data.data.name).toBe('QA Agente');
  40  |         expect(data.data.email).toBe('qa_agente_v3@test.com');
  41  |       }
  42  |     });
  43  |   });
  44  | 
  45  |   test('TC-API-013 — Login e obter token no Practice Expand', async ({ expandApi }) => {
  46  |     let response: Awaited<ReturnType<typeof expandApi.post>>;
  47  | 
  48  |     await test.step('POST /users/login', async () => {
  49  |       response = await expandApi.post('/users/login', {
  50  |         data: {
  51  |           email: 'qa_agente_v3@test.com',
  52  |           password: 'Test@1234',
  53  |         },
  54  |       });
  55  |     });
  56  | 
  57  |     await test.step('Validar token obtido', async () => {
  58  |       expect(response!.status()).toBe(200);
  59  |       const data = await response!.json();
  60  |       expect(data.data.token).toBeTruthy();
  61  |       expect(data.data.token.length).toBeGreaterThan(0);
  62  |       authToken = data.data.token;
  63  |       process.env['EXPAND_AUTH_TOKEN'] = authToken;
  64  |     });
  65  |   });
  66  | 
  67  |   test('TC-API-014 — Criar nota autenticada no Practice Expand', async ({ expandApi }) => {
  68  |     let loginResp: Awaited<ReturnType<typeof expandApi.post>>;
  69  |     let noteResp: Awaited<ReturnType<typeof expandApi.post>>;
  70  |     let token: string;
  71  | 
  72  |     await test.step('Obter token via login', async () => {
  73  |       loginResp = await expandApi.post('/users/login', {
  74  |         data: { email: 'qa_agente_v3@test.com', password: 'Test@1234' },
  75  |       });
  76  |       expect(loginResp.status()).toBe(200);
  77  |       const loginData = await loginResp.json();
  78  |       token = loginData.data.token;
  79  |     });
  80  | 
  81  |     await test.step('POST /notes com token', async () => {
  82  |       noteResp = await expandApi.post('/notes', {
  83  |         headers: { 'x-auth-token': token },
  84  |         data: {
  85  |           title: 'Nota do QA Agente',
  86  |           description: 'Criada pelo executor-api v3',
  87  |           category: 'Work',
  88  |         },
  89  |       });
  90  |     });
  91  | 
  92  |     await test.step('Validar nota criada', async () => {
  93  |       expect(noteResp!.status()).toBe(200);
  94  |       const data = await noteResp!.json();
  95  |       expect(data.data.title).toBe('Nota do QA Agente');
  96  |       expect(data.data.category).toBe('Work');
  97  |     });
  98  |   });
  99  | 
  100 |   test('TC-API-015 — Listar notas autenticado no Practice Expand', async ({ expandApi }) => {
  101 |     let loginResp: Awaited<ReturnType<typeof expandApi.post>>;
  102 |     let notesResp: Awaited<ReturnType<typeof expandApi.get>>;
  103 |     let token: string;
  104 | 
  105 |     await test.step('Obter token via login', async () => {
  106 |       loginResp = await expandApi.post('/users/login', {
  107 |         data: { email: 'qa_agente_v3@test.com', password: 'Test@1234' },
  108 |       });
  109 |       expect(loginResp.status()).toBe(200);
  110 |       const loginData = await loginResp.json();
  111 |       token = loginData.data.token;
  112 |     });
  113 | 
  114 |     await test.step('GET /notes com token', async () => {
  115 |       notesResp = await expandApi.get('/notes', {
  116 |         headers: { 'x-auth-token': token },
  117 |       });
  118 |     });
  119 | 
  120 |     await test.step('Validar lista de notas', async () => {
  121 |       expect(notesResp!.status()).toBe(200);
  122 |       const data = await notesResp!.json();
  123 |       expect(Array.isArray(data.data)).toBeTruthy();
  124 |       if (data.data.length > 0) {
  125 |         const note = data.data[0];
  126 |         expect(typeof note.id).toBe('string');
  127 |         expect(typeof note.title).toBe('string');
  128 |         expect(typeof note.description).toBe('string');
  129 |         expect(typeof note.category).toBe('string');
  130 |       }
  131 |     });
  132 |   });
  133 | 
  134 |   test('TC-API-016 — Tentar criar nota sem autenticação retorna 401', async ({ expandApi }) => {
  135 |     let response: Awaited<ReturnType<typeof expandApi.post>>;
  136 | 
```