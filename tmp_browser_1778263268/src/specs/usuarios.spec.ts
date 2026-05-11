import { test, expect } from '../support/fixtures';

test.describe('Autenticação e Listagem de Usuários @smoke', () => {

  test.beforeAll(async () => {
    if (process.env.SETUP_FAILED) {
      console.warn(`[SETUP] SETUP_FAILED detectado: ${process.env.SETUP_FAILED}`);
    }
  });

  test('TC-B01 — Usuário autenticado visualiza lista de usuários', async ({ usuariosPage, screenShot }) => {
    if (process.env.SETUP_FAILED) {
      test.fail(true, `Falha no setup: ${process.env.SETUP_FAILED}`);
      return;
    }

    await test.step('Realizar login com as credenciais fornecidas', async () => {
      // Autenticação ocorre via AUTH_TOKEN gerado pelo globalSetup
      // Se o token não estiver disponível (SETUP_FAILED), o teste é marcado como FAIL acima
      await usuariosPage.navigate('/');
    });

    await test.step('Navegar para a área de usuários', async () => {
      await usuariosPage.navigateToUsers();
    });

    await test.step('Verificar que a lista de usuários é exibida', async () => {
      // A API /api/users retorna JSON com campo "data" contendo a lista
      await expect(usuariosPage.page).toHaveURL(/users/);
      const bodyText = await usuariosPage.page.locator('body').textContent();
      expect(bodyText).toContain('"data"');
      await screenShot();
    });
  });

});
