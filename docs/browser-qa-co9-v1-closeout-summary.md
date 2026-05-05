# Browser QA: CO-9 v1.0 Docs Surface

Target: `docs/index.html` rendered from local file URL.

## States

- Loading: static document load completed with Playwright `wait_until=load`.
- Success: v1.0 install copy, CO-8 evidence-pack link, and CO-9 closeout link are visible and correct.
- Empty: not applicable for this static documentation page; no data-backed empty list exists.
- Error: no browser page errors or console errors observed.
- Partial: not applicable for this static documentation page; all visible sections render from local HTML.

## Results

### Desktop 1280x900

- Screenshot: `browser-qa-co9-v1-closeout-desktop.png`
- Title: `CivicCore v1.0 - CivicSuite shared platform library`
- CO-8 link visible: `True`
- CO-8 href: `https://github.com/CivicSuite/civiccore/blob/main/docs/evidence/co8-civiccore-procurement-evidence-pack/index.md`
- CO-9 link visible: `True`
- CO-9 href: `https://github.com/CivicSuite/civiccore/blob/main/docs/ops/co-9-civiccore-v1-closeout.md`
- Horizontal overflow: `False` (`scrollWidth=1280`, `clientWidth=1280`)
- Console messages: `0`
- Page errors: `0`
- Body contrast ratio: `15.26`
- Link contrast ratio: `6.83`
- Keyboard focus sample: `PRE:pip install https://github.com/CivicSuite/civiccore/releases/download/v1.0/civiccore-1.0.0; A:CivicSuite Unified Spec; A:README; A:USER-MANUAL; A:CHANGELOG; A:Placeholder ADRs`
- Copy checks: title mentions v1.0=`True`, install uses v1.0 wheel=`True`, status names v1.0 productization=`True`, baseline still named=`True`, no stale staged copy=`True`

### Mobile 390x844

- Screenshot: `browser-qa-co9-v1-closeout-mobile.png`
- Title: `CivicCore v1.0 - CivicSuite shared platform library`
- CO-8 link visible: `True`
- CO-8 href: `https://github.com/CivicSuite/civiccore/blob/main/docs/evidence/co8-civiccore-procurement-evidence-pack/index.md`
- CO-9 link visible: `True`
- CO-9 href: `https://github.com/CivicSuite/civiccore/blob/main/docs/ops/co-9-civiccore-v1-closeout.md`
- Horizontal overflow: `False` (`scrollWidth=390`, `clientWidth=390`)
- Console messages: `0`
- Page errors: `0`
- Body contrast ratio: `15.26`
- Link contrast ratio: `6.83`
- Keyboard focus sample: `PRE:pip install https://github.com/CivicSuite/civiccore/releases/download/v1.0/civiccore-1.0.0; PRE:git clone https://github.com/CivicSuite/civiccore.git cd civiccore pip install -e .[dev]; A:CivicSuite Unified Spec; A:README; A:USER-MANUAL; A:CHANGELOG`
- Copy checks: title mentions v1.0=`True`, install uses v1.0 wheel=`True`, status names v1.0 productization=`True`, baseline still named=`True`, no stale staged copy=`True`

## Verdict

PASS. The v1.0 documentation surface renders on desktop and mobile, the release install copy and CO-8/CO-9 links are visible, console/page errors are clean, keyboard focus reaches documented links, contrast remains above WCAG AA thresholds for normal text, and no horizontal overflow was detected.
