# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: visual.spec.ts >> Visual Regression Tests @visual >> TC-VIS-006 — Baseline dashboard Practice Expand apos login
- Location: visual.spec.ts:70:7

# Error details

```
Test timeout of 45000ms exceeded.
```

```
Error: locator.fill: Test timeout of 45000ms exceeded.
Call log:
  - waiting for getByPlaceholder(/email/i)

```

# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - paragraph [ref=e3]:
    - link "PMP Practice" [ref=e4] [cursor=pointer]:
      - /url: https://pmp.expandtesting.com/
    - text: "| Free PMP Certification Mock Exam Test +900 Questions & Quizzes"
    - link "Mock exam questions" [ref=e5] [cursor=pointer]:
      - img [ref=e7]
      - text: Mock exam questions
  - banner [ref=e10]:
    - navigation "Main navigation" [ref=e11]:
      - link "SUT" [ref=e12] [cursor=pointer]:
        - /url: /
        - 'img "Best Website for Practice Automation Testing: Free UI and REST API Examples and Apps. Using Cypress, Playwright, Selenium, WebdriverIO and Postman." [ref=e13]'
        - text: Practice
      - generic [ref=e14]:
        - list [ref=e15]:
          - listitem [ref=e16]:
            - button "Demos" [ref=e17] [cursor=pointer]
          - listitem [ref=e18]:
            - link "Tools" [ref=e19] [cursor=pointer]:
              - /url: /#tools
          - listitem [ref=e20]:
            - link "Tips" [ref=e21] [cursor=pointer]:
              - /url: /tips
          - listitem [ref=e22]:
            - link "Test Cases" [ref=e23] [cursor=pointer]:
              - /url: /test-cases
          - listitem [ref=e24]:
            - link "API Testing" [ref=e25] [cursor=pointer]:
              - /url: /notes/api/api-docs/
          - listitem [ref=e26]:
            - link "About" [ref=e27] [cursor=pointer]:
              - /url: /about
        - list
        - link "Free ISTQB Mock Exams" [ref=e28] [cursor=pointer]:
          - /url: https://istqb.expandtesting.com/
  - main [ref=e29]:
    - insertion [ref=e33]:
      - generic [ref=e36]:
        - heading "These are topics related to the article that might interest you" [level=2] [ref=e38]: Discover more
        - link "Social Networks" [ref=e39] [cursor=pointer]:
          - generic "Social Networks" [ref=e40]
          - img [ref=e42]
        - link "Development Tools" [ref=e44] [cursor=pointer]:
          - generic "Development Tools" [ref=e45]
          - img [ref=e47]
        - link "Email & Messaging" [ref=e49] [cursor=pointer]:
          - generic "Email & Messaging" [ref=e50]
          - img [ref=e52]
    - paragraph [ref=e55]:
      - text: Do you enjoy this platform? ❤️
      - link "Buy us a coffee" [ref=e56] [cursor=pointer]:
        - /url: https://www.buymeacoffee.com/expandtesting
    - generic [ref=e57]:
      - insertion [ref=e59]:
        - iframe [ref=e61]:
          - generic [active] [ref=f4e1]:
            - generic [ref=f4e5]:
              - link [ref=f4e6] [cursor=pointer]:
                - /url: https://adclick.g.doubleclick.net/aclk?sa=l&ai=CrL71vQ3-aeW9BKek4dUPsYn--AvTgfznhQHp0MuN-BS2kB8QASCVlJmjAWDNkOyArAOgAZiom6tAyAEJqQKf00b2j1KLPqgDAcgDywSqBKECT9BJKeRMRcyR641riySNWntdwOyrlawnRRYRHfbtr4HK1awMT-wePUmUOZUq0gDP-tT-ntGZ_ZxVcHRrWnBtkkgbofnqu3dlQnthOPot56X-U6a6-tTFSuTHGnqMvUA0v8cYLar-KXH_0oAZNWTtWpeersdkw_aUAdPMB_-qJEbQw0PaRzU944dNqlBnEyD9kyoATfmiXn-bODY4J9R4zdIdjYJcuTUHmZwvsFOnBb_9nORKZTxP11GC7WXFWLttEWAbuGayUzVgdT6HcfKPQg56hpN3xk6bQ2senrlrdIEqQm2CgC5Qs2gpOqCmbsn1pIGoe_hECSjBGFmpbHDMAeM8SHHS_Od-s-b6S2RybiQjQ5fbHcN4aDpLK_4BwI21LsAEtJf9ka4FiAXdt_iuVaAGLoAHmODrihuoB6fMsQKoB-LYsQKoB6a-G6gHzM6xAqgH89EbqAeW2BuoB6qbsQKoB47OG6gHk9gbqAfw4BuoB-6WsQKoB_6esQKoB6--sQKoB9XJG6gH2baxAqgHmgaoB_-esQKoB9-fsQKoB_jCsQKoB_vCsQLYBwDSCDEIgGEQARifAzIIioKAgICAgAg6D4BAgMCAgICAqIACqIOAEEi9_cE6WIj0iOmMqpQDsQknHizp1AheA4AKAZgLAcgLAYAMAaIMA5ABAaoNAkJSyA0B6g0TCKuYiemMqpQDFSdSuAQdsYQfv_ANAogOCbgT5APYEwOIFAXQFQGYFgHKFgIKAPgWAYAXAbIXEBgBKgoyNDA2MzM1NzQzUAa6FwI4AaoYFwkBAAAAgILPQBIKMjQwNjMzNTc0MxgBshgJEgKlahguIgEA0BgBwhkCCAE&ae=1&gclid=EAIaIQobChMIpZCJ6YyqlAMVJ1K4BB2xhB-_EAEYASAAEgKx_vD_BwE&num=1&cid=CAQShwIABaugfb4z4w4GKjoWdXGKWVPB1rVeIS39h719ravfa-dWdrijHa6JrYtgYNap9nd8o5lKiU2Z_DPNJFmYCG6U_dBow1BRXrRMx5I-Ns3kZ23tOn2z75rloTejXh-7ngVw0wTSVgjvq6EHjhdFKvNPsQGoRDGClHqYV2xIWbbJu3NSGqKOK7w4atMDaXhFk3C79blA3haOZFTVy9Vp46D9FbhVpZMx4ziNWTWjvUEAdyraUCpaSiSfZh8oCc4E4kvwoCVO6ir4w-KT6auRPf7jR6PFiRNkki4QEexD1GpKCzED8cAoV9Hb7bLUmu7Jy3rhJglrwfgWgBFHJRheQVrUMt6emfnlWxgB&sig=AOD64_0UiMxuBpRpCh4OoZ07-N9_afc6gA&client=ca-pub-1056034821646296&rf=1&nb=9&adurl=https://seiszero.com.br%3Futm_source%3DGoogleAds%26utm_medium%3Ddisplay%26utm_campaign%3DAmpla%26utm_content%3DFotos_Variadas%26utm_term%3D%26ad_id%3D770251932145%26gad_source%3D5%26gad_campaignid%3D22915455965%26gclid%3DEAIaIQobChMIpZCJ6YyqlAMVJ1K4BB2xhB-_EAEYASAAEgKx_vD_BwE
                - img [ref=f4e7]
              - generic [ref=f4e8]:
                - link "O lugar do tenista exigente" [ref=f4e10] [cursor=pointer]:
                  - /url: https://adclick.g.doubleclick.net/aclk?sa=l&ai=CrL71vQ3-aeW9BKek4dUPsYn--AvTgfznhQHp0MuN-BS2kB8QASCVlJmjAWDNkOyArAOgAZiom6tAyAEJqQKf00b2j1KLPqgDAcgDywSqBKECT9BJKeRMRcyR641riySNWntdwOyrlawnRRYRHfbtr4HK1awMT-wePUmUOZUq0gDP-tT-ntGZ_ZxVcHRrWnBtkkgbofnqu3dlQnthOPot56X-U6a6-tTFSuTHGnqMvUA0v8cYLar-KXH_0oAZNWTtWpeersdkw_aUAdPMB_-qJEbQw0PaRzU944dNqlBnEyD9kyoATfmiXn-bODY4J9R4zdIdjYJcuTUHmZwvsFOnBb_9nORKZTxP11GC7WXFWLttEWAbuGayUzVgdT6HcfKPQg56hpN3xk6bQ2senrlrdIEqQm2CgC5Qs2gpOqCmbsn1pIGoe_hECSjBGFmpbHDMAeM8SHHS_Od-s-b6S2RybiQjQ5fbHcN4aDpLK_4BwI21LsAEtJf9ka4FiAXdt_iuVaAGLoAHmODrihuoB6fMsQKoB-LYsQKoB6a-G6gHzM6xAqgH89EbqAeW2BuoB6qbsQKoB47OG6gHk9gbqAfw4BuoB-6WsQKoB_6esQKoB6--sQKoB9XJG6gH2baxAqgHmgaoB_-esQKoB9-fsQKoB_jCsQKoB_vCsQLYBwDSCDEIgGEQARifAzIIioKAgICAgAg6D4BAgMCAgICAqIACqIOAEEi9_cE6WIj0iOmMqpQDsQknHizp1AheA4AKAZgLAcgLAYAMAaIMA5ABAaoNAkJSyA0B6g0TCKuYiemMqpQDFSdSuAQdsYQfv_ANAogOCbgT5APYEwOIFAXQFQGYFgHKFgIKAPgWAYAXAbIXEBgBKgoyNDA2MzM1NzQzUAa6FwI4AaoYFwkBAAAAgILPQBIKMjQwNjMzNTc0MxgBshgJEgKlahguIgEA0BgBwhkCCAE&ae=1&gclid=EAIaIQobChMIpZCJ6YyqlAMVJ1K4BB2xhB-_EAEYASAAEgKx_vD_BwE&num=1&cid=CAQShwIABaugfb4z4w4GKjoWdXGKWVPB1rVeIS39h719ravfa-dWdrijHa6JrYtgYNap9nd8o5lKiU2Z_DPNJFmYCG6U_dBow1BRXrRMx5I-Ns3kZ23tOn2z75rloTejXh-7ngVw0wTSVgjvq6EHjhdFKvNPsQGoRDGClHqYV2xIWbbJu3NSGqKOK7w4atMDaXhFk3C79blA3haOZFTVy9Vp46D9FbhVpZMx4ziNWTWjvUEAdyraUCpaSiSfZh8oCc4E4kvwoCVO6ir4w-KT6auRPf7jR6PFiRNkki4QEexD1GpKCzED8cAoV9Hb7bLUmu7Jy3rhJglrwfgWgBFHJRheQVrUMt6emfnlWxgB&sig=AOD64_0UiMxuBpRpCh4OoZ07-N9_afc6gA&client=ca-pub-1056034821646296&rf=1&nb=0&adurl=https://seiszero.com.br%3Futm_source%3DGoogleAds%26utm_medium%3Ddisplay%26utm_campaign%3DAmpla%26utm_content%3DFotos_Variadas%26utm_term%3D%26ad_id%3D770251932145%26gad_source%3D5%26gad_campaignid%3D22915455965%26gclid%3DEAIaIQobChMIpZCJ6YyqlAMVJ1K4BB2xhB-_EAEYASAAEgKx_vD_BwE
                  - text: O lugar do
                  - text: tenista
                  - text: exigente
                - link [ref=f4e11] [cursor=pointer]:
                  - /url: https://adclick.g.doubleclick.net/aclk?sa=l&ai=CrL71vQ3-aeW9BKek4dUPsYn--AvTgfznhQHp0MuN-BS2kB8QASCVlJmjAWDNkOyArAOgAZiom6tAyAEJqQKf00b2j1KLPqgDAcgDywSqBKECT9BJKeRMRcyR641riySNWntdwOyrlawnRRYRHfbtr4HK1awMT-wePUmUOZUq0gDP-tT-ntGZ_ZxVcHRrWnBtkkgbofnqu3dlQnthOPot56X-U6a6-tTFSuTHGnqMvUA0v8cYLar-KXH_0oAZNWTtWpeersdkw_aUAdPMB_-qJEbQw0PaRzU944dNqlBnEyD9kyoATfmiXn-bODY4J9R4zdIdjYJcuTUHmZwvsFOnBb_9nORKZTxP11GC7WXFWLttEWAbuGayUzVgdT6HcfKPQg56hpN3xk6bQ2senrlrdIEqQm2CgC5Qs2gpOqCmbsn1pIGoe_hECSjBGFmpbHDMAeM8SHHS_Od-s-b6S2RybiQjQ5fbHcN4aDpLK_4BwI21LsAEtJf9ka4FiAXdt_iuVaAGLoAHmODrihuoB6fMsQKoB-LYsQKoB6a-G6gHzM6xAqgH89EbqAeW2BuoB6qbsQKoB47OG6gHk9gbqAfw4BuoB-6WsQKoB_6esQKoB6--sQKoB9XJG6gH2baxAqgHmgaoB_-esQKoB9-fsQKoB_jCsQKoB_vCsQLYBwDSCDEIgGEQARifAzIIioKAgICAgAg6D4BAgMCAgICAqIACqIOAEEi9_cE6WIj0iOmMqpQDsQknHizp1AheA4AKAZgLAcgLAYAMAaIMA5ABAaoNAkJSyA0B6g0TCKuYiemMqpQDFSdSuAQdsYQfv_ANAogOCbgT5APYEwOIFAXQFQGYFgHKFgIKAPgWAYAXAbIXEBgBKgoyNDA2MzM1NzQzUAa6FwI4AaoYFwkBAAAAgILPQBIKMjQwNjMzNTc0MxgBshgJEgKlahguIgEA0BgBwhkCCAE&ae=1&gclid=EAIaIQobChMIpZCJ6YyqlAMVJ1K4BB2xhB-_EAEYASAAEgKx_vD_BwE&num=1&cid=CAQShwIABaugfb4z4w4GKjoWdXGKWVPB1rVeIS39h719ravfa-dWdrijHa6JrYtgYNap9nd8o5lKiU2Z_DPNJFmYCG6U_dBow1BRXrRMx5I-Ns3kZ23tOn2z75rloTejXh-7ngVw0wTSVgjvq6EHjhdFKvNPsQGoRDGClHqYV2xIWbbJu3NSGqKOK7w4atMDaXhFk3C79blA3haOZFTVy9Vp46D9FbhVpZMx4ziNWTWjvUEAdyraUCpaSiSfZh8oCc4E4kvwoCVO6ir4w-KT6auRPf7jR6PFiRNkki4QEexD1GpKCzED8cAoV9Hb7bLUmu7Jy3rhJglrwfgWgBFHJRheQVrUMt6emfnlWxgB&sig=AOD64_0UiMxuBpRpCh4OoZ07-N9_afc6gA&client=ca-pub-1056034821646296&rf=1&nb=19&adurl=https://seiszero.com.br%3Futm_source%3DGoogleAds%26utm_medium%3Ddisplay%26utm_campaign%3DAmpla%26utm_content%3DFotos_Variadas%26utm_term%3D%26ad_id%3D770251932145%26gad_source%3D5%26gad_campaignid%3D22915455965%26gclid%3DEAIaIQobChMIpZCJ6YyqlAMVJ1K4BB2xhB-_EAEYASAAEgKx_vD_BwE
                  - img [ref=f4e12]
                - link "Para quem sabe o que quer e não se contenta com pouco, Seis Zero" [ref=f4e14] [cursor=pointer]:
                  - /url: https://adclick.g.doubleclick.net/aclk?sa=l&ai=CrL71vQ3-aeW9BKek4dUPsYn--AvTgfznhQHp0MuN-BS2kB8QASCVlJmjAWDNkOyArAOgAZiom6tAyAEJqQKf00b2j1KLPqgDAcgDywSqBKECT9BJKeRMRcyR641riySNWntdwOyrlawnRRYRHfbtr4HK1awMT-wePUmUOZUq0gDP-tT-ntGZ_ZxVcHRrWnBtkkgbofnqu3dlQnthOPot56X-U6a6-tTFSuTHGnqMvUA0v8cYLar-KXH_0oAZNWTtWpeersdkw_aUAdPMB_-qJEbQw0PaRzU944dNqlBnEyD9kyoATfmiXn-bODY4J9R4zdIdjYJcuTUHmZwvsFOnBb_9nORKZTxP11GC7WXFWLttEWAbuGayUzVgdT6HcfKPQg56hpN3xk6bQ2senrlrdIEqQm2CgC5Qs2gpOqCmbsn1pIGoe_hECSjBGFmpbHDMAeM8SHHS_Od-s-b6S2RybiQjQ5fbHcN4aDpLK_4BwI21LsAEtJf9ka4FiAXdt_iuVaAGLoAHmODrihuoB6fMsQKoB-LYsQKoB6a-G6gHzM6xAqgH89EbqAeW2BuoB6qbsQKoB47OG6gHk9gbqAfw4BuoB-6WsQKoB_6esQKoB6--sQKoB9XJG6gH2baxAqgHmgaoB_-esQKoB9-fsQKoB_jCsQKoB_vCsQLYBwDSCDEIgGEQARifAzIIioKAgICAgAg6D4BAgMCAgICAqIACqIOAEEi9_cE6WIj0iOmMqpQDsQknHizp1AheA4AKAZgLAcgLAYAMAaIMA5ABAaoNAkJSyA0B6g0TCKuYiemMqpQDFSdSuAQdsYQfv_ANAogOCbgT5APYEwOIFAXQFQGYFgHKFgIKAPgWAYAXAbIXEBgBKgoyNDA2MzM1NzQzUAa6FwI4AaoYFwkBAAAAgILPQBIKMjQwNjMzNTc0MxgBshgJEgKlahguIgEA0BgBwhkCCAE&ae=1&gclid=EAIaIQobChMIpZCJ6YyqlAMVJ1K4BB2xhB-_EAEYASAAEgKx_vD_BwE&num=1&cid=CAQShwIABaugfb4z4w4GKjoWdXGKWVPB1rVeIS39h719ravfa-dWdrijHa6JrYtgYNap9nd8o5lKiU2Z_DPNJFmYCG6U_dBow1BRXrRMx5I-Ns3kZ23tOn2z75rloTejXh-7ngVw0wTSVgjvq6EHjhdFKvNPsQGoRDGClHqYV2xIWbbJu3NSGqKOK7w4atMDaXhFk3C79blA3haOZFTVy9Vp46D9FbhVpZMx4ziNWTWjvUEAdyraUCpaSiSfZh8oCc4E4kvwoCVO6ir4w-KT6auRPf7jR6PFiRNkki4QEexD1GpKCzED8cAoV9Hb7bLUmu7Jy3rhJglrwfgWgBFHJRheQVrUMt6emfnlWxgB&sig=AOD64_0UiMxuBpRpCh4OoZ07-N9_afc6gA&client=ca-pub-1056034821646296&rf=1&nb=7&adurl=https://seiszero.com.br%3Futm_source%3DGoogleAds%26utm_medium%3Ddisplay%26utm_campaign%3DAmpla%26utm_content%3DFotos_Variadas%26utm_term%3D%26ad_id%3D770251932145%26gad_source%3D5%26gad_campaignid%3D22915455965%26gclid%3DEAIaIQobChMIpZCJ6YyqlAMVJ1K4BB2xhB-_EAEYASAAEgKx_vD_BwE
                  - text: Para quem sabe o
                  - text: que quer e não se
                  - text: contenta com pouco,
                  - text: Seis Zero
                - link [ref=f4e15] [cursor=pointer]:
                  - /url: https://adclick.g.doubleclick.net/aclk?sa=l&ai=CrL71vQ3-aeW9BKek4dUPsYn--AvTgfznhQHp0MuN-BS2kB8QASCVlJmjAWDNkOyArAOgAZiom6tAyAEJqQKf00b2j1KLPqgDAcgDywSqBKECT9BJKeRMRcyR641riySNWntdwOyrlawnRRYRHfbtr4HK1awMT-wePUmUOZUq0gDP-tT-ntGZ_ZxVcHRrWnBtkkgbofnqu3dlQnthOPot56X-U6a6-tTFSuTHGnqMvUA0v8cYLar-KXH_0oAZNWTtWpeersdkw_aUAdPMB_-qJEbQw0PaRzU944dNqlBnEyD9kyoATfmiXn-bODY4J9R4zdIdjYJcuTUHmZwvsFOnBb_9nORKZTxP11GC7WXFWLttEWAbuGayUzVgdT6HcfKPQg56hpN3xk6bQ2senrlrdIEqQm2CgC5Qs2gpOqCmbsn1pIGoe_hECSjBGFmpbHDMAeM8SHHS_Od-s-b6S2RybiQjQ5fbHcN4aDpLK_4BwI21LsAEtJf9ka4FiAXdt_iuVaAGLoAHmODrihuoB6fMsQKoB-LYsQKoB6a-G6gHzM6xAqgH89EbqAeW2BuoB6qbsQKoB47OG6gHk9gbqAfw4BuoB-6WsQKoB_6esQKoB6--sQKoB9XJG6gH2baxAqgHmgaoB_-esQKoB9-fsQKoB_jCsQKoB_vCsQLYBwDSCDEIgGEQARifAzIIioKAgICAgAg6D4BAgMCAgICAqIACqIOAEEi9_cE6WIj0iOmMqpQDsQknHizp1AheA4AKAZgLAcgLAYAMAaIMA5ABAaoNAkJSyA0B6g0TCKuYiemMqpQDFSdSuAQdsYQfv_ANAogOCbgT5APYEwOIFAXQFQGYFgHKFgIKAPgWAYAXAbIXEBgBKgoyNDA2MzM1NzQzUAa6FwI4AaoYFwkBAAAAgILPQBIKMjQwNjMzNTc0MxgBshgJEgKlahguIgEA0BgBwhkCCAE&ae=1&gclid=EAIaIQobChMIpZCJ6YyqlAMVJ1K4BB2xhB-_EAEYASAAEgKx_vD_BwE&num=1&cid=CAQShwIABaugfb4z4w4GKjoWdXGKWVPB1rVeIS39h719ravfa-dWdrijHa6JrYtgYNap9nd8o5lKiU2Z_DPNJFmYCG6U_dBow1BRXrRMx5I-Ns3kZ23tOn2z75rloTejXh-7ngVw0wTSVgjvq6EHjhdFKvNPsQGoRDGClHqYV2xIWbbJu3NSGqKOK7w4atMDaXhFk3C79blA3haOZFTVy9Vp46D9FbhVpZMx4ziNWTWjvUEAdyraUCpaSiSfZh8oCc4E4kvwoCVO6ir4w-KT6auRPf7jR6PFiRNkki4QEexD1GpKCzED8cAoV9Hb7bLUmu7Jy3rhJglrwfgWgBFHJRheQVrUMt6emfnlWxgB&sig=AOD64_0UiMxuBpRpCh4OoZ07-N9_afc6gA&client=ca-pub-1056034821646296&rf=1&nb=8&adurl=https://seiszero.com.br%3Futm_source%3DGoogleAds%26utm_medium%3Ddisplay%26utm_campaign%3DAmpla%26utm_content%3DFotos_Variadas%26utm_term%3D%26ad_id%3D770251932145%26gad_source%3D5%26gad_campaignid%3D22915455965%26gclid%3DEAIaIQobChMIpZCJ6YyqlAMVJ1K4BB2xhB-_EAEYASAAEgKx_vD_BwE
                  - img [ref=f4e17]
            - img [ref=f4e22] [cursor=pointer]
            - button [ref=f4e24] [cursor=pointer]:
              - img [ref=f4e25]
            - iframe
      - generic [ref=e64]:
        - navigation "breadcrumb mb-2" [ref=e65]:
          - list [ref=e66]:
            - listitem [ref=e67]:
              - link "Practice" [ref=e68] [cursor=pointer]:
                - /url: /
            - listitem [ref=e69]:
              - text: /
              - link "Home - My Notes - The App for Automation Testing Practice" [ref=e70] [cursor=pointer]:
                - /url: /notes/app/
        - generic [ref=e76]:
          - heading "Login" [level=1] [ref=e77]
          - generic [ref=e78]:
            - generic [ref=e79]:
              - generic [ref=e80]:
                - generic [ref=e81]: Email address
                - textbox "Email address" [ref=e82]
              - generic [ref=e83]:
                - generic [ref=e84]: Password
                - link "Forgot password" [ref=e85] [cursor=pointer]:
                  - /url: /notes/app/forgot-password
                - textbox "Password" [ref=e86]
            - button "Login" [ref=e88] [cursor=pointer]
          - generic [ref=e89]:
            - link "Login with Google" [ref=e90] [cursor=pointer]:
              - /url: https://practice.expandtesting.com/notes/app/auth/google
            - link "Login with LinkedIn" [ref=e91] [cursor=pointer]:
              - /url: https://practice.expandtesting.com/notes/app/auth/linkedin
            - link "Software" [ref=e92] [cursor=pointer]:
              - img [ref=e94]
              - text: Software
          - generic [ref=e96]:
            - text: Don't have an account?
            - link "Create a free account!" [ref=e97] [cursor=pointer]:
              - /url: /notes/app/register
  - contentinfo [ref=e98]:
    - generic [ref=e103]:
      - heading "Practice Test Automation WebSite for Web UI and Rest API" [level=4] [ref=e104]
      - paragraph [ref=e105]:
        - text: "Version: e64cd80e | Copyright"
        - link "Expand Testing" [ref=e106] [cursor=pointer]:
          - /url: https://expandtesting.com/
        - text: "2026"
  - img [ref=e108] [cursor=pointer]
  - generic [ref=e110]:
    - generic [ref=e111] [cursor=pointer]:
      - img [ref=e113]
      - link "Go to shopping options for Development Tools" [ref=e115]: Development Tools
    - button "Close shopping anchor" [ref=e116]
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | import * as fs from 'fs';
  3  | import * as path from 'path';
  4  | 
  5  | const baselineDir = path.join(__dirname, 'baselines');
  6  | fs.mkdirSync(baselineDir, { recursive: true });
  7  | 
  8  | test.describe('Visual Regression Tests @visual', () => {
  9  | 
  10 |   test('TC-VIS-001 — Baseline homepage AutomationExercise', async ({ page }) => {
  11 |     await page.goto('https://automationexercise.com', { waitUntil: 'domcontentloaded' });
  12 |     await page.waitForTimeout(1500);
  13 |     // Ocultar elementos dinamicos (banners, timers)
  14 |     await page.evaluate(() => {
  15 |       document.querySelectorAll('[id*="timer"], [class*="countdown"], [class*="timer"]').forEach((el: any) => {
  16 |         el.style.visibility = 'hidden';
  17 |       });
  18 |     });
  19 |     await expect(page).toHaveScreenshot('automationexercise_home_baseline.png', {
  20 |       maxDiffPixelRatio: 0.02,
  21 |       animations: 'disabled',
  22 |       fullPage: true,
  23 |     });
  24 |   });
  25 | 
  26 |   test('TC-VIS-002 — Baseline pagina de produtos AutomationExercise', async ({ page }) => {
  27 |     await page.goto('https://automationexercise.com/products', { waitUntil: 'domcontentloaded' });
  28 |     await page.waitForTimeout(1000);
  29 |     await expect(page).toHaveScreenshot('automationexercise_products_baseline.png', {
  30 |       maxDiffPixelRatio: 0.02,
  31 |       animations: 'disabled',
  32 |       fullPage: true,
  33 |     });
  34 |   });
  35 | 
  36 |   test('TC-VIS-003 — Comparacao visual homepage dentro do threshold', async ({ page }) => {
  37 |     await page.goto('https://automationexercise.com', { waitUntil: 'domcontentloaded' });
  38 |     await page.waitForTimeout(1500);
  39 |     await page.evaluate(() => {
  40 |       document.querySelectorAll('[id*="timer"], [class*="countdown"], [class*="timer"]').forEach((el: any) => {
  41 |         el.style.visibility = 'hidden';
  42 |       });
  43 |     });
  44 |     await expect(page).toHaveScreenshot('automationexercise_home_baseline.png', {
  45 |       maxDiffPixelRatio: 0.02,
  46 |       animations: 'disabled',
  47 |       fullPage: true,
  48 |     });
  49 |   });
  50 | 
  51 |   test('TC-VIS-004 — Comparacao visual produtos (pode ter regressao)', async ({ page }) => {
  52 |     await page.goto('https://automationexercise.com/products', { waitUntil: 'domcontentloaded' });
  53 |     await page.waitForTimeout(1000);
  54 |     await expect(page).toHaveScreenshot('automationexercise_products_baseline.png', {
  55 |       maxDiffPixelRatio: 0.02,
  56 |       animations: 'disabled',
  57 |       fullPage: true,
  58 |     });
  59 |   });
  60 | 
  61 |   test('TC-VIS-005 — Baseline pagina de login Practice Expand', async ({ page }) => {
  62 |     await page.goto('https://practice.expandtesting.com/notes/app/login', { waitUntil: 'domcontentloaded' });
  63 |     await page.waitForTimeout(1000);
  64 |     await expect(page).toHaveScreenshot('expandtesting_login_baseline.png', {
  65 |       maxDiffPixelRatio: 0.02,
  66 |       animations: 'disabled',
  67 |     });
  68 |   });
  69 | 
  70 |   test('TC-VIS-006 — Baseline dashboard Practice Expand apos login', async ({ page }) => {
  71 |     await page.goto('https://practice.expandtesting.com/notes/app/login', { waitUntil: 'domcontentloaded' });
> 72 |     await page.getByPlaceholder(/email/i).fill('qa_agente_v3@test.com');
     |                                           ^ Error: locator.fill: Test timeout of 45000ms exceeded.
  73 |     await page.getByPlaceholder(/password/i).fill('Test@1234');
  74 |     await page.getByRole('button', { name: /login/i }).click();
  75 |     await page.waitForLoadState('domcontentloaded');
  76 |     await page.waitForTimeout(2000);
  77 |     await expect(page).toHaveScreenshot('expandtesting_dashboard_baseline.png', {
  78 |       maxDiffPixelRatio: 0.03,
  79 |       animations: 'disabled',
  80 |     });
  81 |   });
  82 | 
  83 | });
  84 | 
```