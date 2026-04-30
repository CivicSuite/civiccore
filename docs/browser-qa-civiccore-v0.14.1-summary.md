# CivicCore v0.14.1 Browser QA

- Date: 2026-04-29
- Scope: updated `docs/index.html` after shipping the trusted-header auth patch release and promoting `v0.14.1` as the current development-line target.
- Desktop screenshot: `docs/browser-qa-civiccore-v0.14.1-docs-desktop.png`
- Mobile screenshot: `docs/browser-qa-civiccore-v0.14.1-docs-mobile.png`
- Visible checks: title and release copy show `v0.14.1`, the install instructions point to the `v0.14.1` wheel path, and the compatibility copy now points consumers at the `v0.14.1` release line.
- Console/result note: no page-level docs-console errors were reported by the browser QA gate; Edge headless emitted only the known renderer fallback-task noise while still writing both screenshots successfully.
