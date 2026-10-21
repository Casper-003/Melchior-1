// ==UserScript==
// @name         B站 · 流光毛玻璃
// @namespace    btfer.bilibili.ambient
// @version      0.3.0
// @description  视频边缘的色彩向页面溢出，形成实时环境光与毛玻璃面板。
// @author       Btfer
// @match        https://www.bilibili.com/*
// @match        https://bilibili.com/*
// @run-at       document-idle
// @noframes
// @grant        GM_getValue
// @grant        GM_setValue
// @grant        GM_registerMenuCommand
// ==/UserScript==

(() => {
  'use strict';

  const UI_ID = 'btfer-ambient-ui';
  const BACKDROP_ID = 'btfer-ambient-backdrop';
  const STORAGE_KEY = 'btfer.ambient.settings.v1';
  if (window.top !== window.self || document.getElementById(UI_ID)) return;

  const PROFILES = Object.freeze({
    eco: { label: '省电', width: 128, samples: 8, fps: 6 },
    balanced: { label: '均衡', width: 192, samples: 12, fps: 12 },
    smooth: { label: '流畅', width: 256, samples: 16, fps: 20 },
  });
  const DEFAULTS = Object.freeze({ enabled: true, brightness: 100, blur: 36, spread: 320, profile: 'balanced' });
  const FULL_SPREAD = 560;
  const clamp = (value, min, max, fallback) =>
    typeof value === 'number' && Number.isFinite(value) ? Math.min(max, Math.max(min, value)) : fallback;
  function normalize(value) {
    const input = value && typeof value === 'object' ? value : {};
    return {
      enabled: typeof input.enabled === 'boolean' ? input.enabled : DEFAULTS.enabled,
      brightness: clamp(input.brightness, 40, 160, DEFAULTS.brightness),
      blur: clamp(input.blur, 12, 72, DEFAULTS.blur),
      spread: clamp(input.spread, 120, FULL_SPREAD, DEFAULTS.spread),
      profile: Object.hasOwn(PROFILES, input.profile) ? input.profile : DEFAULTS.profile,
    };
  }
  function readSettings() {
    try {
      return normalize(typeof GM_getValue === 'function'
        ? GM_getValue(STORAGE_KEY, DEFAULTS)
        : JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null'));
    } catch { return { ...DEFAULTS }; }
  }
  function saveSettings() {
    try {
      if (typeof GM_setValue === 'function') GM_setValue(STORAGE_KEY, { ...settings });
      else localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
      storageFailed = false;
    } catch { storageFailed = true; }
    updateStatus();
  }

  let settings = readSettings();
  let storageFailed = false;
  let video = null;
  let activeRoute = '';
  let pageSuspended = false;
  let frameId = null;
  let frameOwner = null;
  let timerId = null;
  let lastDrawAt = 0;
  let hasFrame = false;
  let drawFailures = 0;
  let panelOpen = false;
  let persistTimer = null;
  let geometryKey = '';
  let layoutRequest = null;

  const style = document.createElement('style');
  style.id = 'btfer-ambient-style';
  style.textContent = `
    #${BACKDROP_ID} { display:none; pointer-events:none; position:fixed; inset:0; z-index:-1;
      overflow:hidden; background:#10131e; }
    #${BACKDROP_ID} canvas { position:absolute; inset:0; width:100%; height:100%;
      filter:blur(var(--btfer-blur,36px)) brightness(var(--btfer-brightness,1)) saturate(1.18);
      opacity:0; transition:opacity .55s ease; }
    #${BACKDROP_ID}[data-has-frame] canvas { opacity:1; }
    #${BACKDROP_ID}::after { content:''; position:absolute; inset:0;
      background:linear-gradient(180deg,rgba(8,12,22,.02),rgba(8,12,22,.12)); }
    html[data-btfer-active] { background:#10131e !important;
      --text1:#f1f4ff; --text2:#d5dced; --text3:#adb8d0; --text4:#8e9bb8;
      --bg1:#182132; --bg2:rgba(18,24,38,.9); --bg3:rgba(25,32,49,.94);
      --line_regular:rgba(219,230,255,.15); --line_light:rgba(219,230,255,.1);
      --graph_bg_regular:rgba(219,230,255,.09); }
    html[data-btfer-active] body { background:transparent !important; isolation:isolate; }
    html[data-btfer-active] #${BACKDROP_ID} { display:block; }
    html[data-btfer-active] :is(#app,.video-page-video,.video-container-v1,.video-container-v1 .left-container,
      .video-container-v1 .right-container,.video-container-v1 .right-container-inner) { background:transparent !important; }
    html[data-btfer-active] :is(.video-info-container,.video-toolbar-container,.video-desc-container,
      .right-container-inner,.video-container-v1 > .right-container,.bili-header__bar) {
      background:rgba(17,24,40,.46) !important; border:1px solid rgba(225,235,255,.13);
      box-shadow:0 8px 28px rgba(0,0,0,.08); border-radius:14px; }
    html[data-btfer-active] .bili-header__bar { border-radius:0; border-width:0 0 1px; }
    html[data-btfer-active] .video-info-container { padding:12px 16px; box-sizing:border-box; height:auto !important; }
    html[data-btfer-active] .video-toolbar-container { padding:0 12px; box-sizing:border-box; }
    html[data-btfer-active] .video-desc-container { padding:12px 16px; box-sizing:border-box; }
    html[data-btfer-active] .right-container-inner { padding:12px; box-sizing:border-box; }
    html[data-btfer-active] .video-container-v1 > .right-container:not(:has(.right-container-inner)) {
      padding:12px; box-sizing:border-box; }
    html[data-btfer-active] .video-container-v1 > .right-container:has(.right-container-inner) {
      background:transparent !important; border:0; box-shadow:none; }
    html[data-btfer-active] :is(.video-info-title,.video-title,.video-page-card-small .title,
      .up-panel-container .up-name,.bili-header__bar .left-entry__title,
      .bili-header__bar .right-entry__outside) { color:#f1f4ff !important; }
    html[data-btfer-active] :is(.video-info-detail,.video-info-detail-list,.video-toolbar-left,
      .video-toolbar-right,.video-desc-container,.video-page-card-small .playinfo) { color:#cbd5eb; }
    html[data-btfer-active] .right-container :is(.up-panel-container,.recommend-list-v1,.video-pod,
      .base-video-sections-v1,.video-sections-content-list) { background:transparent !important; }
    html[data-btfer-active] :is(.video-pod__header,.video-pod__body) { background:rgba(21,28,44,.25) !important; }
    @supports (backdrop-filter:blur(1px)) {
      html[data-btfer-active] :is(.video-info-container,.video-toolbar-container,.video-desc-container,
        .right-container-inner,.video-container-v1 > .right-container:not(:has(.right-container-inner)),.bili-header__bar) {
        backdrop-filter:blur(10px); -webkit-backdrop-filter:blur(10px); }
      html[data-btfer-active][data-btfer-profile="eco"] :is(.video-info-container,.video-toolbar-container,
        .video-desc-container,.right-container-inner,.video-container-v1 > .right-container,.bili-header__bar) {
        backdrop-filter:none; -webkit-backdrop-filter:none; background:rgba(17,24,40,.64) !important; }
    }
    html[data-btfer-fullscreen] #${BACKDROP_ID} { visibility:hidden; }
  `;
  document.head.append(style);

  const backdrop = document.createElement('div');
  backdrop.id = BACKDROP_ID;
  backdrop.setAttribute('aria-hidden', 'true');
  const canvas = document.createElement('canvas');
  canvas.width = 192;
  canvas.height = 120;
  backdrop.append(canvas);
  document.body.append(backdrop);
  const context = canvas.getContext('2d');
  const samples = document.createElement('canvas');
  const sampleContext = samples.getContext('2d');
  const field = document.createElement('canvas');
  const fieldContext = field.getContext('2d');

  const host = document.createElement('div');
  host.id = UI_ID;
  host.style.cssText = 'position:fixed;right:max(18px,env(safe-area-inset-right));bottom:max(22px,env(safe-area-inset-bottom));z-index:2147483646;display:none;';
  document.body.append(host);
  const shadow = host.attachShadow({ mode: 'open' });
  shadow.innerHTML = `
    <style>
      :host { font:14px/1.5 system-ui,-apple-system,"Segoe UI","Microsoft YaHei",sans-serif; color:#eff4ff; color-scheme:dark; }
      * { box-sizing:border-box; } [hidden] { display:none !important; }
      button,input,select { font:inherit; } button,input,select { touch-action:manipulation; }
      button { cursor:pointer; } button:focus-visible,input:focus-visible,select:focus-visible {
        outline:2px solid #9bceff; outline-offset:3px; }
      #opener { display:flex;align-items:center;gap:8px; min-height:46px;padding:10px 15px;
        border:1px solid #ffffff36;border-radius:24px;background:#172337e8;color:#eff4ff;
        box-shadow:0 4px 20px #0004; }
      #dot { width:9px;height:9px;border-radius:50%;background:#9edbff;box-shadow:0 0 10px #9edbff88; }
      #opener[aria-pressed="false"] #dot { background:#7d8799;box-shadow:none; }
      #panel { position:absolute;right:0;bottom:58px;width:310px;max-width:calc(100vw - 36px);
        max-height:calc(100dvh - 110px);overflow-y:auto;overscroll-behavior:contain;
        background:#121c2df5;border:1px solid #ffffff26;border-radius:20px;padding:18px;
        box-shadow:0 18px 60px #0007; }
      header { display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px; }
      h2 { font-size:17px;margin:0;font-weight:650;letter-spacing:.04em; }
      #close { background:transparent;color:#bfcce1;border:0;border-radius:10px;min-width:44px;min-height:44px;font-size:24px; }
      .row { display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:44px; }
      .toggle { cursor:pointer; } #enabled { width:22px;height:22px;accent-color:#99ccff; }
      .range { display:block;margin-top:14px; } .range span { display:flex;justify-content:space-between;gap:12px; }
      output { color:#a7d2ff;font-variant-numeric:tabular-nums; }
      input[type="range"] { width:100%;height:38px;margin:0;accent-color:#a7d2ff;cursor:pointer; }
      select { min-height:44px;max-width:170px;background:#223148;color:#eff4ff;border:1px solid #ffffff26;border-radius:10px;padding:6px 10px; }
      .hint { font-size:12px;color:#a6b6ce;margin:8px 0 0; }
      #status { margin:16px 0 0;padding:11px 12px;border-radius:10px;background:#ffffff08;color:#b8c9e3;font-size:12px;overflow-wrap:anywhere; }
      footer { display:flex;gap:10px;margin-top:12px; }
      footer button { flex:1;min-height:44px;background:#25364d;color:#e2edff;border:1px solid #ffffff14;border-radius:10px; }
    </style>
    <section id="panel" role="dialog" aria-labelledby="panel-title" hidden>
      <header><h2 id="panel-title">流光毛玻璃</h2><button id="close" type="button" aria-label="关闭设置">×</button></header>
      <label class="row toggle" for="enabled"><span>开启氛围效果</span><input id="enabled" type="checkbox"></label>
      <label class="range" for="brightness"><span>光晕强度<output id="brightness-value" for="brightness"></output></span>
        <input id="brightness" type="range" min="40" max="160" step="1"></label>
      <label class="range" for="spread"><span>光晕范围<output id="spread-value" for="spread"></output></span>
        <input id="spread" type="range" min="120" max="560" step="10"></label>
      <p class="hint">拉到最右侧为全屏扩散，色光会延伸到页面四角。</p>
      <label class="range" for="blur"><span>柔和程度<output id="blur-value" for="blur"></output></span>
        <input id="blur" type="range" min="12" max="72" step="1"></label>
      <label class="row" for="profile"><span>运行档位</span><select id="profile">
        <option value="eco">省电 · 6 帧/秒</option><option value="balanced">均衡 · 12 帧/秒</option>
        <option value="smooth">流畅 · 20 帧/秒</option></select></label>
      <p class="hint">平板建议先用均衡档。省电档会同时简化面板模糊。</p>
      <p id="status" role="status" aria-live="polite"></p>
      <footer><button id="retry" type="button">重新连接</button><button id="reset" type="button">恢复默认</button></footer>
    </section>
    <button id="opener" type="button" aria-controls="panel" aria-expanded="false" aria-label="打开流光毛玻璃设置">
      <span id="dot" aria-hidden="true"></span><span>氛围</span>
    </button>
  `;
  const $ = (id) => shadow.getElementById(id);
  const root = document.documentElement;

  function isWatchPage() {
    return /^\/video\/(?:BV[a-z0-9]+|av\d+)(?:\/|$)/i.test(location.pathname);
  }
  function setPanel(open, returnFocus = false) {
    panelOpen = open;
    $('panel').hidden = !open;
    $('opener').setAttribute('aria-expanded', String(open));
    if (open) { updateStatus(); $('close').focus({ preventScroll: true }); }
    else if (returnFocus) $('opener').focus({ preventScroll: true });
  }
  function updateStatus() {
    let message;
    if (!settings.enabled) message = '已关闭 · 页面样式已恢复';
    else if (!context || !sampleContext || !fieldContext) message = '当前浏览器无法生成氛围光';
    else if (drawFailures >= 3) message = '暂时无法读取视频画面，可尝试“重新连接”';
    else if (!video && document.querySelector('#bilibili-player bwp-video, .bpx-player-container bwp-video')) {
      message = '当前播放器暂不支持实时背景，可尝试其他视频或播放编码';
    }
    else if (!video) message = '等待B站播放器…';
    else if (pageSuspended || document.hidden) message = '页面在后台 · 已暂停更新';
    else if (document.fullscreenElement) message = '全屏播放中 · 氛围背景已暂停';
    else if (document.pictureInPictureElement === video) message = '画中画播放中 · 背景保持';
    else if (!hasFrame) message = '等待视频画面…';
    else if (video.ended) message = '播放结束 · 背景保持';
    else if (video.paused) message = '视频已暂停 · 背景保持';
    else message = `实时溢光 · ${PROFILES[settings.profile].label} · 最高 ${PROFILES[settings.profile].fps} 帧/秒`;
    if (storageFailed) message += '；设置暂未保存';
    if ($('status').textContent !== message) $('status').textContent = message;
    $('opener').setAttribute('aria-pressed', String(settings.enabled));
  }
  function syncControls() {
    $('enabled').checked = settings.enabled;
    $('brightness').value = String(settings.brightness);
    $('blur').value = String(settings.blur);
    $('spread').value = String(settings.spread);
    $('profile').value = settings.profile;
    $('brightness-value').textContent = `${settings.brightness}%`;
    $('blur-value').textContent = `${settings.blur}px`;
    $('spread-value').textContent = settings.spread === FULL_SPREAD ? '全屏' : `${settings.spread}px`;
    $('spread').setAttribute('aria-valuetext', settings.spread === FULL_SPREAD ? '全屏扩散' : `${settings.spread}像素`);
  }
  function applySettings() {
    root.toggleAttribute('data-btfer-active', Boolean(activeRoute && settings.enabled));
    if (activeRoute && settings.enabled) root.setAttribute('data-btfer-profile', settings.profile);
    else root.removeAttribute('data-btfer-profile');
    backdrop.style.setProperty('--btfer-blur', `${settings.blur}px`);
    backdrop.style.setProperty('--btfer-brightness', String(settings.brightness / 100));
    syncControls();
    stopLoop();
    if (settings.enabled) { drawFrame(true); scheduleFrame(); }
    updateStatus();
  }
  function changeSettings(patch) {
    settings = normalize({ ...settings, ...patch });
    applySettings();
    clearTimeout(persistTimer);
    persistTimer = setTimeout(() => { persistTimer = null; saveSettings(); }, 180);
  }
  $('opener').addEventListener('click', () => setPanel(!panelOpen));
  $('close').addEventListener('click', () => setPanel(false, true));
  $('enabled').addEventListener('change', (event) => changeSettings({ enabled: event.target.checked }));
  for (const name of ['brightness', 'blur', 'spread']) {
    $(name).addEventListener('input', (event) => changeSettings({ [name]: Number(event.target.value) }));
  }
  $('profile').addEventListener('change', (event) => changeSettings({ profile: event.target.value }));
  $('reset').addEventListener('click', () => changeSettings(DEFAULTS));
  $('retry').addEventListener('click', () => { bindVideo(null); reconcile(); });
  document.addEventListener('pointerdown', (event) => {
    if (panelOpen && !event.composedPath().includes(host)) setPanel(false);
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && panelOpen) { event.stopPropagation(); setPanel(false, true); }
  }, true);
  if (typeof GM_registerMenuCommand === 'function') {
    GM_registerMenuCommand('流光毛玻璃 · 设置', () => {
      if (activeRoute) setPanel(true);
      else window.alert('请先打开B站普通视频播放页，再调整流光毛玻璃。');
    });
  }

  function findVideo() {
    const candidates = [...document.querySelectorAll(
      '#bilibili-player video, .bpx-player-container video, .bilibili-player video, #playerWrap video, .player-wrap video'
    )];
    for (const custom of document.querySelectorAll('#bilibili-player bwp-video, .bpx-player-container bwp-video')) {
      if (custom.shadowRoot) candidates.push(...custom.shadowRoot.querySelectorAll('video'));
    }
    let best = null;
    let bestScore = -1;
    for (const candidate of candidates) {
      const rect = candidate.getBoundingClientRect();
      if (rect.width < 80 || rect.height < 45 || candidate.closest('[hidden]')) continue;
      const computed = getComputedStyle(candidate);
      if (computed.visibility === 'hidden' || computed.display === 'none') continue;
      const score = rect.width * rect.height + (candidate.readyState >= 2 ? 10000 : 0);
      if (score > bestScore) { best = candidate; bestScore = score; }
    }
    return best;
  }
  function resetFrame() {
    hasFrame = false;
    lastDrawAt = 0;
    geometryKey = '';
    drawFailures = 0;
    backdrop.removeAttribute('data-has-frame');
    // Resizing clears both the previous pixels and the canvas's origin-clean state.
    canvas.width = canvas.width;
    field.width = field.width;
    samples.width = samples.width;
  }
  function canDraw() {
    return Boolean(context && sampleContext && fieldContext && activeRoute && settings.enabled && video?.isConnected && !pageSuspended &&
      !document.hidden && !document.fullscreenElement && document.pictureInPictureElement !== video &&
      video.readyState >= 2 && video.videoWidth > 0 && video.videoHeight > 0 && drawFailures < 3);
  }
  function videoBounds() {
    const rect = video.getBoundingClientRect();
    let { left, top, width, height } = rect;
    const fit = getComputedStyle(video).objectFit;
    if (fit === 'contain' || fit === 'scale-down') {
      const ratio = Math.min(width / video.videoWidth, height / video.videoHeight);
      const actualWidth = video.videoWidth * ratio;
      const actualHeight = video.videoHeight * ratio;
      left += (width - actualWidth) / 2;
      top += (height - actualHeight) / 2;
      width = actualWidth;
      height = actualHeight;
    }
    return { left, top, width, height };
  }
  function boundsKey(bounds) {
    return [bounds.left, bounds.top, bounds.width, bounds.height, innerWidth, innerHeight]
      .map(Math.round).join(',');
  }
  function paintViewportSpill(x, y, width, height, amount) {
    if (amount <= 0) return;
    // Extend only the edge strips and corner colors to the viewport bounds.
    // This fills every exposed part of the page, including diagonal corners,
    // without bringing the center of the video back into the background.
    const left = Math.max(0, Math.min(field.width, x));
    const right = Math.max(0, Math.min(field.width, x + width));
    const top = Math.max(0, Math.min(field.height, y));
    const bottom = Math.max(0, Math.min(field.height, y + height));
    const columns = samples.width;
    const rows = samples.height;
    const drawPatch = (sourceX, sourceY, sourceWidth, sourceHeight, dx, dy, dw, dh) => {
      if (dw > 0 && dh > 0) fieldContext.drawImage(samples, sourceX, sourceY, sourceWidth, sourceHeight, dx, dy, dw, dh);
    };
    fieldContext.save();
    fieldContext.globalCompositeOperation = 'destination-over';
    fieldContext.globalAlpha = 0.82 * amount;
    try {
      drawPatch(0, 0, columns, 1, left, 0, right - left, top);
      drawPatch(0, rows - 1, columns, 1, left, bottom, right - left, field.height - bottom);
      drawPatch(0, 0, 1, rows, 0, top, left, bottom - top);
      drawPatch(columns - 1, 0, 1, rows, right, top, field.width - right, bottom - top);
      drawPatch(0, 0, 1, 1, 0, 0, left, top);
      drawPatch(columns - 1, 0, 1, 1, right, 0, field.width - right, top);
      drawPatch(0, rows - 1, 1, 1, 0, bottom, left, field.height - bottom);
      drawPatch(columns - 1, rows - 1, 1, 1, right, bottom, field.width - right, field.height - bottom);
    } finally { fieldContext.restore(); }
  }
  function paintEdgeLight(bounds, profile) {
    // The coarse sample is used only as four edge strips. Interior subjects are
    // deliberately excluded from the light field; no pixel readback is needed.
    const columns = profile.samples;
    const rows = Math.max(5, Math.round(columns * video.videoHeight / video.videoWidth));
    if (samples.width !== columns || samples.height !== rows) {
      samples.width = columns;
      samples.height = rows;
    }
    sampleContext.drawImage(video, 0, 0, columns, rows);
    const sx = field.width / innerWidth;
    const sy = field.height / innerHeight;
    const x = bounds.left * sx;
    const y = bounds.top * sy;
    const width = bounds.width * sx;
    const height = bounds.height * sy;
    const steps = 16;
    const step = settings.spread / steps;
    fieldContext.clearRect(0, 0, field.width, field.height);
    fieldContext.imageSmoothingEnabled = true;
    for (let i = 0; i < steps; i++) {
      const distance = i * step;
      const flare = distance * 0.5;
      fieldContext.globalAlpha = 0.95 * Math.pow(1 - i / steps, 1.7);
      // The four ribbons expand from the player's actual position. Their
      // opacity decays with distance, including where their corners meet.
      fieldContext.drawImage(samples, 0, 0, columns, 1,
        x - flare * sx, y - (distance + step) * sy, width + flare * 2 * sx, (step + 1) * sy);
      fieldContext.drawImage(samples, 0, rows - 1, columns, 1,
        x - flare * sx, y + height + distance * sy, width + flare * 2 * sx, (step + 1) * sy);
      fieldContext.drawImage(samples, 0, 0, 1, rows,
        x - (distance + step) * sx, y - flare * sy, (step + 1) * sx, height + flare * 2 * sy);
      fieldContext.drawImage(samples, columns - 1, 0, 1, rows,
        x + width + distance * sx, y - flare * sy, (step + 1) * sx, height + flare * 2 * sy);
    }
    fieldContext.globalAlpha = 1;
    // Blend smoothly into viewport coverage over the final part of the slider.
    // The endpoint is relative to the window rather than a fixed pixel radius.
    const coverage = Math.max(0, (settings.spread - 440) / (FULL_SPREAD - 440));
    paintViewportSpill(x, y, width, height, coverage * coverage * (3 - 2 * coverage));
  }
  function drawFrame(force = false) {
    if (!canDraw()) return;
    const now = performance.now();
    const profile = PROFILES[settings.profile];
    if (!force && now - lastDrawAt < 1000 / profile.fps - 1) return;
    try {
      const width = profile.width;
      const height = Math.max(48, Math.min(768, Math.round(width * innerHeight / innerWidth)));
      if (canvas.width !== width || canvas.height !== height) {
        canvas.width = width;
        canvas.height = height;
        field.width = width;
        field.height = height;
        hasFrame = false;
      }
      if (field.width !== width || field.height !== height) { field.width = width; field.height = height; }
      const bounds = videoBounds();
      const key = boundsKey(bounds);
      const moved = key !== geometryKey;
      paintEdgeLight(bounds, profile);
      const elapsed = Math.min(500, Math.max(1, now - lastDrawAt));
      if (!hasFrame || force || moved) {
        context.clearRect(0, 0, width, height);
        context.globalAlpha = 1;
      } else {
        const blend = 1 - Math.exp(-elapsed / 220);
        // Weighted premultiplied alpha keeps empty areas transparent rather
        // than accumulating an opaque copy of the previous light field.
        context.globalCompositeOperation = 'destination-out';
        context.globalAlpha = blend;
        context.fillRect(0, 0, width, height);
        context.globalCompositeOperation = 'lighter';
        context.globalAlpha = blend;
      }
      context.drawImage(field, 0, 0, width, height);
      context.globalAlpha = 1;
      context.globalCompositeOperation = 'source-over';
      geometryKey = key;
      lastDrawAt = now;
      hasFrame = true;
      drawFailures = 0;
      backdrop.setAttribute('data-has-frame', '');
    } catch (error) {
      context.globalAlpha = 1;
      context.globalCompositeOperation = 'source-over';
      drawFailures += 1;
      if (drawFailures === 3) {
        backdrop.removeAttribute('data-has-frame');
        console.warn('[流光毛玻璃] 当前视频无法生成背景，已停止更新。', error.name);
      }
    }
    updateStatus();
  }
  function stopLoop() {
    if (timerId !== null) clearTimeout(timerId);
    if (frameId !== null && frameOwner && typeof frameOwner.cancelVideoFrameCallback === 'function') {
      frameOwner.cancelVideoFrameCallback(frameId);
    }
    timerId = null;
    frameId = null;
    frameOwner = null;
  }
  function scheduleFrame() {
    if (timerId !== null || frameId !== null || !canDraw() || video.paused || video.ended) return;
    timerId = setTimeout(() => {
      timerId = null;
      if (!canDraw() || video.paused || video.ended) return;
      const owner = video;
      if (typeof owner.requestVideoFrameCallback === 'function') {
        frameOwner = owner;
        frameId = owner.requestVideoFrameCallback(() => {
          frameId = null;
          frameOwner = null;
          if (owner !== video) return;
          drawFrame();
          scheduleFrame();
        });
      } else {
        drawFrame();
        scheduleFrame();
      }
    }, 1000 / PROFILES[settings.profile].fps);
  }
  function onVideoEvent(event) {
    stopLoop();
    if (event.type === 'emptied' || event.type === 'loadstart') resetFrame();
    else {
      if (event.type === 'loadeddata') drawFailures = 0;
      drawFrame(true);
      scheduleFrame();
    }
    updateStatus();
  }
  const VIDEO_EVENTS = ['playing', 'pause', 'ended', 'loadeddata', 'loadedmetadata', 'seeked',
    'emptied', 'loadstart', 'resize', 'enterpictureinpicture', 'leavepictureinpicture'];
  function bindVideo(next) {
    stopLoop();
    if (video) VIDEO_EVENTS.forEach((event) => video.removeEventListener(event, onVideoEvent));
    video = next;
    resetFrame();
    if (video) {
      VIDEO_EVENTS.forEach((event) => video.addEventListener(event, onVideoEvent));
      drawFrame(true);
      scheduleFrame();
    }
    updateStatus();
  }
  function reconcile() {
    const nextRoute = isWatchPage() ? `${location.pathname}${location.search}` : '';
    if (nextRoute !== activeRoute) {
      activeRoute = nextRoute;
      bindVideo(null);
      host.style.display = activeRoute ? 'block' : 'none';
      if (!activeRoute) setPanel(false);
      applySettings();
    }
    if (!activeRoute) return;
    const nextVideo = findVideo();
    if (nextVideo !== video) bindVideo(nextVideo);
    else if (!hasFrame) { drawFrame(true); scheduleFrame(); }
    else if (canDraw() && boundsKey(videoBounds()) !== geometryKey) drawFrame(true);
    updateStatus();
  }
  function refreshLayout() {
    if (!activeRoute || !settings.enabled || layoutRequest !== null) return;
    layoutRequest = requestAnimationFrame(() => {
      layoutRequest = null;
      if (canDraw() && boundsKey(videoBounds()) !== geometryKey) drawFrame(true);
    });
  }
  function onVisibilityChange() {
    stopLoop();
    root.toggleAttribute('data-btfer-fullscreen', Boolean(document.fullscreenElement));
    drawFrame(true);
    scheduleFrame();
    updateStatus();
  }
  document.addEventListener('visibilitychange', onVisibilityChange);
  document.addEventListener('fullscreenchange', onVisibilityChange);
  window.addEventListener('popstate', reconcile);
  window.addEventListener('hashchange', reconcile);
  window.addEventListener('scroll', refreshLayout, { passive: true, capture: true });
  window.addEventListener('resize', refreshLayout, { passive: true });
  window.visualViewport?.addEventListener('resize', refreshLayout, { passive: true });
  window.addEventListener('pagehide', () => {
    pageSuspended = true;
    stopLoop();
    if (persistTimer !== null) { clearTimeout(persistTimer); persistTimer = null; saveSettings(); }
  });
  window.addEventListener('pageshow', () => { pageSuspended = false; reconcile(); onVisibilityChange(); });
  // A low-frequency scan avoids observing every mutation in the live danmaku DOM.
  setInterval(reconcile, 1200);
  reconcile();
})();
