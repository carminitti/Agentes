import { defineConfig } from '@playwright/test';
export default defineConfig({
  timeout: 60000, workers: 1, retries: 0,
  testMatch: ['**/*.spec.ts'],
  reporter: [['json', { outputFile: 'resultado_a11y.json' }]],
  use: { headless: true, ignoreHTTPSErrors: true },
});
