import { test, expect } from '@playwright/test';

test.describe('TC-BROWSER-S6-002 -- Practice Software Testing Cart @e2e', () => {
  test('Adicionar produto ao carrinho', async ({ page }) => {
    page.setDefaultNavigationTimeout(60_000);
    page.setDefaultTimeout(30_000);

    await test.step('Navegar para pagina de login via UI', async () => {
      // Acessar a home primeiro para o Angular carregar
      await page.goto('https://practicesoftwaretesting.com/', { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(3000);

      // Clicar no link de login no nav (icone de usuario ou texto "Sign in")
      const signinLink = page.locator('a[routerlink="/auth/login"], a:has-text("Sign in"), a[data-test="nav-sign-in"]').first();
      await signinLink.waitFor({ state: 'visible', timeout: 15_000 });
      await signinLink.click();
      await page.waitForTimeout(3000);
    });

    await test.step('Preencher credenciais e fazer login', async () => {
      // Aguardar campos de email/password
      await page.waitForSelector('input[data-test="email"], input[id="email"], [formcontrolname="email"]', { timeout: 15_000 });

      const emailInput = page.locator('input[data-test="email"], input[id="email"], [formcontrolname="email"]').first();
      await emailInput.fill('customer@practicesoftwaretesting.com');

      const passInput = page.locator('input[data-test="password"], input[type="password"]').first();
      await passInput.fill('welcome01');

      const loginBtn = page.locator('button[data-test="login-submit"], input[type="submit"], button[type="submit"]').first();
      await loginBtn.click();
      await page.waitForTimeout(3000);
    });

    await test.step('Acessar listagem de produtos', async () => {
      // Navegar para home/produtos
      await page.goto('https://practicesoftwaretesting.com/', { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(3000);
      await page.waitForSelector('.card, [class*="product-card"]', { timeout: 20_000 });
    });

    let cartBefore = 0;

    await test.step('Obter contador do carrinho antes', async () => {
      try {
        const badge = page.locator('.badge, [data-test="cart-quantity"]').first();
        const txt = await badge.textContent({ timeout: 3000 }).catch(() => '0');
        cartBefore = parseInt(txt?.trim() || '0', 10) || 0;
      } catch { cartBefore = 0; }
      console.log(`[INFO] Cart antes: ${cartBefore}`);
    });

    await test.step('Clicar no primeiro produto', async () => {
      const firstCard = page.locator('.card').first();
      await firstCard.click();
      await page.waitForTimeout(3000);
    });

    await test.step('Adicionar ao carrinho', async () => {
      const addBtn = page.locator('[data-test="add-to-cart"], button:has-text("Add to cart")').first();
      await addBtn.waitFor({ state: 'visible', timeout: 15_000 });
      await addBtn.click();
      await page.waitForTimeout(3000);
    });

    await test.step('Validar confirmacao', async () => {
      const toast = page.locator('.toast, [role="alert"], [data-test="success-message"]').first();
      const toastVisible = await toast.isVisible({ timeout: 5000 }).catch(() => false);

      let cartAfter = 0;
      try {
        const badge = page.locator('.badge, [data-test="cart-quantity"]').first();
        const txt = await badge.textContent({ timeout: 3000 }).catch(() => '0');
        cartAfter = parseInt(txt?.trim() || '0', 10) || 0;
      } catch { cartAfter = 0; }

      const cartIncremented = cartAfter > cartBefore;
      console.log(`[INFO] Toast: ${toastVisible}, cart antes=${cartBefore}, depois=${cartAfter}`);

      expect(toastVisible || cartIncremented, 'Confirmacao de adicao ao carrinho deve aparecer').toBeTruthy();
      await page.screenshot({ path: 'test-results/TC-BROWSER-S6-002.png' });
    });
  });
});
