# Browser QA - CivicCore v0.20.0

Date: 2026-05-02

Scope:
- Rendered `docs/index.html` after adding the shared startup config validation release language.
- Confirmed the landing page source references `v0.20.0`, the v0.20.0 GitHub release wheel path, and startup config validation helpers.
- Captured desktop and mobile evidence with Chrome headless.

Evidence:
- Desktop screenshot: `docs/screenshots/browser-qa-v0200-desktop.png`
- Mobile screenshot: `docs/screenshots/browser-qa-v0200-mobile.png`

Viewport checks:
- Desktop: `1440x1100`
- Mobile: `390x1200`

Console/page-error check:
- `docs/index.html` has no page script execution path; Chrome headless produced screenshots without JavaScript page errors.
