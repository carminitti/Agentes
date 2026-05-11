import { test, expect } from '../../support/fixtures';
import { countrySchema } from '../schemas/country.schema';
import { issSchema } from '../schemas/iss.schema';

test.describe('Public APIs Suite5 @api', () => {

  test('TC-API-S5-001 — Consultar dados do Brasil na Countries REST API', async ({ apiClient }) => {
    let response: Awaited<ReturnType<typeof apiClient.get>>;
    let duration_ms: number;

    await test.step('Enviar GET /name/brazil', async () => {
      const start = Date.now();
      response = await apiClient.get('https://restcountries.com/v3.1/name/brazil');
      duration_ms = Date.now() - start;
    });

    await test.step('Validar resposta', async () => {
      expect(response.status()).toBe(200);
      expect(response.ok()).toBeTruthy();
      expect(duration_ms).toBeLessThan(4000);

      const data = await response.json();
      expect(Array.isArray(data)).toBeTruthy();
      expect(data.length).toBeGreaterThanOrEqual(1);

      const country = data[0];
      const validation = countrySchema.safeParse(country);
      if (!validation.success) console.error('Contrato inválido:', validation.error.format());
      expect(validation.success, 'Contrato Zod válido').toBeTruthy();

      expect(country.name.common).toBe('Brazil');
      expect(country.population).toBeGreaterThan(0);
      expect(country.currencies).toHaveProperty('BRL');
    });
  });

  test('TC-API-S5-002 — Consultar posição atual da ISS via Open Notify', async ({ apiClient }) => {
    let response: Awaited<ReturnType<typeof apiClient.get>>;
    let duration_ms: number;

    await test.step('Enviar GET /iss-now.json', async () => {
      const start = Date.now();
      response = await apiClient.get('http://api.open-notify.org/iss-now.json');
      duration_ms = Date.now() - start;
    });

    await test.step('Validar resposta', async () => {
      expect(response.status()).toBe(200);
      expect(response.ok()).toBeTruthy();
      expect(duration_ms).toBeLessThan(4000);

      const data = await response.json();
      const validation = issSchema.safeParse(data);
      if (!validation.success) console.error('Contrato inválido:', validation.error.format());
      expect(validation.success, 'Contrato Zod válido').toBeTruthy();

      expect(data.message).toBe('success');
      expect(typeof data.timestamp).toBe('number');
      expect(data.timestamp).toBeGreaterThan(0);
      expect(data.iss_position).toHaveProperty('latitude');
      expect(data.iss_position).toHaveProperty('longitude');
    });
  });

});
