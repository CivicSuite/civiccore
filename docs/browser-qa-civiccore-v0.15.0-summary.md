# CivicCore v0.15.0 Browser QA

- Date: 2026-04-29
- Scope: updated `docs/index.html` after shipping the trusted-proxy helper release and promoting `v0.15.0` as the current development-line target.
- Desktop screenshot: `docs/browser-qa-civiccore-v0.15.0-docs-desktop.png`
- Mobile screenshot: `docs/browser-qa-civiccore-v0.15.0-docs-mobile.png`
- Visible checks: title and release copy show `v0.15.0`, the install instructions point to the `v0.15.0` wheel path, and the docs now describe the trusted-proxy helper export for downstream staff-auth consumers.
- Console/result note: no page-level docs-console errors were reported by the in-app browser check; Edge headless emitted only the known renderer fallback-task noise while still writing both screenshots successfully.
