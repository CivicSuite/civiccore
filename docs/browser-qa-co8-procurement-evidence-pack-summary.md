# Browser QA: CO-8 Procurement Evidence Pack Docs Link

Target: `docs/index.html` rendered from local file URL.

## States

- Loading: static document load completed with Playwright `wait_until=load`.
- Success: CO-8 procurement evidence pack link is visible and points at the evidence-pack index.
- Empty: not applicable for this static documentation page; no data-backed empty list exists.
- Error: no browser page errors or console errors observed.
- Partial: not applicable for this static documentation page; all visible sections render from local HTML.

## Results

### Desktop 1280x900

- Screenshot: `browser-qa-co8-procurement-evidence-pack-desktop.png`
- Title: `CivicCore v0.22.1 - CivicSuite shared platform library`
- CO-8 link visible: `True`
- CO-8 href: `https://github.com/CivicSuite/civiccore/blob/main/docs/evidence/co8-civiccore-procurement-evidence-pack/index.md`
- Horizontal overflow: `False` (`scrollWidth=1280`, `clientWidth=1280`)
- Console messages: `0`
- Page errors: `0`
- Body contrast ratio: `15.26`
- Link contrast ratio: `6.83`
- Keyboard focus sample: `PRE:pip install https://github.com/CivicSuite/civiccore/releases/download/v0.22.1/ci; A:CivicSuite Unified Spec; A:README; A:USER-MANUAL; A:CHANGELOG`

### Mobile 390x844

- Screenshot: `browser-qa-co8-procurement-evidence-pack-mobile.png`
- Title: `CivicCore v0.22.1 - CivicSuite shared platform library`
- CO-8 link visible: `True`
- CO-8 href: `https://github.com/CivicSuite/civiccore/blob/main/docs/evidence/co8-civiccore-procurement-evidence-pack/index.md`
- Horizontal overflow: `False` (`scrollWidth=390`, `clientWidth=390`)
- Console messages: `0`
- Page errors: `0`
- Body contrast ratio: `15.26`
- Link contrast ratio: `6.83`
- Keyboard focus sample: `PRE:pip install https://github.com/CivicSuite/civiccore/releases/download/v0.22.1/ci; PRE:git clone https://github.com/CivicSuite/civiccore.git
cd civiccore
pip install -; A:CivicSuite Unified Spec; A:README; A:USER-MANUAL`

## Verdict

PASS. The rendered docs link is visible on desktop and mobile, no console/page errors were observed, keyboard focus reaches the documentation links, contrast remains above WCAG AA thresholds for normal text, and no horizontal overflow was detected.
