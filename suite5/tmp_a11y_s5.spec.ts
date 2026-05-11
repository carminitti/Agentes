import { test } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import * as fs from 'fs';
import * as path from 'path';

const SUITE_DIR = 'C:/Users/gabriel.carminitti/Documents/claude/agentes/suite5/suite_http_magnitude_k6_visual_axe_zap_db_20260511_100000';
const OUTPUT_DIR = path.join(SUITE_DIR, 'acessibilidade');

function ts() { return new Date().toISOString().replace('T', ' ').slice(0, 19); }

const results: any[] = [];

test.describe('Acessibilidade WCAG 2.1 AA Suite 5', () => {

  test.afterAll(() => {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    const passed = results.filter(r => r.status === 'passed').length;
    const failed = results.filter(r => r.status === 'failed').length;
    const warning = results.filter(r => r.status === 'warning').length;

    const outputJson = {
      executor: 'axe-core',
      environment: 'https://www.w3.org + https://developer.mozilla.org',
      wcag_level: 'wcag2aa',
      results,
      summary: {
        total: results.length,
        passed,
        failed,
        warning,
        known_environment_failures: 0,
        total_violations: results.reduce((acc, r) => acc + (r.violations?.length || 0), 0),
        by_impact: {
          critical: results.flatMap(r => r.violations || []).filter(v => v.impact === 'critical').length,
          serious: results.flatMap(r => r.violations || []).filter(v => v.impact === 'serious').length,
          moderate: results.flatMap(r => r.violations || []).filter(v => v.impact === 'moderate').length,
          minor: results.flatMap(r => r.violations || []).filter(v => v.impact === 'minor').length,
        }
      }
    };

    fs.writeFileSync(path.join(OUTPUT_DIR, 'resultado.json'), JSON.stringify(outputJson, null, 2));

    const logLines = [`[${ts()}] === executor-acessibilidade — inicio ===`, `[${ts()}] WCAG: wcag2aa\n`];
    for (const r of results) {
      logLines.push(`[${ts()}] [${r.id}] ${r.title}`);
      for (const line of r.logs || []) logLines.push(`[${ts()}]   ${line}`);
      logLines.push(`[${ts()}]   -> STATUS: ${r.status.toUpperCase()}\n`);
    }
    logLines.push(`[${ts()}] === Fim: ${passed} passou, ${failed} falhou, ${warning} aviso ===`);
    fs.writeFileSync(path.join(OUTPUT_DIR, 'execution.log'), logLines.join('\n'));

    console.log(`Resultado salvo em: ${OUTPUT_DIR}`);
  });

  test('TC-A11Y-S5-001 - Conformidade WCAG 2.1 AA na pagina de padroes WCAG do W3C', async ({ page }) => {
    const logs: string[] = [];
    const url = 'https://www.w3.org/WAI/standards-guidelines/wcag/';

    logs.push(`[NAV] Acessando ${url}`);
    await page.goto(url);
    await page.waitForLoadState('domcontentloaded');
    await page.waitForSelector('main', { timeout: 20_000 });
    logs.push('[ANALYSIS] Executando axe-core (WCAG 2.1 AA)');

    const axeResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
      .analyze();

    const violations = axeResults.violations.map(v => ({
      rule_id: v.id,
      impact: v.impact,
      description: v.description,
      affected_elements: v.nodes.slice(0, 3).map(n => n.target[0] || '?'),
      how_to_fix: v.help,
      help_url: v.helpUrl,
      known_environment_failure: false,
      known_failure_note: null
    }));

    const critical = violations.filter(v => v.impact === 'critical').length;
    const serious = violations.filter(v => v.impact === 'serious').length;
    const moderate = violations.filter(v => v.impact === 'moderate').length;
    const minor = violations.filter(v => v.impact === 'minor').length;

    for (const v of violations) {
      logs.push(`[VIOLATION] ${v.rule_id} (${v.impact}): ${v.affected_elements.length} elemento(s)`);
    }

    const status = (critical > 0 || serious > 0) ? 'failed' : (moderate > 0 || minor > 0 ? 'warning' : 'passed');
    const deploy_blocked = critical > 0 || serious > 0;
    logs.push(`[RESULT] ${violations.length} violacoes encontradas — ${status}${deploy_blocked ? '; deploy bloqueado' : ''}`);

    results.push({
      id: 'TC-A11Y-S5-001',
      title: 'Conformidade WCAG 2.1 AA na pagina de padroes WCAG do W3C',
      status,
      deploy_blocked,
      violations,
      passes_count: axeResults.passes.length,
      logs,
      error: null
    });

    // Assertions
    if (critical > 0) throw new Error(`${critical} violacao(oes) critica(s) encontrada(s)`);
    if (serious > 0) throw new Error(`${serious} violacao(oes) serious encontrada(s)`);
  });

  test('TC-A11Y-S5-002 - Conformidade WCAG 2.1 AA na pagina de acessibilidade do MDN', async ({ page }) => {
    const logs: string[] = [];
    const url = 'https://developer.mozilla.org/en-US/docs/Web/Accessibility';

    logs.push(`[NAV] Acessando ${url}`);
    await page.goto(url);
    await page.waitForLoadState('domcontentloaded');
    await page.waitForSelector('main', { timeout: 20_000 });
    logs.push('[ANALYSIS] Executando axe-core (WCAG 2.1 AA)');

    const axeResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
      .analyze();

    const violations = axeResults.violations.map(v => ({
      rule_id: v.id,
      impact: v.impact,
      description: v.description,
      affected_elements: v.nodes.slice(0, 3).map(n => n.target[0] || '?'),
      how_to_fix: v.help,
      help_url: v.helpUrl,
      known_environment_failure: false,
      known_failure_note: null
    }));

    const critical = violations.filter(v => v.impact === 'critical').length;
    const serious = violations.filter(v => v.impact === 'serious').length;
    const moderate = violations.filter(v => v.impact === 'moderate').length;
    const minor = violations.filter(v => v.impact === 'minor').length;

    for (const v of violations) {
      logs.push(`[VIOLATION] ${v.rule_id} (${v.impact}): ${v.affected_elements.length} elemento(s)`);
    }

    const status = (critical > 0 || serious > 0) ? 'failed' : (moderate > 0 || minor > 0 ? 'warning' : 'passed');
    const deploy_blocked = critical > 0 || serious > 0;
    logs.push(`[RESULT] ${violations.length} violacoes encontradas — ${status}${deploy_blocked ? '; deploy bloqueado' : ''}`);

    results.push({
      id: 'TC-A11Y-S5-002',
      title: 'Conformidade WCAG 2.1 AA na pagina de acessibilidade do MDN',
      status,
      deploy_blocked,
      violations,
      passes_count: axeResults.passes.length,
      logs,
      error: null
    });

    if (critical > 0) throw new Error(`${critical} violacao(oes) critica(s) encontrada(s)`);
    if (serious > 0) throw new Error(`${serious} violacao(oes) serious encontrada(s)`);
  });

});
