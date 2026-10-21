'use strict';

// Run with Node.js and Playwright. Uses isolated browser profiles and local media.
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const assert = require('node:assert/strict');
const project = path.resolve(__dirname, '..');
const fixture = fs.readFileSync(path.join(__dirname, 'fixture.html'));
const script = fs.readFileSync(path.join(project, 'bilibili-ambient-glass.user.js'));
let media = Buffer.alloc(0);
const channels = process.argv.slice(2).length ? process.argv.slice(2) : ['msedge', 'chrome'];
const results = [];
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function createServer() {
  return http.createServer((req, res) => {
    if (req.url === '/bilibili-ambient-glass.user.js') {
      res.writeHead(200, { 'Content-Type': 'text/javascript; charset=utf-8' });res.end(script);
    } else if (req.url === '/sample.webm') {
      res.writeHead(200, { 'Content-Type': 'video/webm' });res.end(media);
    } else if (req.url === '/favicon.ico') { res.writeHead(204);res.end(); }
    else { res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });res.end(fixture); }
  });
}
async function listen(server) {
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  return `http://127.0.0.1:${server.address().port}`;
}
async function check(name, test) {
  await test();results.push(name);console.log(`PASS ${name}`);
}
const count = (page) => page.evaluate(() => window.__ambientTest.draws);
const active = (page) => page.locator('html').getAttribute('data-btfer-active');
async function expectDrawing(page) {
  const before = await count(page);
  await page.waitForFunction((previous) => window.__ambientTest.draws > previous + 1, before);
}
async function expectStopped(page) {
  await sleep(180);
  const before = await count(page);
  await sleep(450);
  assert.equal(await count(page), before);
}

function installInstrumentation() {
  const draw = CanvasRenderingContext2D.prototype.drawImage;
  const read = CanvasRenderingContext2D.prototype.getImageData;
  window.__ambientTest = { draws: 0, fail: false, reads: 0, warnings: [] };
  const isAmbient = (canvas) => canvas.parentElement?.id === 'btfer-ambient-backdrop';
  CanvasRenderingContext2D.prototype.drawImage = function (...args) {
    if (isAmbient(this.canvas)) {
      window.__ambientTest.draws++;
      if (window.__ambientTest.fail) throw new DOMException('Test: protected media', 'SecurityError');
    }
    return draw.apply(this, args);
  };
  CanvasRenderingContext2D.prototype.getImageData = function (...args) {
    if (isAmbient(this.canvas)) { window.__ambientTest.reads++;throw new Error('Production pixel readback is forbidden in this test'); }
    return read.apply(this, args);
  };
  window.__ambientSample = () => {
    const canvas = document.querySelector('#btfer-ambient-backdrop canvas');
    return Array.from(read.call(canvas.getContext('2d'), 12, 12, 1, 1).data);
  };
  window.__ambientSampleAt = (x, y) => {
    const canvas = document.querySelector('#btfer-ambient-backdrop canvas');
    return Array.from(read.call(canvas.getContext('2d'), Math.floor(x / innerWidth * canvas.width),
      Math.floor(y / innerHeight * canvas.height), 1, 1).data);
  };
}

async function run(channel, origin, otherOrigin) {
  const browser = await chromium.launch({ channel, headless: true });
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 }, hasTouch: true });
  await context.addInitScript(installInstrumentation);
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  try {
    await page.goto(`${origin}/video/BV1test/`);
    await page.waitForSelector('#btfer-ambient-backdrop[data-has-frame]');
    const ui = page.locator('#btfer-ambient-ui');
    const opener = ui.locator('#opener');

    await check(`${channel}: live video paints without reading pixels or changing source`, async () => {
      await expectDrawing(page);
      const cool = await page.evaluate(() => window.__ambientSample());
      await page.evaluate(() => window.fixture.setTheme('warm'));
      await sleep(900);
      const warm = await page.evaluate(() => window.__ambientSample());
      assert.ok(warm[0] > cool[0] + 70, `${cool} -> ${warm}`);
      assert.equal(await page.evaluate(() => window.__ambientTest.reads), 0);
      assert.equal(await page.locator('video').getAttribute('crossorigin'), null);
      assert.equal(await page.locator('video').count(), 1);
      const colors = await page.evaluate(() => ({
        body: getComputedStyle(document.body).backgroundColor,
        title: getComputedStyle(document.querySelector('h1')).color,
        panel: getComputedStyle(document.querySelector('.video-info-container')).backgroundColor,
      }));
      assert.equal(colors.body, 'rgba(0, 0, 0, 0)');assert.equal(colors.title, 'rgb(241, 244, 255)');
      assert.ok(colors.panel.includes('0.46'));
    });
    await check(`${channel}: edge colors spill outward, center subjects do not enter the glow`, async () => {
      await page.evaluate(() => window.fixture.setTheme('edge-probe-a'));await sleep(1100);
      await page.locator('video').evaluate(el => el.pause());await sleep(80);
      const sampleEdges = () => page.evaluate(() => {
        const rect = document.querySelector('video').getBoundingClientRect();
        return {
          left: window.__ambientSampleAt(rect.left - 12, rect.top + rect.height / 2),
          right: window.__ambientSampleAt(rect.right + 36, rect.top + rect.height / 2),
          top: window.__ambientSampleAt(rect.left + rect.width / 2, rect.top - 48),
          center: window.__ambientSampleAt(rect.left + rect.width / 2, rect.top + rect.height / 2),
          far: window.__ambientSampleAt(innerWidth - 3, innerHeight - 3),
        };
      });
      const before = await sampleEdges();
      assert.ok(before.left[0] > before.left[1] * 1.7, `Warm left edge: ${before.left}`);
      assert.ok(before.right[1] > before.right[0] * 1.7, `Green right edge: ${before.right}`);
      assert.ok(before.top[2] > before.top[0] * 1.7, `Blue top edge: ${before.top}`);
      assert.equal(before.center[3], 0, 'The frame interior is not copied into the light field');
      assert.equal(before.far[3], 0, 'Distant areas remain transparent');
      await page.locator('video').evaluate(el => el.play());
      await page.evaluate(() => window.fixture.setTheme('edge-probe-b'));await sleep(1100);
      await page.locator('video').evaluate(el => el.pause());await sleep(80);
      const after = await sampleEdges();
      for (const side of ['left', 'right', 'top']) {
        for (let i = 0; i < 4; i++) assert.ok(Math.abs(before[side][i] - after[side][i]) < 5,
          `${side}: center must not affect edge light (${before[side]} -> ${after[side]})`);
      }
      if (channel === 'msedge') {
        fs.mkdirSync(path.join(project, 'test-results'), { recursive: true });
        await page.screenshot({ path: path.join(project, 'test-results', 'edge-spill-proof.png') });
      }
      await page.locator('video').evaluate(el => el.play());
      await page.evaluate(() => window.fixture.setTheme('cool'));await sleep(750);
    });
    await check(`${channel}: maximum spread fills viewport corners, resizes and survives reload`, async () => {
      await page.evaluate(() => window.fixture.setTheme('edge-probe-a'));await sleep(250);
      await page.locator('video').evaluate(el => el.pause());await sleep(80);
      await opener.click();await ui.locator('#spread').fill('560');
      assert.equal(await ui.locator('#spread-value').innerText(), '全屏');
      await ui.locator('#close').click();
      for (const viewport of [{ width: 1280, height: 800 }, { width: 2560, height: 1392 }, { width: 800, height: 1280 }]) {
        await page.setViewportSize(viewport);
        await page.waitForFunction(({ width, height }) => {
          const canvas = document.querySelector('#btfer-ambient-backdrop canvas');
          return canvas.height === Math.round(canvas.width * height / width);
        }, viewport);
        const points = await page.evaluate(() => {
          const sample = window.__ambientSampleAt;
          const rect = document.querySelector('video').getBoundingClientRect();
          return {
            edges: [sample(3, 3), sample(innerWidth - 3, 3), sample(3, innerHeight - 3),
              sample(innerWidth - 3, innerHeight - 3), sample(innerWidth - 3, innerHeight / 2)],
            center: sample(rect.left + rect.width / 2, rect.top + rect.height / 2),
          };
        });
        assert.ok(points.edges.every(pixel => pixel[3] >= 195), `${JSON.stringify(viewport)}: ${JSON.stringify(points.edges)}`);
        assert.equal(points.center[3], 0, 'Full-page coverage still excludes the video interior');
        if (channel === 'msedge' && viewport.width === 1280) {
          await page.screenshot({ path: path.join(project, 'test-results', 'full-page-glow-proof.png') });
        }
      }
      await page.setViewportSize({ width: 1280, height: 800 });
      await page.locator('video').evaluate(el => el.play());
      await page.evaluate(() => window.fixture.setTheme('cool'));await sleep(350);
      await page.locator('video').evaluate(el => el.pause());await sleep(80);
      if (channel === 'msedge') {
        await page.screenshot({ path: path.join(project, 'test-results', 'full-page-glow-preview.png') });
      }
      await sleep(220);await page.reload();
      await page.waitForSelector('#btfer-ambient-backdrop[data-has-frame]');
      await opener.click();assert.equal(await ui.locator('#spread-value').innerText(), '全屏');
      assert.ok(await page.evaluate(() => window.__ambientSampleAt(innerWidth - 3, innerHeight - 3)[3]) >= 195);
      await ui.locator('#reset').click();await ui.locator('#close').click();
      assert.equal(await page.evaluate(() => window.__ambientSampleAt(innerWidth - 3, innerHeight - 3)[3]), 0);
    });
    await check(`${channel}: light follows player position when scrolling a paused video`, async () => {
      await page.locator('video').evaluate(el => el.pause());await expectStopped(page);
      const before = await count(page);
      await page.evaluate(() => window.scrollTo(0, 80));
      await page.waitForFunction(previous => window.__ambientTest.draws > previous, before);
      await expectStopped(page);
      await page.evaluate(() => window.scrollTo(0, 0));await sleep(200);
      await page.locator('video').evaluate(el => el.play());await expectDrawing(page);
    });
    await check(`${channel}: pause, resume and background suspension`, async () => {
      await page.locator('video').evaluate((el) => el.pause());
      await expectStopped(page);
      await page.locator('video').evaluate((el) => el.play());
      await expectDrawing(page);
      await page.evaluate(() => {
        Object.defineProperty(document, 'hidden', { configurable: true, value: true });
        document.dispatchEvent(new Event('visibilitychange'));
      });
      await expectStopped(page);
      await page.evaluate(() => { delete document.hidden;document.dispatchEvent(new Event('visibilitychange')); });
      await expectDrawing(page);
    });
    await check(`${channel}: touch settings, saved values and disable restores page`, async () => {
      await opener.click();
      assert.equal(await opener.getAttribute('aria-expanded'), 'true');
      await ui.locator('#brightness').fill('105');await ui.locator('#blur').fill('48');
      await ui.locator('#spread').fill('440');
      await ui.locator('#profile').selectOption('eco');
      await ui.locator('#enabled').uncheck();
      assert.equal(await active(page), null);await expectStopped(page);
      assert.equal(await page.locator('body').evaluate((el) => getComputedStyle(el).backgroundColor), 'rgb(255, 255, 255)');
      await sleep(240);await page.reload();
      assert.equal(await active(page), null);
      await opener.click();assert.equal(await ui.locator('#brightness').inputValue(), '105');
      assert.equal(await ui.locator('#spread').inputValue(), '440');
      assert.equal(await ui.locator('#profile').inputValue(), 'eco');
      await ui.locator('#reset').click();
      assert.notEqual(await active(page), null);
      assert.equal(await ui.locator('#blur').inputValue(), '36');
      await expectDrawing(page);
      await page.keyboard.press('Escape');assert.equal(await opener.getAttribute('aria-expanded'), 'false');
    });
    await check(`${channel}: replaces player and follows SPA navigation`, async () => {
      await page.evaluate(() => window.fixture.replaceVideo());
      await sleep(1400);await expectDrawing(page);
      await page.evaluate(() => history.pushState({}, '', '/'));
      await page.waitForFunction(() => !document.documentElement.hasAttribute('data-btfer-active'));
      await expectStopped(page);assert.equal(await ui.isVisible(), false);
      await page.evaluate(() => history.pushState({}, '', '/video/BV1next/?p=2'));
      await page.waitForSelector('#btfer-ambient-backdrop[data-has-frame]');await expectDrawing(page);
      await page.addScriptTag({ content: script.toString() });
      assert.equal(await page.locator('#btfer-ambient-backdrop').count(), 1);
      assert.equal(await page.locator('#btfer-ambient-ui').count(), 1);
    });
    await check(`${channel}: stops on unsupported frames and reconnects`, async () => {
      await page.evaluate(() => { window.__ambientTest.fail = true; });
      await page.waitForFunction(() => !document.querySelector('#btfer-ambient-backdrop').hasAttribute('data-has-frame'));
      await expectStopped(page);
      await opener.click();assert.match(await ui.locator('#status').innerText(), /暂时无法/);
      await page.evaluate(() => { window.__ambientTest.fail = false; });
      await ui.locator('#retry').click();await expectDrawing(page);
      await ui.locator('#close').click();
    });
    await check(`${channel}: native fullscreen pauses ambient and resumes on exit`, async () => {
      await page.locator('#fullscreen').click();
      await page.waitForFunction(() => Boolean(document.fullscreenElement));await expectStopped(page);
      await page.evaluate(() => document.exitFullscreen());await expectDrawing(page);
    });
    await check(`${channel}: open shadow video connects, closed special player reports limitation`, async () => {
      await page.evaluate(async () => {
        const old = document.querySelector('video');const stream = old.srcObject;old.pause();
        const custom = document.createElement('bwp-video');custom.style.cssText = 'display:block;width:100%;height:100%';
        const shadow = custom.attachShadow({ mode: 'open' });
        const inner = document.createElement('video');inner.style.cssText = 'width:100%;height:100%';
        inner.muted = true;inner.srcObject = stream;shadow.append(inner);old.replaceWith(custom);await inner.play();
        window.__shadowStream = stream;
      });
      await sleep(1400);await expectDrawing(page);
      await page.evaluate(() => {
        const custom = document.querySelector('bwp-video');custom.shadowRoot.querySelector('video').pause();
        const closed = document.createElement('bwp-video');closed.style.cssText = 'display:block;width:100%;height:100%';
        closed.attachShadow({ mode: 'closed' });custom.replaceWith(closed);
      });
      await sleep(1400);await opener.click();assert.match(await ui.locator('#status').innerText(), /当前播放器暂不支持/);
      await ui.locator('#close').click();
      await page.evaluate(async () => {
        const next = document.createElement('video');next.muted = true;next.srcObject = window.__shadowStream;
        document.querySelector('bwp-video').replaceWith(next);await next.play();
      });
      await sleep(1400);await expectDrawing(page);
    });
    if (channel === 'msedge') {
      await page.evaluate(() => window.fixture.setTheme('cool'));await sleep(700);
      fs.mkdirSync(path.join(project, 'test-results'), { recursive: true });
      await page.screenshot({ path: path.join(project, 'test-results', 'tablet-preview.png') });
      await opener.click();
      await page.screenshot({ path: path.join(project, 'test-results', 'settings-preview.png') });
      await ui.locator('#close').click();
    }
    await check(`${channel}: portrait settings stay inside viewport`, async () => {
      await page.setViewportSize({ width: 800, height: 1280 });await opener.click();
      const bounds = await ui.locator('#panel').boundingBox();
      assert.ok(bounds.x >= 0 && bounds.y >= 0 && bounds.x + bounds.width <= 800 && bounds.y + bounds.height <= 1280);
      await ui.locator('#close').click();
    });
    await check(`${channel}: cross-origin video still draws without CORS readback`, async () => {
      media = Buffer.from(await page.evaluate(() => window.fixture.record()));
      assert.ok(media.length > 1000);
      await page.locator('video').evaluate((el, src) => {
        el.pause();el.srcObject = null;el.src = src;el.loop = true;return el.play();
      }, `${otherOrigin}/sample.webm`);
      await page.waitForSelector('#btfer-ambient-backdrop[data-has-frame]');await expectDrawing(page);
      const blocked = await page.evaluate(() => { try { window.__ambientSample();return false; } catch (error) { return error.name === 'SecurityError'; } });
      assert.equal(blocked, true);
      assert.equal(await page.evaluate(() => window.__ambientTest.reads), 0);
      assert.equal(await page.locator('video').getAttribute('crossorigin'), null);
    });
    assert.deepEqual(errors, [], 'No uncaught browser errors');

    await check(`${channel}: timer fallback when video frame callbacks are unavailable`, async () => {
      const fallback = await browser.newContext();
      await fallback.addInitScript(installInstrumentation);
      await fallback.addInitScript(() => { HTMLVideoElement.prototype.requestVideoFrameCallback = undefined; });
      const alternate = await fallback.newPage();
      await alternate.goto(`${origin}/video/BV1fallback/`);
      await alternate.waitForSelector('#btfer-ambient-backdrop[data-has-frame]');
      await expectDrawing(alternate);await fallback.close();
    });
  } finally { await context.close();await browser.close(); }
}

(async () => {
  const server = createServer();const other = createServer();
  try {
    const origin = await listen(server);const otherOrigin = await listen(other);
    for (const channel of channels) await run(channel, origin, otherOrigin);
    console.log(`\n${results.length} browser checks passed.`);
  } finally { await Promise.all([new Promise(r => server.close(r)), new Promise(r => other.close(r))]); }
})().catch((error) => { console.error(error);process.exitCode = 1; });
