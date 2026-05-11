# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: src\api\specs\swapi.spec.ts >> SWAPI Integration Tests @api >> TC-API-001 — Gerar API client para a SWAPI: GET /people/1/ retorna 200
- Location: src\api\specs\swapi.spec.ts:7:7

# Error details

```
Error: expect(received).toBe(expected) // Object.is equality

Expected: 200
Received: 404
```

# Test source

```ts
  1  | import { test, expect } from '../../support/fixtures';
  2  | import { peopleSchema } from '../schemas/people.schema';
  3  | import { starshipSchema } from '../schemas/starship.schema';
  4  | 
  5  | test.describe('SWAPI Integration Tests @api', () => {
  6  | 
  7  |   test('TC-API-001 — Gerar API client para a SWAPI: GET /people/1/ retorna 200', async ({ apiClient }) => {
  8  |     let response: Awaited<ReturnType<typeof apiClient.getById>>;
  9  | 
  10 |     await test.step('Requisitar Luke Skywalker', async () => {
  11 |       response = await apiClient.getById('/people', '1');
  12 |     });
  13 | 
  14 |     await test.step('Validar status e contrato', async () => {
> 15 |       expect(response.status()).toBe(200);
     |                                 ^ Error: expect(received).toBe(expected) // Object.is equality
  16 |       expect(response.ok()).toBeTruthy();
  17 |       const data = await response.json();
  18 |       const validation = peopleSchema.safeParse(data);
  19 |       if (!validation.success) console.error('Contrato inválido:', JSON.stringify(validation.error.format()));
  20 |       expect(validation.success, 'Contrato People deve ser válido').toBeTruthy();
  21 |     });
  22 |   });
  23 | 
  24 |   test('TC-API-002 — Validar contrato Zod do endpoint People /people/1/', async ({ apiClient }) => {
  25 |     let response: Awaited<ReturnType<typeof apiClient.getById>>;
  26 | 
  27 |     await test.step('Requisitar People/1', async () => {
  28 |       response = await apiClient.getById('/people', '1');
  29 |     });
  30 | 
  31 |     await test.step('Validar campos obrigatórios do schema Zod', async () => {
  32 |       expect(response.status()).toBe(200);
  33 |       const data = await response.json();
  34 |       const validation = peopleSchema.safeParse(data);
  35 |       expect(validation.success, 'Schema Zod People deve ser válido').toBeTruthy();
  36 |       if (validation.success) {
  37 |         expect(typeof validation.data.name).toBe('string');
  38 |         expect(typeof validation.data.height).toBe('string');
  39 |         expect(typeof validation.data.mass).toBe('string');
  40 |         expect(typeof validation.data.birth_year).toBe('string');
  41 |         expect(typeof validation.data.gender).toBe('string');
  42 |         expect(Array.isArray(validation.data.films)).toBeTruthy();
  43 |         expect(typeof validation.data.url).toBe('string');
  44 |       }
  45 |     });
  46 |   });
  47 | 
  48 |   test('TC-API-003 — Buscar Millennium Falcon: GET /starships/10/ status 200 e name correto', async ({ apiClient }) => {
  49 |     let response: Awaited<ReturnType<typeof apiClient.getById>>;
  50 | 
  51 |     await test.step('Requisitar Starships/10', async () => {
  52 |       response = await apiClient.getById('/starships', '10');
  53 |     });
  54 | 
  55 |     await test.step('Validar status, contrato e name', async () => {
  56 |       expect(response.status()).toBe(200);
  57 |       expect(response.ok()).toBeTruthy();
  58 |       const data = await response.json();
  59 |       const validation = starshipSchema.safeParse(data);
  60 |       if (!validation.success) console.error('Contrato inválido:', JSON.stringify(validation.error.format()));
  61 |       expect(validation.success, 'Contrato Starship deve ser válido').toBeTruthy();
  62 |       expect(data.name).toBe('Millennium Falcon');
  63 |     });
  64 |   });
  65 | 
  66 |   test('TC-API-004 — API client: GET /people/ retorna lista paginada', async ({ apiClient }) => {
  67 |     let response: Awaited<ReturnType<typeof apiClient.getAll>>;
  68 | 
  69 |     await test.step('Requisitar listagem de People', async () => {
  70 |       response = await apiClient.getAll('/people');
  71 |     });
  72 | 
  73 |     await test.step('Validar resposta paginada', async () => {
  74 |       expect(response.status()).toBe(200);
  75 |       const data = await response.json();
  76 |       expect(data).toHaveProperty('count');
  77 |       expect(data).toHaveProperty('results');
  78 |       expect(Array.isArray(data.results)).toBeTruthy();
  79 |     });
  80 |   });
  81 | });
  82 | 
```