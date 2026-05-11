import { test as base } from '@playwright/test';
import { SwapiHomePage } from '../pages/SwapiHomePage';

type MyFixtures = {
  swapiHomePage: SwapiHomePage;
  screenShot: () => Promise<void>;
};

export const test = base.extend<MyFixtures>({
  swapiHomePage: async ({ page }, use) => { await use(new SwapiHomePage(page)); },
  screenShot: async ({ page }, use, testInfo) => {
    await use(async () => {
      const s = await page.screenshot();
      await testInfo.attach(`screenshot-${Date.now()}`, { body: s, contentType: 'image/png' });
    });
  },
});

export { expect } from '@playwright/test';
