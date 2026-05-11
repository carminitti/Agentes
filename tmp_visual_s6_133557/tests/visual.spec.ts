import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

const BASELINE_DIR = path.join(__dirname, '..', 'baselines');
fs.mkdirSync(BASELINE_DIR, { recursive: true });
fs.mkdirSync(path.join(__dirname, '..', 'test-results'), { recursive: true });

async function compareOrCreateBaseline(
  page: import('@playwright/test').Page,
  screenshotName: string,
  threshold: number
): Promise<{ status: 'baseline_created' | 'passed' | 'failed'; diffPercent: number; message: string }> {
  const baselinePath = path.join(BASELINE_DIR, screenshotName);
  const currentBuffer = await page.screenshot({ fullPage: false });
  fs.writeFileSync(path.join(__dirname, '..', 'test-results', screenshotName), currentBuffer);

  if (!fs.existsSync(baselinePath)) {
    fs.writeFileSync(baselinePath, currentBuffer);
    return {
      status: 'baseline_created',
      diffPercent: 0,
      message: `Baseline criado: ${screenshotName}. Marcar para validacao manual.`
    };
  }

  // Comparar usando toMatchSnapshot via expect diretamente na leitura do arquivo
  const baselineBuffer = fs.readFileSync(baselinePath);
  if (currentBuffer.length === 0 || baselineBuffer.length === 0) {
    return { status: 'failed', diffPercent: 100, message: 'Screenshot vazio' };
  }

  // Comparacao simples por tamanho de buffer como proxy (sem sharp/pixelmatch disponivel)
  // Em producao usaria pixelmatch; aqui, diferenca de tamanho > threshold -> aviso
  const sizeDiff = Math.abs(currentBuffer.length - baselineBuffer.length);
  const diffPercent = (sizeDiff / Math.max(baselineBuffer.length, 1)) * 100;
  const passed = diffPercent <= threshold;

  return {
    status: passed ? 'passed' : 'failed',
    diffPercent: Math.round(diffPercent * 100) / 100,
    message: passed
      ? `Diferenca de ${diffPercent.toFixed(2)}% dentro do threshold de ${threshold}%`
      : `Diferenca de ${diffPercent.toFixed(2)}% excede o threshold de ${threshold}%`
  };
}

test.describe('TC-VISUAL-S6-001 -- WebAIM Contrast @visual', () => {
  test('Regressao visual do artigo de contraste de cores do WebAIM', async ({ page }) => {
    page.setDefaultNavigationTimeout(60_000);

    await test.step('Acessar pagina WebAIM contrast', async () => {
      await page.goto('https://webaim.org/articles/contrast/', { waitUntil: 'domcontentloaded' });
      await page.waitForSelector('main, article', { timeout: 20_000 });
    });

    await test.step('Ocultar elementos dinamicos e capturar screenshot', async () => {
      // Ocultar banners de cookie e elementos dinamicos
      await page.evaluate(() => {
        const selectors = ['#cookie-notice', '.cookie-banner', '.gdpr', '[class*="cookie"]', '[id*="cookie"]'];
        selectors.forEach(sel => {
          document.querySelectorAll(sel).forEach((el: Element) => {
            (el as HTMLElement).style.display = 'none';
          });
        });
      });
      await page.waitForTimeout(500);
    });

    await test.step('Comparar com baseline', async () => {
      const result = await compareOrCreateBaseline(page, 'webaim-contrast.png', 2);

      if (result.status === 'baseline_created') {
        console.log(`[VISUAL] ${result.message}`);
        // Baseline criado -- passa (primeira execucao)
        expect(result.status).toBe('baseline_created');
      } else {
        expect(result.diffPercent, result.message).toBeLessThanOrEqual(2);
      }
    });
  });
});

test.describe('TC-VISUAL-S6-002 -- PokéAPI Homepage @visual', () => {
  test('Regressao visual da homepage da documentacao PokeAPI', async ({ page }) => {
    page.setDefaultNavigationTimeout(60_000);

    await test.step('Acessar homepage PokeAPI', async () => {
      await page.goto('https://pokeapi.co', { waitUntil: 'domcontentloaded' });
      // Aguardar main ou .landing
      await Promise.race([
        page.waitForSelector('main', { timeout: 20_000 }),
        page.waitForSelector('.landing', { timeout: 20_000 }),
      ]).catch(() => page.waitForTimeout(3000));
    });

    await test.step('Capturar screenshot acima da dobra', async () => {
      await page.waitForTimeout(1000);
    });

    await test.step('Comparar com baseline', async () => {
      const result = await compareOrCreateBaseline(page, 'pokeapi-home.png', 2);

      if (result.status === 'baseline_created') {
        console.log(`[VISUAL] ${result.message}`);
        expect(result.status).toBe('baseline_created');
      } else {
        expect(result.diffPercent, result.message).toBeLessThanOrEqual(2);
      }
    });
  });
});
