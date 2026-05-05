# CivicCore CO-3 Browser QA Evidence

Date: 2026-05-05

Scope: `docs/index.html` rendered from branch `docs/co-3-tier1-retrofit-ledger`
after the CO-3 Tier 1 retrofit ledger and post-publication release-copy updates.

## Viewports

- Desktop: 1280 x 900, screenshot
  `docs/browser-qa-co3-tier1-ledger-desktop.png`
- Mobile: 390 x 844, screenshot
  `docs/browser-qa-co3-tier1-ledger-mobile.png`

## Rendered States

- Success state: checked on desktop and mobile.
- Loading state: not applicable; `docs/index.html` is a static file with no
  asynchronous loading path.
- Empty state: not applicable; static documentation page has no data-backed
  empty condition.
- Error state: not applicable; static documentation page has no user-triggered
  error condition.
- Partial/degraded state: not applicable; page has no runtime service or
  progressive data dependency.

## Results

- Page title: `CivicCore v0.22.1 - CivicSuite shared platform library`
- Main heading: `CivicCore`
- Status copy includes `v0.22.1 is the first attested baseline release`
- Install copy includes the `v0.22.1` GitHub wheel URL
- Documentation links include the Tier 1 retrofit ledger
- Stale staged-release copy: not present
- Browser console messages: none
- Page errors: none
- Horizontal overflow: false on desktop and mobile
- Body contrast ratio: 15.26
- Link contrast ratio: 6.83
- Keyboard navigation: Tab traversal reaches both command blocks and all
  documented links with visible focus outlines
- Empty image alt count: 0

## Browser Automation Command

The check used bundled Playwright via the workspace Node runtime and opened:

```text
file:///C:/Users/scott/OneDrive/Desktop/Claude/civiccore/docs/index.html
```
