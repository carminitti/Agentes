import { test, expect } from '@playwright/test';

test.describe('TC-BROWSER-S6-001 -- Demoblaze Laptops @e2e', () => {
  test('Navegar ate categoria Laptops e verificar listagem', async ({ page }) => {
    page.setDefaultNavigationTimeout(60_000);
    page.setDefaultTimeout(30_000);

    await test.step('Acessar homepage Demoblaze', async () => {
      await page.goto('https://www.demoblaze.com/', { waitUntil: 'domcontentloaded' });
      // Aguardar a lista de categorias
      await page.waitForSelector('#cat', { timeout: 20_000 });
    });

    await test.step('Clicar em categoria Laptops', async () => {
      // O menu de categorias do Demoblaze tem itens de lista com texto
      await page.getByText('Laptops', { exact: true }).click();
      // Aguardar que a listagem de produtos mude
      await page.waitForTimeout(2000);
      // Verificar que ha pelo menos um card de produto visivel
      await page.waitForSelector('.card-title', { timeout: 15_000 });
    });

    await test.step('Validar listagem de Laptops', async () => {
      const cards = page.locator('.card-title');
      const count = await cards.count();
      expect(count, 'Deve haver ao menos 1 produto na categoria Laptops').toBeGreaterThan(0);

      // Verificar que há preço visível
      const prices = page.locator('.card-block h5');
      const priceCount = await prices.count();
      expect(priceCount, 'Deve haver ao menos 1 preço visível').toBeGreaterThan(0);

      await page.screenshot({ path: 'test-results/TC-BROWSER-S6-001.png', fullPage: false });
    });
  });
});
