import { test as base, APIRequestContext } from '@playwright/test';

type MyFixtures = {
  jsonApi: APIRequestContext;
  expandApi: APIRequestContext;
};

export const test = base.extend<MyFixtures>({
  jsonApi: async ({ playwright }, use) => {
    const ctx = await playwright.request.newContext({
      baseURL: process.env.BASE_URL_JSON || 'https://jsonplaceholder.typicode.com',
      extraHTTPHeaders: { 'Content-Type': 'application/json' },
    });
    await use(ctx);
    await ctx.dispose();
  },
  expandApi: async ({ playwright }, use) => {
    const ctx = await playwright.request.newContext({
      baseURL: process.env.BASE_URL_EXPAND || 'https://practice.expandtesting.com/notes/api',
      extraHTTPHeaders: { 'Content-Type': 'application/json' },
    });
    await use(ctx);
    await ctx.dispose();
  },
});

export { expect } from '@playwright/test';
