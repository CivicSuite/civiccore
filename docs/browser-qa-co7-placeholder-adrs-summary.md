# CO-7 Placeholder ADRs Browser QA Evidence

Date: 2026-05-05

Scope: `docs/index.html` rendered after CO-7 CivicCore freeze/spec-lockstep documentation updates.

## Viewports

- Desktop: 1280 x 900, screenshot `docs/browser-qa-co7-placeholder-adrs-desktop.png`
- Mobile: 390 x 844, screenshot `docs/browser-qa-co7-placeholder-adrs-mobile.png`

## Rendered States

- Success state: checked on desktop and mobile.
- Loading state: not applicable; static HTML has no async loading state.
- Empty state: not applicable; static documentation page has no user data collection.
- Error state: not applicable; static file render has no runtime fetch/error branch.
- Partial state: not applicable; static page has no partial-data branch.

## Results

- Page title: `CivicCore v0.22.1 - CivicSuite shared platform library`
- Page title matches expected: true
- Main heading: `CivicCore`
- Placeholder ADRs link visible: true
- Downstream rule copy visible: true
- Catalog placeholder visible: true
- Browser console messages: desktop 0, mobile 0
- Page errors: desktop 0, mobile 0
- Horizontal overflow: desktop false, mobile false
- Body contrast ratio: desktop 15.26, mobile 15.26
- Link contrast ratio: desktop 6.83, mobile 6.83
- Keyboard focus sample after tabbing: Desktop: pre pip install https://github.com/CivicSuite/civiccore/releases/download/v0.22.1/civiccore-0.22.1-py3-none-any.whl -> a CivicSuite Unified Spec -> a README -> a USER-MANUAL -> a CHANGELOG -> a Placeholder ADRs -> a Cleanroom harness -> a Historical provenance policy -> a Tier 1 retrofit ledger -> a CO-4 cross-module retrofit report; Mobile: pre pip install https://github.com/CivicSuite/civiccore/releases/download/v0.22.1/civiccore-0.22.1-py3-none-any.whl -> pre git clone https://github.com/CivicSuite/civiccore.git cd civiccore pip install -e .[dev] -> a CivicSuite Unified Spec -> a README -> a USER-MANUAL -> a CHANGELOG -> a Placeholder ADRs -> a Cleanroom harness -> a Historical provenance policy -> a Tier 1 retrofit ledger
- Empty image alt count: desktop 0, mobile 0
- Copy review: the placeholder ADR copy names the reserved namespaces, states the downstream no-dependency rule, and does not imply the placeholders are shipped APIs.

## Result

PASS

## Browser Automation Command

The check used Python Playwright from this workspace and opened:

```text
file:///C:/Users/scott/OneDrive/Desktop/Claude/civiccore/docs/index.html
```
