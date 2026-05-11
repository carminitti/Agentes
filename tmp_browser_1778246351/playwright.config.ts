import { defineConfig } from '@playwright/test';

export default defineConfig({
  timeout: 30000,
  workers: 1,
  retries: 0,
  testMatch: ['**/*.spec.ts'],
  reporter: [['json', { outputFile: 'resultado.json' }]],
  use: {
    headless: true,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
    baseURL: 'https://swapi.dev',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
});
