import { test as base, APIRequestContext } from '@playwright/test';
import { ApiClient } from '../api/clients/ApiClient';

type MyFixtures = {
  apiClient: ApiClient;
  apiRequest: APIRequestContext;
};

export const test = base.extend<MyFixtures>({
  apiRequest: async ({ playwright }, use) => {
    const ctx = await playwright.request.newContext({ ignoreHTTPSErrors: true });
    await use(ctx);
    await ctx.dispose();
  },
  apiClient: async ({ apiRequest }, use) => {
    await use(new ApiClient(apiRequest));
  },
});

export { expect } from '@playwright/test';
