# Browser QA - CivicCore v0.21.0

Date: 2026-05-02

Scope:
- Rendered `docs/index.html` after adding the shared scheduling helper release language.
- Confirmed the landing page source references `v0.21.0`, the v0.21.0 GitHub release wheel path, and `civiccore.scheduling` cron helper scope.
- Captured desktop and mobile evidence with Playwright Chromium.

Evidence:
- Desktop screenshot: `docs/screenshots/browser-qa-v0210-desktop.png`
- Mobile screenshot: `docs/screenshots/browser-qa-v0210-mobile.png`

Viewport checks:
- Desktop: `1440x1100`
- Mobile: `390x1200`

Console/page-error check:
- `docs/index.html` rendered with zero browser console errors and zero page errors.
