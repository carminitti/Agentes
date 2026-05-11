import { defineConfig } from '@playwright/test';
export default defineConfig({
  timeout: 30000, workers: 1, retries: 0,
  testMatch: ['**/*.spec.ts'],
  snapshotDir: './snapshots',
  reporter: [['json', { outputFile: 'resultado_visual.json' }]],
  use: { headless: true, viewport: { width: 1280, height: 720 }, ignoreHTTPSErrors: true, animations: 'disabled' },
});
