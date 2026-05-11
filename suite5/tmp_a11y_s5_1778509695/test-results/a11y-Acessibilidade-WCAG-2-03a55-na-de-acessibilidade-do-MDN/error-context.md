# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: a11y.spec.ts >> Acessibilidade WCAG 2.1 AA Suite 5 >> TC-A11Y-S5-002 - Conformidade WCAG 2.1 AA na pagina de acessibilidade do MDN
- Location: a11y.spec.ts:110:7

# Error details

```
Error: 2 violacao(oes) serious encontrada(s)
```

# Test source

```ts
  60  |     logs.push(`[NAV] Acessando ${url}`);
  61  |     await page.goto(url);
  62  |     await page.waitForLoadState('domcontentloaded');
  63  |     await page.waitForSelector('main', { timeout: 20_000 });
  64  |     logs.push('[ANALYSIS] Executando axe-core (WCAG 2.1 AA)');
  65  | 
  66  |     const axeResults = await new AxeBuilder({ page })
  67  |       .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
  68  |       .analyze();
  69  | 
  70  |     const violations = axeResults.violations.map(v => ({
  71  |       rule_id: v.id,
  72  |       impact: v.impact,
  73  |       description: v.description,
  74  |       affected_elements: v.nodes.slice(0, 3).map(n => n.target[0] || '?'),
  75  |       how_to_fix: v.help,
  76  |       help_url: v.helpUrl,
  77  |       known_environment_failure: false,
  78  |       known_failure_note: null
  79  |     }));
  80  | 
  81  |     const critical = violations.filter(v => v.impact === 'critical').length;
  82  |     const serious = violations.filter(v => v.impact === 'serious').length;
  83  |     const moderate = violations.filter(v => v.impact === 'moderate').length;
  84  |     const minor = violations.filter(v => v.impact === 'minor').length;
  85  | 
  86  |     for (const v of violations) {
  87  |       logs.push(`[VIOLATION] ${v.rule_id} (${v.impact}): ${v.affected_elements.length} elemento(s)`);
  88  |     }
  89  | 
  90  |     const status = (critical > 0 || serious > 0) ? 'failed' : (moderate > 0 || minor > 0 ? 'warning' : 'passed');
  91  |     const deploy_blocked = critical > 0 || serious > 0;
  92  |     logs.push(`[RESULT] ${violations.length} violacoes encontradas — ${status}${deploy_blocked ? '; deploy bloqueado' : ''}`);
  93  | 
  94  |     results.push({
  95  |       id: 'TC-A11Y-S5-001',
  96  |       title: 'Conformidade WCAG 2.1 AA na pagina de padroes WCAG do W3C',
  97  |       status,
  98  |       deploy_blocked,
  99  |       violations,
  100 |       passes_count: axeResults.passes.length,
  101 |       logs,
  102 |       error: null
  103 |     });
  104 | 
  105 |     // Assertions
  106 |     if (critical > 0) throw new Error(`${critical} violacao(oes) critica(s) encontrada(s)`);
  107 |     if (serious > 0) throw new Error(`${serious} violacao(oes) serious encontrada(s)`);
  108 |   });
  109 | 
  110 |   test('TC-A11Y-S5-002 - Conformidade WCAG 2.1 AA na pagina de acessibilidade do MDN', async ({ page }) => {
  111 |     const logs: string[] = [];
  112 |     const url = 'https://developer.mozilla.org/en-US/docs/Web/Accessibility';
  113 | 
  114 |     logs.push(`[NAV] Acessando ${url}`);
  115 |     await page.goto(url);
  116 |     await page.waitForLoadState('domcontentloaded');
  117 |     await page.waitForSelector('main', { timeout: 20_000 });
  118 |     logs.push('[ANALYSIS] Executando axe-core (WCAG 2.1 AA)');
  119 | 
  120 |     const axeResults = await new AxeBuilder({ page })
  121 |       .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
  122 |       .analyze();
  123 | 
  124 |     const violations = axeResults.violations.map(v => ({
  125 |       rule_id: v.id,
  126 |       impact: v.impact,
  127 |       description: v.description,
  128 |       affected_elements: v.nodes.slice(0, 3).map(n => n.target[0] || '?'),
  129 |       how_to_fix: v.help,
  130 |       help_url: v.helpUrl,
  131 |       known_environment_failure: false,
  132 |       known_failure_note: null
  133 |     }));
  134 | 
  135 |     const critical = violations.filter(v => v.impact === 'critical').length;
  136 |     const serious = violations.filter(v => v.impact === 'serious').length;
  137 |     const moderate = violations.filter(v => v.impact === 'moderate').length;
  138 |     const minor = violations.filter(v => v.impact === 'minor').length;
  139 | 
  140 |     for (const v of violations) {
  141 |       logs.push(`[VIOLATION] ${v.rule_id} (${v.impact}): ${v.affected_elements.length} elemento(s)`);
  142 |     }
  143 | 
  144 |     const status = (critical > 0 || serious > 0) ? 'failed' : (moderate > 0 || minor > 0 ? 'warning' : 'passed');
  145 |     const deploy_blocked = critical > 0 || serious > 0;
  146 |     logs.push(`[RESULT] ${violations.length} violacoes encontradas — ${status}${deploy_blocked ? '; deploy bloqueado' : ''}`);
  147 | 
  148 |     results.push({
  149 |       id: 'TC-A11Y-S5-002',
  150 |       title: 'Conformidade WCAG 2.1 AA na pagina de acessibilidade do MDN',
  151 |       status,
  152 |       deploy_blocked,
  153 |       violations,
  154 |       passes_count: axeResults.passes.length,
  155 |       logs,
  156 |       error: null
  157 |     });
  158 | 
  159 |     if (critical > 0) throw new Error(`${critical} violacao(oes) critica(s) encontrada(s)`);
> 160 |     if (serious > 0) throw new Error(`${serious} violacao(oes) serious encontrada(s)`);
      |                            ^ Error: 2 violacao(oes) serious encontrada(s)
  161 |   });
  162 | 
  163 | });
  164 | 
```