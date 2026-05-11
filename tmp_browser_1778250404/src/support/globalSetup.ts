import { FullConfig } from '@playwright/test';
import * as fs from 'fs';

export default async function globalSetup(_config: FullConfig): Promise<void> {
  fs.mkdirSync('reports', { recursive: true });
}
