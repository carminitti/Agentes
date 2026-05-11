import { test } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import * as fs from 'fs';
import * as path from 'path';

const SUITE_DIR = 'suite_api_browser_k6_visual_axe_zap_db_20260511_100754';
const outputDir = path.join(SUITE_DIR, 'acessibilidade');
fs.mkdirSync(outputDir, { recursive: true });

interface ViolationResult {
  rule_id: string;
  impact: string;
  description: string;
  affected_elements: string[];
  how_to_fix: string;
  help_url: string;
  known_environment_failure: boolean;
  known_failure_note: string | null;
}

interface TestResult {
  id: string;
  title: string;
  status: string;
  deploy_blocked: boolean;
  violations: ViolationResult[];
  passes_count: number;
  logs: string[];
  error: string | null;
}

const results: TestResult[] = [];
const logLines: string[] = [];
const nowStr = () => new Date().toISOString().replace('T', ' ').slice(0, 19);

test('TC-A11Y-S3-001 — Conformidade WCAG 2.1 AA no formulario de pratica', async ({ page }) => {
  logLines.push('[' + nowStr() + '] [TC-A11Y-S3-001] inicio');
  const logs: string[] = [];

  await page.goto('https://practiceautomation.com/practice-form/');
  logs.push('[NAV] Acessando https://practiceautomation.com/practice-form/');

  // Aguardar formulario
  try {
    await page.waitForSelector('form', { timeout: 15000 });
    logs.push('[WAIT] Formulario visivel');
  } catch {
    await page.waitForLoadState('domcontentloaded');
    logs.push('[WAIT] domcontentloaded (fallback)');
  }

  logs.push('[ANALYSIS] Executando axe-core (WCAG 2.1 AA)');
  const axeResults = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
    .analyze();

  const violations: ViolationResult[] = axeResults.violations.map(v => ({
    rule_id: v.id,
    impact: v.impact || 'unknown',
    description: v.description,
    affected_elements: v.nodes.map(n => n.html).slice(0, 3),
    how_to_fix: v.nodes[0]?.failureSummary || '',
    help_url: v.helpUrl,
    known_environment_failure: false,
    known_failure_note: null,
  }));

  for (const v of violations) {
    logs.push('[VIOLATION] ' + v.rule_id + ' (' + v.impact + '): ' + v.affected_elements.length + ' elementos');
  }

  const hasCritical = violations.some(v => v.impact === 'critical');
  const hasSerious = violations.some(v => v.impact === 'serious');
  const status = (hasCritical || hasSerious) ? 'failed' : (violations.length > 0 ? 'warning' : 'passed');
  const deploy_blocked = hasCritical || hasSerious;

  logs.push('[RESULT] ' + violations.length + ' violacoes encontradas — ' + status);

  results.push({
    id: 'TC-A11Y-S3-001',
    title: 'Conformidade WCAG 2.1 AA no formulario de pratica',
    status,
    deploy_blocked,
    violations,
    passes_count: axeResults.passes.length,
    logs,
    error: null,
  });

  logLines.push('[' + nowStr() + ']   -> STATUS: ' + status.toUpperCase());
});

test('TC-A11Y-S3-002 — Conformidade WCAG 2.1 AA na pagina inicial de citacoes', async ({ page }) => {
  logLines.push('[' + nowStr() + '] [TC-A11Y-S3-002] inicio');
  const logs: string[] = [];

  await page.goto('https://quotes.toscrape.com/');
  logs.push('[NAV] Acessando https://quotes.toscrape.com/');

  await page.waitForSelector('div.quote', { timeout: 15000 });
  logs.push('[WAIT] div.quote visivel');

  logs.push('[ANALYSIS] Executando axe-core (WCAG 2.1 AA)');
  const axeResults = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
    .analyze();

  const violations: ViolationResult[] = axeResults.violations.map(v => ({
    rule_id: v.id,
    impact: v.impact || 'unknown',
    description: v.description,
    affected_elements: v.nodes.map(n => n.html).slice(0, 3),
    how_to_fix: v.nodes[0]?.failureSummary || '',
    help_url: v.helpUrl,
    known_environment_failure: false,
    known_failure_note: null,
  }));

  for (const v of violations) {
    logs.push('[VIOLATION] ' + v.rule_id + ' (' + v.impact + '): ' + v.affected_elements.length + ' elementos');
  }

  const hasCritical = violations.some(v => v.impact === 'critical');
  const hasSerious = violations.some(v => v.impact === 'serious');
  const status = (hasCritical || hasSerious) ? 'failed' : (violations.length > 0 ? 'warning' : 'passed');
  const deploy_blocked = hasCritical || hasSerious;

  logs.push('[RESULT] ' + violations.length + ' violacoes encontradas — ' + status);
  if (!deploy_blocked) logs.push('[RESULT] deploy_blocked: false');

  results.push({
    id: 'TC-A11Y-S3-002',
    title: 'Conformidade WCAG 2.1 AA na pagina inicial de citacoes',
    status,
    deploy_blocked,
    violations,
    passes_count: axeResults.passes.length,
    logs,
    error: null,
  });

  logLines.push('[' + nowStr() + ']   -> STATUS: ' + status.toUpperCase());
});

test.afterAll(async () => {
  const passed = results.filter(r => r.status === 'passed').length;
  const failed = results.filter(r => r.status === 'failed').length;
  const warning = results.filter(r => r.status === 'warning').length;

  const byImpact = { critical: 0, serious: 0, moderate: 0, minor: 0 };
  for (const r of results) {
    for (const v of r.violations) {
      const imp = v.impact as keyof typeof byImpact;
      if (imp in byImpact) byImpact[imp]++;
    }
  }

  const outputJson = {
    executor: 'axe-core',
    environment: 'practiceautomation.com / quotes.toscrape.com',
    wcag_level: 'wcag2aa',
    results,
    summary: {
      total: results.length,
      passed,
      failed,
      warning,
      known_environment_failures: 0,
      total_violations: results.reduce((acc, r) => acc + r.violations.length, 0),
      by_impact: byImpact,
    },
  };

  fs.writeFileSync(path.join(outputDir, 'resultado.json'), JSON.stringify(outputJson, null, 2));

  logLines.push('[' + nowStr() + '] === Fim: ' + passed + ' passou, ' + failed + ' falhou, ' + warning + ' aviso ===');
  fs.writeFileSync(path.join(outputDir, 'execution.log'), logLines.join('\n'));

  console.log(JSON.stringify(outputJson, null, 2));
});
