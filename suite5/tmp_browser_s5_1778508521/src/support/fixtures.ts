import { test as base } from '@playwright/test';
import { captureScreenshot } from './utils';

type MyFixtures = {
  screenShot: () => Promise<void>;
};

export const test = base.extend<MyFixtures>({
  screenShot: async ({ page }, use, testInfo) => {
    await use(async () => { await captureScreenshot(page, testInfo); });
  },
});

export { expect } from '@playwright/test';
