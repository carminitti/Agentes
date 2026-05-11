import { test, expect } from '../support/fixtures';
import { request } from '@playwright/test';

test.describe('Login @smoke @sanity @e2e', () => {

  // TC-CL-001: Smoke — página de login carrega corretamente
  test('TC-CL-001 — Verificar se a página de login carrega corretamente', async ({ loginPage, page }) => {
    await test.step('Acessar a página de login', async () => {
      await loginPage.navigate();
    });

    await test.step('Verificar elementos obrigatórios presentes', async () => {
      await expect(loginPage.formLogin).toBeVisible();
      await expect(loginPage.inputEmail).toBeVisible();
      await expect(loginPage.inputPassword).toBeVisible();
      await expect(loginPage.btnLogin).toBeVisible();
    });
  });

  // TC-CL-002: E2E — login com credenciais válidas
  test('TC-CL-002 — Verificar login com credenciais válidas', async ({ loginPage, page }) => {
    await test.step('Acessar a página de login', async () => {
      await loginPage.navigate();
    });

    await test.step('Preencher credenciais e submeter', async () => {
      await loginPage.login(
        process.env.USER_EMAIL as string,
        process.env.USER_PASSWORD as string
      );
    });

    await test.step('Verificar redirecionamento para home autenticada', async () => {
      await expect(loginPage.loggedInAs).toBeVisible({ timeout: 10_000 });
    });
  });

  // TC-CL-003: E2E — login com credenciais inválidas exibe erro
  test('TC-CL-003 — Verificar login com credenciais inválidas', async ({ loginPage }) => {
    await test.step('Acessar a página de login', async () => {
      await loginPage.navigate();
    });

    await test.step('Preencher credenciais inválidas e submeter', async () => {
      await loginPage.login('wrong@email.com', 'wrongpass');
    });

    await test.step('Verificar mensagem de erro', async () => {
      await expect(loginPage.errorMessage).toBeVisible({ timeout: 5_000 });
    });
  });

  // TC-CL-004: Sanity http — API de produtos retorna status 200
  test('TC-CL-004 — Verificar se a API de produtos retorna status 200', async ({ page }) => {
    let statusCode: number;
    let body: unknown;

    await test.step('Fazer GET /api/productsList', async () => {
      const ctx = await (page.context().request as unknown as { newContext?: never });
      const apiCtx = await request.newContext({ baseURL: process.env.BASE_URL });
      const resp = await apiCtx.get('/api/productsList');
      statusCode = resp.status();
      body = await resp.json();
      await apiCtx.dispose();
    });

    await test.step('Verificar status 200 e lista de produtos', async () => {
      expect(statusCode!).toBe(200);
      const data = body as { products?: unknown[] };
      expect(Array.isArray(data.products) && data.products.length > 0).toBeTruthy();
    });
  });

});
