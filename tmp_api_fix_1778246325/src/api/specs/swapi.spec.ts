import { test, expect } from '../../support/fixtures';
import { peopleSchema } from '../schemas/people.schema';
import { starshipSchema } from '../schemas/starship.schema';

test.describe('SWAPI Integration Tests @api', () => {

  test('TC-API-001 — API client: GET /api/people/1/ retorna 200', async ({ apiClient }) => {
    let response: Awaited<ReturnType<typeof apiClient.getById>>;

    await test.step('Requisitar Luke Skywalker via API client', async () => {
      response = await apiClient.getById('people', '1');
    });

    await test.step('Validar status e contrato Zod People', async () => {
      expect(response.status()).toBe(200);
      expect(response.ok()).toBeTruthy();
      const data = await response.json();
      expect(data.name).toBe('Luke Skywalker');
      const validation = peopleSchema.safeParse(data);
      if (!validation.success) console.error('Contrato inválido:', JSON.stringify(validation.error.format()));
      expect(validation.success, 'Contrato People deve ser válido').toBeTruthy();
    });
  });

  test('TC-API-002 — Schema Zod People: validar campos name, height, mass, birth_year, gender, films, url', async ({ apiClient }) => {
    let response: Awaited<ReturnType<typeof apiClient.getById>>;

    await test.step('Requisitar /api/people/1/', async () => {
      response = await apiClient.getById('people', '1');
    });

    await test.step('Validar todos os campos do schema Zod', async () => {
      expect(response.status()).toBe(200);
      const data = await response.json();
      const validation = peopleSchema.safeParse(data);
      expect(validation.success, 'Schema Zod People completo deve ser válido').toBeTruthy();
      if (validation.success) {
        expect(typeof validation.data.name).toBe('string');
        expect(typeof validation.data.height).toBe('string');
        expect(typeof validation.data.mass).toBe('string');
        expect(typeof validation.data.birth_year).toBe('string');
        expect(typeof validation.data.gender).toBe('string');
        expect(Array.isArray(validation.data.films)).toBeTruthy();
        expect(typeof validation.data.url).toBe('string');
      }
    });
  });

  test('TC-API-003 — Buscar Millennium Falcon: GET /api/starships/10/ retorna name correto', async ({ apiClient }) => {
    let response: Awaited<ReturnType<typeof apiClient.getById>>;

    await test.step('Requisitar Starships/10', async () => {
      response = await apiClient.getById('starships', '10');
    });

    await test.step('Validar status, contrato e name == Millennium Falcon', async () => {
      expect(response.status()).toBe(200);
      expect(response.ok()).toBeTruthy();
      const data = await response.json();
      const validation = starshipSchema.safeParse(data);
      if (!validation.success) console.error('Contrato inválido:', JSON.stringify(validation.error.format()));
      expect(validation.success, 'Contrato Starship deve ser válido').toBeTruthy();
      expect(data.name).toBe('Millennium Falcon');
    });
  });

  test('TC-API-004 — GET /api/people/ retorna lista paginada com count e results', async ({ apiClient }) => {
    let response: Awaited<ReturnType<typeof apiClient.getAll>>;

    await test.step('Requisitar listagem de People', async () => {
      response = await apiClient.getAll('people');
    });

    await test.step('Validar estrutura de resposta paginada', async () => {
      expect(response.status()).toBe(200);
      const data = await response.json();
      expect(data).toHaveProperty('count');
      expect(data).toHaveProperty('results');
      expect(Array.isArray(data.results)).toBeTruthy();
      expect(data.results.length).toBeGreaterThan(0);
    });
  });

});
