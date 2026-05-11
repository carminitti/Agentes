import { test } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('TC-A11Y-001 — axe-core WCAG 2.1 AA — https://swapi.dev', async ({ page }) => {
  await test.step('Navegar para https://swapi.dev', async () => {
    await page.goto('https://swapi.dev/');
    await page.waitForLoadState('domcontentloaded');
  });

  await test.step('Executar análise axe-core', async () => {
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
      .analyze();
    
    const violations = results.violations;
    console.log('TOTAL_VIOLATIONS:' + violations.length);
    console.log('VIOLATIONS_JSON:' + JSON.stringify(violations.map(v => ({
      rule_id: v.id,
      impact: v.impact,
      description: v.description,
      affected_elements: v.nodes.map((n: any) => n.target.join(' ')).slice(0, 3),
      help_url: v.helpUrl
    }))));
    
    const critical = violations.filter((v: any) => v.impact === 'critical').length;
    const serious = violations.filter((v: any) => v.impact === 'serious').length;
    console.log('CRITICAL:' + critical + ' SERIOUS:' + serious);
  });
});
