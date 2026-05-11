import { test } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import * as fs from 'fs';
import * as path from 'path';

test('TC-A11Y-001 - Acessibilidade da pagina inicial (WCAG 2.1 AA)', async ({ page }) => {
  const logs: string[] = [];

  logs.push('[NAV] Acessando https://automationexercise.com');
  await page.goto('https://automationexercise.com', { waitUntil: 'networkidle' });
  logs.push('[ANALYSIS] Executando axe-core (WCAG 2.1 AA)');

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
    .analyze();

  const violations = results.violations;
  const passesCount = results.passes.length;

  // Identify known demo failures (color contrast)
  const KNOWN_DEMO_FAILURE_RULES = ['color-contrast'];

  const violationsProcessed = violations.map((v) => {
    const isKnown = KNOWN_DEMO_FAILURE_RULES.includes(v.id);
    return {
      rule_id: v.id,
      impact: v.impact,
      description: v.description,
      affected_elements: v.nodes.slice(0, 5).map((n) => n.target.join(', ')),
      how_to_fix: v.nodes[0]?.failureSummary || '',
      help_url: v.helpUrl,
      known_environment_failure: isKnown,
      known_failure_note: isKnown ? 'falha conhecida do ambiente de demonstracao - nao corrigivel pelo time' : null
    };
  });

  // Determine status
  const nonKnownViolations = violationsProcessed.filter(v => !v.known_environment_failure);
  const hasCriticalOrSerious = nonKnownViolations.some(v => v.impact === 'critical' || v.impact === 'serious');
  const hasModerateOrMinor = nonKnownViolations.some(v => v.impact === 'moderate' || v.impact === 'minor');

  let status = 'passed';
  if (hasCriticalOrSerious) {
    status = 'failed';
  } else if (hasModerateOrMinor || violations.length > 0) {
    status = 'warning';
  }

  // deploy_blocked: false if all failed violations are known_environment_failure
  const allFailedAreKnown = violations.length === 0 ||
    violationsProcessed.filter(v => v.impact === 'critical' || v.impact === 'serious').every(v => v.known_environment_failure);
  const deployBlocked = status === 'failed' && !allFailedAreKnown;

  for (const v of violationsProcessed) {
    const mark = v.known_environment_failure ? '[KNOWN_DEMO]' : `[${v.impact?.toUpperCase()}]`;
    logs.push(`[VIOLATION] ${v.rule_id} (${v.impact}): ${v.affected_elements.length} elementos afetados ${mark}`);
  }
  logs.push(`[RESULT] ${violations.length} violacoes encontradas — ${status}; deploy_blocked: ${deployBlocked}`);

  const output = {
    executor: 'axe-core',
    environment: 'https://automationexercise.com',
    wcag_level: 'wcag2aa',
    results: [
      {
        id: 'TC-A11Y-001',
        title: 'Acessibilidade da pagina inicial',
        status: status,
        deploy_blocked: deployBlocked,
        violations: violationsProcessed,
        passes_count: passesCount,
        logs: logs,
        error: null
      }
    ],
    summary: {
      total: 1,
      passed: status === 'passed' ? 1 : 0,
      failed: status === 'failed' ? 1 : 0,
      warning: status === 'warning' ? 1 : 0,
      known_environment_failures: violationsProcessed.filter(v => v.known_environment_failure).length,
      total_violations: violations.length,
      by_impact: {
        critical: violations.filter(v => v.impact === 'critical').length,
        serious: violations.filter(v => v.impact === 'serious').length,
        moderate: violations.filter(v => v.impact === 'moderate').length,
        minor: violations.filter(v => v.impact === 'minor').length
      }
    }
  };

  const outPath = path.join(__dirname, 'a11y_result.json');
  fs.writeFileSync(outPath, JSON.stringify(output, null, 2), 'utf-8');
  console.log(JSON.stringify(output, null, 2));
});
