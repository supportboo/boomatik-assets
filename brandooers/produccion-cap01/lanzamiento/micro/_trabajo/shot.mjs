// node shot.mjs <html> <out.png> <w> <h> [transparent]  — one headless Chrome, closed at the end; caller checks RAM first.
// Prints how many text blocks fall off the canvas (must be 0).
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
const { chromium } = createRequire('C:/Users/march/boo-manager/.claude/worktrees/social-growth/package.json')('playwright');
const [html, out, w, h, transparent] = process.argv.slice(2);
const browser = await chromium.launch({ channel: 'chrome' });
try {
  const page = await browser.newPage({ viewport: { width: +w, height: +h } });
  await page.goto(pathToFileURL(html).href, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const off = await page.evaluate(() => [...document.querySelectorAll('.blk,.cav,.lp,.ttl,.t')].filter((e) => {
    const b = e.getBoundingClientRect();
    return b.right > innerWidth + 1 || b.bottom > innerHeight + 1 || b.left < -1 || b.top < -1;
  }).length);
  await page.screenshot({ path: out, omitBackground: transparent === 'transparent' });
  console.log(JSON.stringify({ out, offCanvas: off }));
} finally {
  await browser.close();
}
