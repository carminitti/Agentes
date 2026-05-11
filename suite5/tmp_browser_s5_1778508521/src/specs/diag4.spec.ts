import { test, expect } from '../support/fixtures';

test('diag TC-001 exact flow from home', async ({ page }) => {
  page.setDefaultNavigationTimeout(60_000);

  await page.goto('https://practicesoftwaretesting.com/');
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(2000);
  console.log('Step1 URL:', page.url());

  // click sign in — same as TC-001
  const signInDataTest = page.locator('[data-test="nav-sign-in"]');
  const signInLink = page.getByRole('link', { name: /sign in/i });
  const signInBtn = page.getByRole('button', { name: /sign in/i });

  const hasDataTest = await signInDataTest.isVisible().catch(() => false);
  const hasLink = await signInLink.first().isVisible().catch(() => false);
  console.log('nav-sign-in data-test visible:', hasDataTest);
  console.log('Sign In link visible:', hasLink);

  if (hasDataTest) {
    await signInDataTest.click();
  } else if (hasLink) {
    await signInLink.first().click();
  } else {
    await signInBtn.first().click();
  }
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(1000);
  console.log('After sign-in click URL:', page.url());

  // Check login form
  const emailInput = page.locator('[data-test="email"]').or(page.locator('input[type="email"]'));
  const isEmailVisible = await emailInput.first().isVisible().catch(() => false);
  console.log('Email input visible on login form:', isEmailVisible);

  if (!isEmailVisible) {
    // Maybe we're already on account page or there's a modal
    console.log('Current page title:', await page.title());
    const allInputs = await page.locator('input').count();
    console.log('Total inputs on page:', allInputs);
  }

  expect(true).toBeTruthy();
});
