import { test as base, APIRequestContext } from '@playwright/test';
import { UsuariosPage } from '../pages/UsuariosPage';
import { captureScreenshot } from './utils';

type MyFixtures = {
  usuariosPage: UsuariosPage;
  apiRequest: APIRequestContext;
  screenShot: () => Promise<void>;
};

export const test = base.extend<MyFixtures>({
  usuariosPage: async ({ page }, use) => {
    await use(new UsuariosPage(page));
  },
  apiRequest: async ({ playwright }, use) => {
    const ctx = await playwright.request.newContext({ baseURL: process.env.BASE_URL });
    await use(ctx);
    await ctx.dispose();
  },
  screenShot: async ({ page }, use, testInfo) => {
    await use(async () => { await captureScreenshot(page, testInfo); });
  },
});

export { expect } from '@playwright/test';
