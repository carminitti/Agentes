import { test } from '@playwright/test';

test('Inspecionar pagina de login do Practice Software Testing', async ({ page }) => {
  page.setDefaultNavigationTimeout(60_000);

  await page.goto('https://practicesoftwaretesting.com/#/auth/login', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(5000);

  // Logar o HTML para entender a estrutura
  const html = await page.content();
  const inputs = await page.$$eval('input', els => els.map(e => ({
    type: e.getAttribute('type'),
    name: e.getAttribute('name'),
    id: e.getAttribute('id'),
    placeholder: e.getAttribute('placeholder'),
    'ng-reflect': e.getAttribute('ng-reflect-name'),
    class: e.className?.substring(0, 50)
  })));
  console.log('INPUTS encontrados:', JSON.stringify(inputs, null, 2));

  const buttons = await page.$$eval('button', els => els.map(e => ({
    text: e.textContent?.trim().substring(0, 50),
    type: e.getAttribute('type'),
    class: e.className?.substring(0, 50)
  })));
  console.log('BUTTONS encontrados:', JSON.stringify(buttons, null, 2));

  await page.screenshot({ path: 'test-results/inspect-login.png', fullPage: true });
});
