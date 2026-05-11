import { test as base, APIRequestContext } from '@playwright/test';
import { ApiClient } from '../api/clients/ApiClient';

type MyFixtures = { apiClient: ApiClient; };

export const test = base.extend<MyFixtures>({
  apiClient: async ({ playwright }, use) => {
    const ctx = await playwright.request.newContext({
      ignoreHTTPSErrors: true,
    });
    await use(new ApiClient(ctx));
    await ctx.dispose();
  },
});
export { expect } from '@playwright/test';
