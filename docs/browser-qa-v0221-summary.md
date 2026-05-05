# CivicCore v0.22.1 Browser QA Evidence

Date: 2026-05-05

Scope: `docs/index.html` rendered from the `release/v0.22.1-attested-baseline-staging` branch.

## Viewports

- Desktop: 1280 x 900, screenshot `docs/browser-qa-v0221-desktop.png`
- Mobile: 390 x 844, screenshot `docs/browser-qa-v0221-mobile.png`

## Results

- Page title: `CivicCore v0.22.1 - CivicSuite shared platform library`
- Main heading: `CivicCore`
- Status copy includes `v0.22.1 is staged as the first attested baseline release`
- Install copy includes the `v0.22.1` GitHub wheel URL
- Browser console messages: none
- Page errors: none
- Horizontal overflow: false on desktop and mobile
- Body contrast ratio: 15.26
- Link contrast ratio: 6.83
- Keyboard tab order reaches all documented links
- Empty image alt count: 0

## Browser Automation Command

The check used bundled Playwright via the workspace Node runtime and opened:

```text
file:///C:/Users/scott/OneDrive/Desktop/Claude/civiccore/docs/index.html
```
