import { defineConfig } from '@playwright/test';

export default defineConfig({
  timeout: 45_000,
  fullyParallel: false,
  workers: 1,
  retries: 0,
  testMatch: ['*.spec.ts'],
  reporter: [['json', { outputFile: 'results.json' }]],
  use: {
    headless: true,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
  },
  snapshotDir: './baselines',
  updateSnapshots: 'missing',
});
