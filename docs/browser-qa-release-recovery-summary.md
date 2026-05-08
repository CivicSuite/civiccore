# CivicCore Release Recovery Browser QA

Date: 2026-05-07
Surface: `docs/index.html`
Tool: Playwright Chromium through Codex Node REPL

## Desktop

- Viewport: 1366 x 900
- Screenshot: `docs/browser-qa-release-recovery-desktop.png`
- Title: `CivicCore v1.0 - CivicSuite shared platform library (provisional)`
- Provisional/recovery copy visible: yes
- Install command visible: yes
- Not-end-user-app copy visible: yes
- Console messages: none
- Page errors: none
- Horizontal overflow: no
- Keyboard focus sample:
  - install command block
  - CivicSuite Unified Spec
  - README
  - USER-MANUAL
  - CHANGELOG
  - Placeholder ADRs
  - CO-8 procurement evidence pack
  - CO-9 closeout report

## Mobile

- Viewport: 390 x 844
- Screenshot: `docs/browser-qa-release-recovery-mobile.png`
- Title: `CivicCore v1.0 - CivicSuite shared platform library (provisional)`
- Provisional/recovery copy visible: yes
- Install command visible: yes
- Not-end-user-app copy visible: yes
- Console messages: none
- Page errors: none
- Horizontal overflow: no
- Keyboard focus sample:
  - install command block
  - clone/development install block
  - CivicSuite Unified Spec
  - README
  - USER-MANUAL
  - CHANGELOG
  - Placeholder ADRs
  - CO-8 procurement evidence pack

## Verdict

PASS. The changed docs landing page now renders the provisional release posture
clearly on desktop and mobile, without console/page errors or layout overflow.
