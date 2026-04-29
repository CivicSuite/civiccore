# CivicCore v0.11.0 Browser QA

- Date: 2026-04-29
- Scope: updated `docs/index.html` after shipping the shared `civiccore.search` access-helper surface and promoting `v0.11.0` to the latest published release line.
- Desktop screenshot: `docs/browser-qa-civiccore-v0.11.0-docs-desktop.png`
- Mobile screenshot: `docs/browser-qa-civiccore-v0.11.0-docs-mobile.png`
- Visible checks: title/description show `v0.11.0`, install instructions point to the published `v0.11.0` wheel, search helpers mention permission-aware access checks, compatibility copy no longer claims `v0.10.0` is still pending.
- Console/result note: no page-level console issues surfaced during the browser pass; headless Edge emitted unrelated internal renderer task-provider stderr outside the page context.
