import * as fs from 'fs';
export default async function globalSetup(): Promise<void> {
  fs.mkdirSync('reports', { recursive: true });
}
