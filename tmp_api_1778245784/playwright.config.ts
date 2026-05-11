import { defineConfig } from '@playwright/test';

export default defineConfig({
  timeout: 30000,
  expect: { timeout: 5000 },
  fullyParallel: true,
  workers: 4,
  retries: 0,
  testMatch: ['**/*.spec.ts'],
  reporter: [['json', { outputFile: 'resultado.json' }]],
  use: {
    ignoreHTTPSErrors: true,
    baseURL: 'https://swapi.dev/api',
  },
});
