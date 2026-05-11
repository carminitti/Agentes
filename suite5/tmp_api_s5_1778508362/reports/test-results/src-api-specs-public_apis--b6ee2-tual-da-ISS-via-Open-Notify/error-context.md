# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: src\api\specs\public_apis.spec.ts >> Public APIs Suite5 @api >> TC-API-S5-002 — Consultar posição atual da ISS via Open Notify
- Location: src\api\specs\public_apis.spec.ts:37:7

# Error details

```
Error: expect(received).toBeLessThan(expected)

Expected: < 4000
Received:   7862
```

# Test source

```ts
  1  | import { test, expect } from '../../support/fixtures';
  2  | import { countrySchema } from '../schemas/country.schema';
  3  | import { issSchema } from '../schemas/iss.schema';
  4  | 
  5  | test.describe('Public APIs Suite5 @api', () => {
  6  | 
  7  |   test('TC-API-S5-001 — Consultar dados do Brasil na Countries REST API', async ({ apiClient }) => {
  8  |     let response: Awaited<ReturnType<typeof apiClient.get>>;
  9  |     let duration_ms: number;
  10 | 
  11 |     await test.step('Enviar GET /name/brazil', async () => {
  12 |       const start = Date.now();
  13 |       response = await apiClient.get('https://restcountries.com/v3.1/name/brazil');
  14 |       duration_ms = Date.now() - start;
  15 |     });
  16 | 
  17 |     await test.step('Validar resposta', async () => {
  18 |       expect(response.status()).toBe(200);
  19 |       expect(response.ok()).toBeTruthy();
  20 |       expect(duration_ms).toBeLessThan(4000);
  21 | 
  22 |       const data = await response.json();
  23 |       expect(Array.isArray(data)).toBeTruthy();
  24 |       expect(data.length).toBeGreaterThanOrEqual(1);
  25 | 
  26 |       const country = data[0];
  27 |       const validation = countrySchema.safeParse(country);
  28 |       if (!validation.success) console.error('Contrato inválido:', validation.error.format());
  29 |       expect(validation.success, 'Contrato Zod válido').toBeTruthy();
  30 | 
  31 |       expect(country.name.common).toBe('Brazil');
  32 |       expect(country.population).toBeGreaterThan(0);
  33 |       expect(country.currencies).toHaveProperty('BRL');
  34 |     });
  35 |   });
  36 | 
  37 |   test('TC-API-S5-002 — Consultar posição atual da ISS via Open Notify', async ({ apiClient }) => {
  38 |     let response: Awaited<ReturnType<typeof apiClient.get>>;
  39 |     let duration_ms: number;
  40 | 
  41 |     await test.step('Enviar GET /iss-now.json', async () => {
  42 |       const start = Date.now();
  43 |       response = await apiClient.get('http://api.open-notify.org/iss-now.json');
  44 |       duration_ms = Date.now() - start;
  45 |     });
  46 | 
  47 |     await test.step('Validar resposta', async () => {
  48 |       expect(response.status()).toBe(200);
  49 |       expect(response.ok()).toBeTruthy();
> 50 |       expect(duration_ms).toBeLessThan(4000);
     |                           ^ Error: expect(received).toBeLessThan(expected)
  51 | 
  52 |       const data = await response.json();
  53 |       const validation = issSchema.safeParse(data);
  54 |       if (!validation.success) console.error('Contrato inválido:', validation.error.format());
  55 |       expect(validation.success, 'Contrato Zod válido').toBeTruthy();
  56 | 
  57 |       expect(data.message).toBe('success');
  58 |       expect(typeof data.timestamp).toBe('number');
  59 |       expect(data.timestamp).toBeGreaterThan(0);
  60 |       expect(data.iss_position).toHaveProperty('latitude');
  61 |       expect(data.iss_position).toHaveProperty('longitude');
  62 |     });
  63 |   });
  64 | 
  65 | });
  66 | 
```