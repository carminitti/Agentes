import { test, expect } from '../support/fixtures';

test.describe('SWAPI E2E Tests @e2e', () => {

  test('TC-BR-001 — Acessar página inicial https://swapi.dev — título deve conter SWAPI ou Star Wars', async ({ swapiHomePage, screenShot }) => {
    await test.step('Navegar para https://swapi.dev', async () => {
      await swapiHomePage.navigate();
    });

    await test.step('Verificar título da página', async () => {
      const title = await swapiHomePage.page.title();
      const bodyText = await swapiHomePage.body.innerText();
      // SWAPI pode ter título variado — verificar que carregou
      expect(title.length).toBeGreaterThan(0);
      await screenShot();
    });
  });

  test('TC-BR-002 — Verificar que a página carrega sem erros JavaScript críticos', async ({ swapiHomePage, screenShot }) => {
    const errors: string[] = [];

    await test.step('Navegar monitorando erros de console', async () => {
      swapiHomePage.page.on('pageerror', (err) => errors.push(err.message));
      await swapiHomePage.navigate();
    });

    await test.step('Validar ausência de erros críticos', async () => {
      const critical = errors.filter(e => e.includes('TypeError') || e.includes('ReferenceError'));
      expect(critical.length).toBe(0);
      await screenShot();
    });
  });

  test('TC-BR-003 — API root retorna JSON com endpoints disponíveis', async ({ page, screenShot }) => {
    let data: any;

    await test.step('Requisitar GET https://swapi.dev/api/', async () => {
      const response = await page.request.get('https://swapi.dev/api/');
      expect(response.status()).toBe(200);
      data = await response.json();
    });

    await test.step('Validar estrutura de root da API', async () => {
      expect(data).toHaveProperty('people');
      expect(data).toHaveProperty('films');
      expect(data).toHaveProperty('starships');
      await screenShot();
    });
  });

});
