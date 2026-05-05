# CO-6 Cleanroom Harness Browser QA Evidence

Date: 2026-05-05

Scope: `docs/index.html` rendered after adding the CO-6 cleanroom harness documentation link.

## Viewports

- Desktop: 1280 x 900, screenshot `docs/browser-qa-co6-cleanroom-harness-desktop.png`
- Mobile: 390 x 844, screenshot `docs/browser-qa-co6-cleanroom-harness-mobile.png`

## Rendered States

- Success state: checked on desktop and mobile.
- Loading state: not applicable; static HTML has no async loading state.
- Empty state: not applicable; static documentation page has no user data collection.
- Error state: not applicable; static file render has no runtime fetch/error branch.
- Partial state: not applicable; static page has no partial-data branch.

## Results

- Page title: `CivicCore v0.22.1 - CivicSuite shared platform library`
- Main heading: `CivicCore`
- Cleanroom harness link visible: true
- Cleanroom copy visible: true
- v0.22.1 baseline copy visible: true
- Browser console messages: 0
- Page errors: 0
- Horizontal overflow: false
- Body contrast ratio: 15.26
- Link contrast ratio: 6.83
- Keyboard focus sample after tabbing: Desktop: pre pip install https://github.com/CivicSuite/civiccore/releases/download/v0.22.1/civiccor -> a CivicSuite Unified Spec -> a README -> a USER-MANUAL -> a CHANGELOG -> a Cleanroom harness -> a Historical provenance policy -> a Tier 1 retrofit ledger -> a CO-4 cross-module retrofit report; Mobile: pre pip install https://github.com/CivicSuite/civiccore/releases/download/v0.22.1/civiccor -> pre git clone https://github.com/CivicSuite/civiccore.git cd civiccore pip install -e .[de -> a CivicSuite Unified Spec -> a README -> a USER-MANUAL -> a CHANGELOG -> a Cleanroom harness -> a Historical provenance policy -> a Tier 1 retrofit ledger
- Empty image alt count: 0
- Copy review: the cleanroom harness link names the artifact, states the verification paths, and does not imply a public release was cut.

## Result

PASS

## Browser Automation Command

The check used bundled Playwright via the workspace Node runtime and opened:

```text
file:///C:/Users/scott/OneDrive/Desktop/Claude/civiccore/docs/index.html
```
