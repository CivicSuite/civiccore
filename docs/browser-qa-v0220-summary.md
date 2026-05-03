# Browser QA - CivicCore v0.22.0

Date: 2026-05-03

Scope:
- Rendered `docs/index.html` after adding the shared sync source status projection release language.
- Confirmed the landing page source references `v0.22.0`, the v0.22.0 GitHub release wheel path, `SyncSourceStatus`, and `build_sync_source_status`.
- Captured desktop and mobile evidence with Chrome headless.

Evidence:
- Desktop screenshot: `docs/screenshots/browser-qa-v0220-desktop.png`
- Mobile screenshot: `docs/screenshots/browser-qa-v0220-mobile.png`

Viewport checks:
- Desktop: `1440x1100`
- Mobile: `390x1200`

Console/page-error check:
- `docs/index.html` has no page script execution path; Chrome headless produced screenshots without JavaScript page errors.
