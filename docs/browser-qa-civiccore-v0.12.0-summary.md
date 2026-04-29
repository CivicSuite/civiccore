# CivicCore v0.12.0 Browser QA

- Date: 2026-04-29
- Scope: updated `docs/index.html` after shipping the shared `civiccore.security` connector-host validation and encrypted-config helper surface and promoting `v0.12.0` to the current development-line release target.
- Desktop screenshot: `docs/browser-qa-civiccore-v0.12.0-docs-desktop.png`
- Mobile screenshot: `docs/browser-qa-civiccore-v0.12.0-docs-mobile.png`
- Visible checks: title/description show `v0.12.0`, install instructions point to the `v0.12.0` wheel path, status copy mentions the shared `civiccore.security` surface, and compatibility copy no longer claims `v0.11.0` is the current consumer target.
- Console/result note: no page-level console issues surfaced during the browser pass; headless Edge emitted unrelated internal renderer task-provider stderr outside the page context.
