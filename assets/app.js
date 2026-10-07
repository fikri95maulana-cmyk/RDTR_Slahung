/* WebGIS RDTR Kecamatan Slahung — Leaflet, tanpa framework.
   Data layer dimuat per-permintaan lewat <script> (juga berjalan saat index.html dibuka langsung dari disk). */
(function () {
  'use strict';
  const CAT = window.CATALOG;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const svg = (id, cls = '') => `<svg class="i ${cls}"><use href="#i-${id}"/></svg>`;
  const byId = new Map(CAT.layers.map((l) => [l.id, l]));
  const groupOf = new Map(CAT.groups.map((g) => [g.id, g]));

  /* ------------------------------------------------------------ basemap */
  const G = 'https://mt{s}.google.com/vt/lyrs=';
  const BASEMAPS = [
    { id: 'sat', name: 'Google Satelit', url: G + 's&x={x}&y={y}&z={z}', sub: '0123', max: 21, attr: 'Imagery © Google' },
    { id: 'hyb', name: 'Google Satelit + Label', url: G + 'y&x={x}&y={y}&z={z}', sub: '0123', max: 21, attr: 'Imagery © Google' },
    { id: 'road', name: 'Google Peta Jalan', url: G + 'm&x={x}&y={y}&z={z}', sub: '0123', max: 21, attr: 'Map © Google' },
    { id: 'ter', name: 'Google Medan', url: G + 'p&x={x}&y={y}&z={z}', sub: '0123', max: 20, attr: 'Map © Google' },
    { id: 'osm', name: 'OpenStreetMap', url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png', sub: 'abc', max: 19, attr: '© OpenStreetMap contributors' },
    { id: 'light', name: 'Carto Terang', url: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', sub: 'abcd', max: 20, attr: '© OpenStreetMap, © CARTO' },
    { id: 'dark', name: 'Carto Gelap', url: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', sub: 'abcd', max: 20, attr: '© OpenStreetMap, © CARTO' },
    { id: 'none', name: 'Tanpa Basemap', url: null },
  ];

  /* --------------------------------------------------------------- peta */
  const map = L.map('map', { zoomControl: false, maxZoom: 21, minZoom: 9, zoomSnap: 0.5, zoomDelta: 0.5, attributionControl: true, doubleClickZoom: false });
  map.attributionControl.setPrefix('WebGIS RDTR Slahung · <a href="https://leafletjs.com" target="_blank" rel="noopener">Leaflet</a>');
  L.control.zoom({ position: 'topright', zoomInTitle: 'Perbesar', zoomOutTitle: 'Perkecil' }).addTo(map);
  L.control.scale({ metric: true, imperial: false, position: 'bottomleft' }).addTo(map);
  const home = L.latLngBounds(CAT.bounds);
  map.fitBounds(home, { padding: [20, 20] });
  map.setMaxBounds(home.pad(2.5));

  const paneZ = { raster: 210, poly: 300, line: 400, point: 500 };
  map.createPane('highlight').style.zIndex = 610;
  map.createPane('labels').style.zIndex = 620;
  map.getPane('highlight').style.pointerEvents = 'none';
  map.getPane('labels').style.pointerEvents = 'none';

  let baseLayer = null, baseId = null;
  function setBasemap(id) {
    const b = BASEMAPS.find((x) => x.id === id) || BASEMAPS[0];
    if (baseLayer) map.removeLayer(baseLayer);
    baseLayer = null;
    if (b.url) {
      baseLayer = L.tileLayer(b.url, { subdomains: b.sub, maxZoom: b.max, maxNativeZoom: Math.min(b.max, 20), attribution: b.attr, crossOrigin: false });
      baseLayer.addTo(map).bringToBack();
    }
    baseId = b.id;
    $('#basemapName').textContent = b.name;
    $$('.bm').forEach((n) => n.classList.toggle('on', n.dataset.id === b.id));
    const dark = b.id === 'sat' || b.id === 'hyb' || b.id === 'dark' || b.id === 'none';
    $('#map').style.background = dark ? '#0b1f3a' : '#e8eef5';
    syncHash();
  }
  function tileThumb(b) {
    if (!b.url) return 'repeating-linear-gradient(45deg,#e2e8f0 0 8px,#f8fafc 8px 16px)';
    const z = 12, lat = -8.02, lon = 111.4;
    const x = Math.floor(((lon + 180) / 360) * 2 ** z);
    const y = Math.floor(((1 - Math.log(Math.tan((lat * Math.PI) / 180) + 1 / Math.cos((lat * Math.PI) / 180)) / Math.PI) / 2) * 2 ** z);
    const u = b.url.replace('{s}', b.sub[0]).replace('{x}', x).replace('{y}', y).replace('{z}', z).replace('{r}', '');
    return `url("${u}")`;
  }
  (function buildBasemapMenu() {
    const m = $('#basemapMenu');
    BASEMAPS.forEach((b) => {
      const n = document.createElement('button');
      n.className = 'bm'; n.dataset.id = b.id;
      n.innerHTML = `<span class="th" style="background-image:${tileThumb(b)}"></span><span class="t">${esc(b.name)}</span>`;
      n.onclick = () => { setBasemap(b.id); m.hidden = true; $('#basemapBtn').setAttribute('aria-expanded', 'false'); };
      m.appendChild(n);
    });
    $('#basemapBtn').onclick = () => { m.hidden = !m.hidden; $('#basemapBtn').setAttribute('aria-expanded', String(!m.hidden)); };
    map.on('click', () => { m.hidden = true; });
  })();

  /* --------------------------------------------------- pemuatan data */
  const waiters = {}, store = {}, infoStore = {};
  window.__L = (id, fc) => { store[id] = fc; waiters[id] && waiters[id](fc); };
  window.__I = (id, obj) => { infoStore[id] = obj; waiters['i:' + id] && waiters['i:' + id](obj); };
  function loadScript(key, src, cache) {
    if (cache[key.replace(/^i:/, '')]) return Promise.resolve(cache[key.replace(/^i:/, '')]);
    return new Promise((res, rej) => {
      waiters[key] = res;
      const s = document.createElement('script');
      s.src = src; s.async = true;
      s.onerror = () => rej(new Error('Gagal memuat ' + src));
      document.head.appendChild(s);
    });
  }
  const loadFC = (meta) => loadScript(meta.id, meta.file, store);
  const loadInfo = (folder) => loadScript('i:' + folder, `data/info/${folder}.js`, infoStore);

  /* ---------------------------------------------------------- gaya */
  const key = (v) => (v === undefined || v === null ? '' : String(v));
  function itemMap(meta) { return meta._im || (meta._im = new Map((meta.style.items || []).map((it) => [it.v, it]))); }
  function itemFor(meta, f) { return meta.style.kind === 'cat' ? itemMap(meta).get(key(f.properties[meta.style.by])) : null; }
  function styleFn(meta) {
    const s = meta.style;
    return (f) => {
      if (s.kind === 'contour') {
        const idx = Number(f.properties.VALKNT) % 50 === 0;
        return { color: idx ? '#fbbf24' : '#f59e0b', weight: idx ? 1.6 : 0.7, opacity: idx ? 0.95 : 0.7, fill: false };
      }
      const it = itemFor(meta, f);
      if (meta.geom === 'line') {
        return { color: it ? it.c : s.stroke, weight: (it && it.w) || s.w || 2, dashArray: (it && it.d) || s.dash || null, opacity: 1, lineCap: 'round', lineJoin: 'round' };
      }
      const w = s.w === undefined ? 1 : s.w;
      const fill = it ? it.c : s.fill;
      const fo = it && it.o !== undefined ? it.o : s.op === undefined ? 0.5 : s.op;
      return { stroke: w > 0, color: s.kind === 'cat' ? s.stroke || '#fff' : s.stroke || fill, weight: w, opacity: 0.95, dashArray: s.dash || null, fillColor: fill, fillOpacity: fo, fill: true };
    };
  }
  function pointLayer(meta, f, ll, pane, renderer) {
    const s = meta.style, it = itemFor(meta, f);
    const color = it ? it.c : s.fill || '#2563eb';
    const icon = (it && it.i) || s.icon;
    if (icon) {
      return L.marker(ll, { pane, interactive: false, keyboard: false, icon: L.divIcon({ className: 'pin-wrap', html: `<div class="pin" style="--c:${color}">${icon}</div>`, iconSize: [26, 26], iconAnchor: [13, 13] }) });
    }
    return L.circleMarker(ll, { pane, renderer, interactive: false, radius: s.r || 4, color: '#fff', weight: 1, fillColor: color, fillOpacity: 0.95 });
  }

  /* ------------------------------------------------------- legenda */
  function swatch(meta, it) {
    const s = meta.style;
    if (meta.geom === 'raster') return `<span class="sw poly" style="background:${it.c};border-color:rgba(15,23,42,.25)"></span>`;
    const c = it ? it.c : s.fill || s.stroke;
    if (meta.geom === 'line') return `<span class="sw line" style="border-top-color:${c};border-top-width:${Math.min(5, (it && it.w) || s.w || 2)}px;border-top-style:${((it && it.d) || s.dash) ? 'dashed' : 'solid'}"></span>`;
    if (meta.geom === 'point') {
      const icon = (it && it.i) || s.icon;
      return icon ? `<span class="sw pin" style="background:${c}">${icon}</span>` : `<span class="sw dot" style="background:${c}"></span>`;
    }
    const op = it && it.o !== undefined ? it.o : s.op === undefined ? 0.5 : s.op;
    const fillA = Math.max(op, op === 0 ? 0 : 0.35);
    const stroke = s.kind === 'cat' ? 'rgba(15,23,42,.3)' : s.stroke || c;
    return `<span class="sw poly" style="background:${hexA(c, fillA)};border-color:${stroke}"></span>`;
  }
  function hexA(hex, a) {
    const m = /^#([0-9a-f]{6})$/i.exec(hex); if (!m) return hex;
    const n = parseInt(m[1], 16);
    return `rgba(${n >> 16},${(n >> 8) & 255},${n & 255},${a})`;
  }
  function legendItems(meta) {
    if (meta.geom === 'raster') return meta.legend.map((i) => ({ html: swatch(meta, i), l: i.l }));
    const s = meta.style;
    if (s.kind === 'contour') return [{ html: swatch({ geom: 'line', style: { stroke: '#fbbf24', w: 2 } }), l: 'Kontur indeks (kelipatan 50 m)' }, { html: swatch({ geom: 'line', style: { stroke: '#f59e0b', w: 1 } }), l: 'Kontur biasa (interval 12,5 m)' }];
    if (s.kind === 'cat') return s.items.map((it) => ({ html: swatch(meta, it), l: it.l, n: it.n }));
    return [{ html: swatch(meta), l: meta.name }];
  }
  function legendBlock(meta) {
    const items = legendItems(meta);
    const single = meta.style && meta.style.kind === 'single';
    return `<div class="lg"><h4>${esc(meta.name)}</h4>${single ? '' : items.map((i) => `<div class="lg-i">${i.html}<span>${esc(i.l)}</span>${i.n !== undefined && meta.geom !== 'raster' ? `<span class="n">${i.n}</span>` : ''}</div>`).join('')}${single ? `<div class="lg-i">${items[0].html}<span>${esc(meta.geom === 'point' ? 'Titik' : meta.geom === 'line' ? 'Garis' : 'Area')}</span></div>` : ''}</div>`;
  }
  function renderLegend() {
    const ids = order.slice().reverse();
    $('#legendBox').hidden = ids.length === 0;
    $('#legendBody').innerHTML = ids.map((id) => legendBlock(byId.get(id))).join('');
  }
  $('#legendHead').onclick = () => { const b = $('#legendBox'); b.classList.toggle('closed'); $('#legendHead').setAttribute('aria-expanded', String(!b.classList.contains('closed'))); };

  /* ------------------------------------------------ layer aktif/peta */
  const order = [];          // bawah -> atas
  const live = {};           // id -> {layer, labels, pane, opacity}
  const pending = new Set();

  function baseZ(meta) { return paneZ[meta.geom === 'raster' ? 'raster' : meta.geom]; }
  function applyZ() {
    order.forEach((id, idx) => {
      const L_ = live[id]; if (!L_) return;
      const meta = byId.get(id);
      L_.paneEl.style.zIndex = baseZ(meta) + Math.min(idx, 95);
    });
  }
  function labelMinZoom(meta) { return meta.geom === 'poly' ? 12 : meta.style.label_zoom || 14; }
  function buildLabels(meta, fc) {
    const grp = L.layerGroup();
    const cls = 'maplabel' + (meta.id.includes('sungai') ? ' river' : meta.geom === 'point' ? ' small' : '');
    fc.features.forEach((f) => {
      const p = f.properties; if (!p._lbl) return;
      L.marker([p._ly, p._lx], { pane: 'labels', interactive: false, keyboard: false, icon: L.divIcon({ className: cls, html: esc(p._lbl), iconSize: null }) }).addTo(grp);
    });
    return grp;
  }
  function updateLabels() {
    const z = map.getZoom();
    order.forEach((id) => {
      const lv = live[id]; if (!lv || !lv.labels) return;
      const show = z >= labelMinZoom(byId.get(id));
      const has = map.hasLayer(lv.labels);
      if (show && !has) lv.labels.addTo(map);
      if (!show && has) map.removeLayer(lv.labels);
    });
  }
  map.on('zoomend', updateLabels);

  async function activate(id, opts = {}) {
    const meta = byId.get(id);
    if (!meta || live[id] || pending.has(id)) return;
    pending.add(id); setBusy(id, true);
    try {
      const pane = 'p_' + id;
      const paneEl = map.getPane(pane) || map.createPane(pane);
      paneEl.style.pointerEvents = 'none';
      let layer, labels = null;
      if (meta.geom === 'raster') {
        layer = L.imageOverlay(meta.raster, meta.bounds, { pane, interactive: false });
      } else {
        const fc = await loadFC(meta);
        const renderer = L.canvas({ pane, padding: 0.4 });
        if (meta.geom === 'point') {
          layer = L.geoJSON(fc, { pane, pointToLayer: (f, ll) => pointLayer(meta, f, ll, pane, renderer) });
        } else {
          layer = L.geoJSON(fc, { pane, renderer, interactive: false, style: styleFn(meta) });
        }
        if (meta.label) labels = buildLabels(meta, fc);
      }
      live[id] = { layer, labels, paneEl, opacity: opts.opacity ?? 1 };
      order.push(id);
      layer.addTo(map);
      paneEl.style.opacity = live[id].opacity;
      applyZ(); updateLabels();
    } catch (e) {
      toast('Layer gagal dimuat: ' + meta.name, true);
      console.error(e);
      const cb = $(`input[data-id="${id}"]`); if (cb) cb.checked = false;
    } finally {
      pending.delete(id); setBusy(id, false);
      refreshUI();
    }
  }
  function deactivate(id) {
    const lv = live[id]; if (!lv) return;
    map.removeLayer(lv.layer);
    if (lv.labels && map.hasLayer(lv.labels)) map.removeLayer(lv.labels);
    delete live[id];
    order.splice(order.indexOf(id), 1);
    applyZ(); refreshUI();
  }
  function toggle(id, on) { on ? activate(id) : deactivate(id); }
  function setBusy(id, b) {
    const row = $(`.lyr[data-id="${id}"] .busy`);
    if (row) row.innerHTML = b ? '<span class="spinner sm"></span>' : '';
  }

  /* -------------------------------------------------- panel layer */
  const DRAW = { poly: 'Area', line: 'Garis', point: 'Titik', raster: 'Raster' };
  function fmtN(n) { return n.toLocaleString('id-ID'); }
  function sidebarSymbol(meta) {
    if (meta.geom === 'raster') return '<span class="sw ras"></span>';
    const s = meta.style;
    if (s.kind === 'cat') {
      const it = s.items[0];
      const many = s.items.slice(0, 4);
      if (meta.geom === 'point') return swatch(meta, it);
      if (meta.geom === 'line') return swatch(meta, it);
      return `<span style="display:flex;gap:1px">${many.map((i) => `<span style="width:5px;height:12px;background:${i.c};opacity:.9;border-radius:1px"></span>`).join('')}</span>`;
    }
    if (s.kind === 'contour') return swatch({ geom: 'line', style: { stroke: '#f59e0b', w: 2 } });
    return swatch(meta);
  }
  function buildGroups() {
    const wrap = $('#groups');
    wrap.innerHTML = '';
    CAT.groups.forEach((g) => {
      const items = CAT.layers.filter((l) => l.group === g.id);
      if (!items.length) return;
      const sec = document.createElement('section');
      sec.className = 'grp'; sec.dataset.g = g.id;
      sec.innerHTML = `<button class="grp-head"><span class="gi" style="background:${g.color}22">${g.icon}</span><span class="gn">${esc(g.name)}</span><span class="cnt">${items.length}</span>${svg('down', 'chev')}</button><div class="grp-body"></div>`;
      const body = $('.grp-body', sec);
      items.forEach((m) => {
        const d = document.createElement('div');
        d.className = 'lyr'; d.dataset.id = m.id; d.dataset.t = (m.name + ' ' + g.name + ' ' + (m.desc || '') + ' ' + (m.shp || '')).toLowerCase();
        d.innerHTML = `<div class="lyr-row"><input type="checkbox" data-id="${m.id}" aria-label="Tampilkan ${esc(m.name)}"><span class="sym">${sidebarSymbol(m)}</span><span class="lyr-name">${esc(m.name)}<small>${DRAW[m.geom]}${m.n ? ' · ' + fmtN(m.n) + ' objek' : ''}</small></span><span class="busy"></span><button class="more" title="Detail & opsi" aria-label="Detail layer">${svg('more')}</button></div>
        <div class="lyr-extra">${m.desc ? `<p>${esc(m.desc)}</p>` : ''}<div class="btnrow"><button class="btn small" data-a="zoom">${svg('focus')}Zoom</button><button class="btn small" data-a="info">${svg('info')}Info & Metadata</button>${m.geom !== 'raster' ? `<button class="btn small" data-a="table">${svg('table')}Tabel Atribut</button>` : ''}<a class="btn small" href="${esc(m.zip)}" download>${svg('download')}Unduh ZIP</a></div></div>`;
        body.appendChild(d);
      });
      wrap.appendChild(sec);
    });
  }
  const groupsEl = $('#groups');
  groupsEl.addEventListener('click', (e) => {
    const head = e.target.closest('.grp-head');
    if (head) { head.parentElement.classList.toggle('open'); return; }
    const row = e.target.closest('.lyr'); if (!row) return;
    const id = row.dataset.id;
    if (e.target.closest('.more')) { row.classList.toggle('expanded'); return; }
    const a = e.target.closest('[data-a]');
    if (a) { act(a.dataset.a, id); return; }
    if (e.target.closest('.lyr-name')) { const cb = $('input', row); cb.checked = !cb.checked; toggle(id, cb.checked); }
  });
  groupsEl.addEventListener('change', (e) => { if (e.target.matches('input[data-id]')) toggle(e.target.dataset.id, e.target.checked); });

  function act(a, id) {
    const m = byId.get(id);
    if (a === 'zoom') { map.fitBounds(m.bounds, { padding: [30, 30] }); closeSideOnMobile(); }
    if (a === 'info') showInfo(m);
    if (a === 'table') showTable(m);
  }

  function refreshUI() {
    $$('input[data-id]', groupsEl).forEach((cb) => { cb.checked = !!live[cb.dataset.id] || pending.has(cb.dataset.id); });
    $$('.grp', groupsEl).forEach((g) => {
      const n = $$('input:checked', g).length, c = $('.cnt', g);
      const total = CAT.layers.filter((l) => l.group === g.dataset.g).length;
      c.textContent = n ? `${n} / ${total}` : total; c.classList.toggle('has', n > 0);
    });
    $('#actCount').textContent = order.length;
    renderActive(); renderLegend(); syncHash();
  }
  function renderActive() {
    const box = $('#activeList');
    $('#noActive').hidden = order.length > 0;
    box.innerHTML = '';
    order.slice().reverse().forEach((id, i) => {
      const m = byId.get(id), lv = live[id];
      const d = document.createElement('div');
      d.className = 'act'; d.dataset.id = id;
      const pct = Math.round(lv.opacity * 100);
      d.innerHTML = `<div class="act-top"><span class="sym">${sidebarSymbol(m)}</span><span class="nm">${esc(m.name)}</span><div class="tools">
        <button class="tbtn" data-a="up" title="Naikkan urutan" ${i === 0 ? 'disabled style="opacity:.35"' : ''}>${svg('up')}</button>
        <button class="tbtn" data-a="down" title="Turunkan urutan" ${i === order.length - 1 ? 'disabled style="opacity:.35"' : ''}>${svg('down')}</button>
        <button class="tbtn" data-a="zoom" title="Zoom ke layer">${svg('focus')}</button>
        <button class="tbtn" data-a="info" title="Info & metadata">${svg('info')}</button>
        ${m.geom !== 'raster' ? `<button class="tbtn" data-a="table" title="Tabel atribut">${svg('table')}</button>` : ''}
        <button class="tbtn del" data-a="off" title="Matikan layer">${svg('x')}</button></div></div>
        <label class="opa">Transparansi<input type="range" min="5" max="100" value="${pct}" data-a="opa"><b>${pct}%</b></label>`;
      box.appendChild(d);
    });
  }
  $('#activeList').addEventListener('click', (e) => {
    const b = e.target.closest('[data-a]'); if (!b || b.disabled) return;
    const id = b.closest('.act').dataset.id, a = b.dataset.a;
    if (a === 'off') return deactivate(id);
    if (a === 'up' || a === 'down') {
      const i = order.indexOf(id), j = a === 'up' ? i + 1 : i - 1;
      if (j < 0 || j >= order.length) return;
      [order[i], order[j]] = [order[j], order[i]];
      applyZ(); renderActive(); renderLegend(); syncHash(); return;
    }
    act(a, id);
  });
  $('#activeList').addEventListener('input', (e) => {
    if (e.target.dataset.a !== 'opa') return;
    const id = e.target.closest('.act').dataset.id, v = e.target.value / 100;
    live[id].opacity = v; live[id].paneEl.style.opacity = v;
    e.target.nextElementSibling.textContent = Math.round(v * 100) + '%';
  });
  $('#activeList').addEventListener('change', syncHash);

  /* tab & pencarian */
  $$('.tab').forEach((t) => (t.onclick = () => {
    $$('.tab').forEach((x) => x.classList.toggle('active', x === t));
    $$('.tabpane').forEach((p) => p.classList.toggle('active', p.id === 'tab-' + t.dataset.tab));
  }));
  $('#layerSearch').addEventListener('input', (e) => {
    const q = e.target.value.trim().toLowerCase(), words = q.split(/\s+/).filter(Boolean);
    let any = false;
    $$('.grp', groupsEl).forEach((g) => {
      let n = 0;
      $$('.lyr', g).forEach((l) => {
        const ok = words.every((w) => l.dataset.t.includes(w));
        l.hidden = !ok; if (ok) n++;
        const nm = $('.lyr-name', l);
        const small = nm.querySelector('small').outerHTML, raw = byId.get(l.dataset.id).name;
        nm.innerHTML = (q && ok ? highlight(raw, words) : esc(raw)) + small;
      });
      g.hidden = n === 0; any = any || n > 0;
      if (q) g.classList.toggle('open', n > 0);
    });
    $('#noResult').hidden = any;
  });
  function highlight(txt, words) {
    let out = esc(txt);
    words.forEach((w) => { out = out.replace(new RegExp('(' + w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig'), '<mark>$1</mark>'); });
    return out;
  }
  $('#btnExpand').onclick = () => $$('.grp', groupsEl).forEach((g) => g.classList.add('open'));
  $('#btnCollapse').onclick = () => $$('.grp', groupsEl).forEach((g) => g.classList.remove('open'));
  $('#btnClear').onclick = () => { order.slice().forEach(deactivate); };

  /* ------------------------------------------------------ toast, modal */
  let toastT;
  function toast(msg, err) {
    const t = $('#toast'); t.textContent = msg; t.className = 'toast' + (err ? ' err' : ''); t.hidden = false;
    clearTimeout(toastT); toastT = setTimeout(() => (t.hidden = true), 3200);
  }
  function openModal(title, html) {
    $('#modalTitle').textContent = title; $('#modalBody').innerHTML = html; $('#modal').hidden = false;
  }
  const closeModal = () => { $('#modal').hidden = true; $('#modalBody').innerHTML = ''; };
  $('#modalClose').onclick = closeModal;
  $('#modal').addEventListener('mousedown', (e) => { if (e.target.id === 'modal') closeModal(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeModal(); });

  const NUMKEY = /thn|tahun|year|tgl|kode|code|^id|nomor|^no|kd[a-z]/i;
  function fmtVal(k, v) {
    if (v === undefined || v === null || v === '') return '–';
    if (typeof v === 'number') return NUMKEY.test(k) ? String(v) : v.toLocaleString('id-ID', { maximumFractionDigits: 2 });
    return esc(v);
  }
  function fmtCell(v) {
    if (v === '' || v === null || v === undefined) return '';
    if (typeof v === 'number') return v.toLocaleString('id-ID', { maximumFractionDigits: 2 });
    return esc(v);
  }
  function tableHTML(t) {
    return `${t.note ? `<p class="note">${esc(t.note)}</p>` : ''}<div class="tbl-wrap"><table class="dt"><thead><tr>${t.cols.map((c) => `<th>${esc(c)}</th>`).join('')}</tr></thead><tbody>${t.rows.map((r) => `<tr>${r.map((c) => `<td class="${typeof c === 'number' ? 'num' : ''}">${fmtCell(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
  }

  /* modal: info layer */
  async function showInfo(m) {
    const g = groupOf.get(m.group);
    const rows = [
      ['Kelompok', g.name], ['Jenis data', DRAW[m.geom] + (m.geom === 'raster' ? '' : ' (vektor)')],
      m.n ? ['Jumlah objek', fmtN(m.n)] : null,
      ['Sumber berkas', `${m.shp} (dalam ${m.zip})`], ['Ukuran data web', `${(m.kb / 1024).toFixed(2)} MB`],
    ].filter(Boolean);
    let html = `<div id="infoTabs" class="mtabs"><button class="mtab on" data-t="sum">Ringkasan</button></div><div id="infoPane"></div>`;
    openModal(m.name, html);
    const tabs = $('#infoTabs'), pane = $('#infoPane');
    const panes = { sum: `${m.desc ? `<p>${esc(m.desc)}</p>` : ''}<dl class="kv">${rows.map((r) => `<dt>${esc(r[0])}</dt><dd>${esc(r[1])}</dd>`).join('')}</dl>
      ${m.fields.length ? `<strong>Atribut yang ditampilkan</strong><div class="chips">${m.fields.map((f) => `<span class="chip">${esc(f[1])}</span>`).join('')}</div>` : ''}
      <legend-slot></legend-slot>
      <div class="btnrow"><a class="btn primary" href="${esc(m.zip)}" download>${svg('download')}Unduh Shapefile (ZIP)</a><button class="btn" id="infoZoom">${svg('focus')}Zoom ke layer</button></div>` };
    pane.innerHTML = panes.sum.replace('<legend-slot></legend-slot>', `<strong>Legenda</strong><div class="lg" style="margin:6px 0 14px">${legendItems(m).map((i) => `<div class="lg-i">${i.html}<span>${esc(i.l)}</span>${i.n !== undefined ? `<span class="n">${i.n}</span>` : ''}</div>`).join('')}</div>`);
    $('#infoZoom').onclick = () => { closeModal(); map.fitBounds(m.bounds, { padding: [30, 30] }); };
    if (m.info) {
      try {
        const info = await loadInfo(m.info);
        const addTab = (id, label, html) => {
          panes[id] = html; const b = document.createElement('button'); b.className = 'mtab'; b.dataset.t = id; b.textContent = label; tabs.appendChild(b);
        };
        if (info.text) addTab('met', 'Metode & Hasil Analisis', `<pre class="metode">${esc(info.text)}</pre>`);
        info.tables.forEach((t, i) => addTab('t' + i, t.title, tableHTML(t)));
      } catch (e) { /* abaikan */ }
    }
    tabs.onclick = (e) => {
      const b = e.target.closest('.mtab'); if (!b) return;
      $$('.mtab', tabs).forEach((x) => x.classList.toggle('on', x === b));
      pane.innerHTML = panes[b.dataset.t];
      if (b.dataset.t === 'sum') $('#infoZoom').onclick = () => { closeModal(); map.fitBounds(m.bounds, { padding: [30, 30] }); };
    };
  }

  /* modal: tabel atribut */
  async function showTable(m) {
    openModal('Tabel Atribut — ' + m.name, '<div class="spinner" style="margin:30px auto;border-color:#cbd5e1;border-top-color:#0d9488"></div>');
    let fc;
    try { fc = await loadFC(m); } catch (e) { return toast('Gagal memuat data', true); }
    const cols = m.fields.length ? m.fields : Object.keys(fc.features[0].properties).filter((k) => k[0] !== '_').map((k) => [k, k]);
    const feats = fc.features;
    const LIMIT = 800;
    $('#modalBody').innerHTML = `<div class="tbl-tools"><input id="tq" type="search" placeholder="Filter data…"><span class="note" id="tcount" style="margin:0"></span><button class="btn small" id="tcsv">${svg('download')}Unduh CSV</button></div>
      <div class="tbl-wrap"><table class="dt"><thead><tr>${cols.map((c) => `<th>${esc(c[1])}</th>`).join('')}</tr></thead><tbody id="tb"></tbody></table></div>`;
    const draw = (q) => {
      const ql = q.toLowerCase();
      const rows = [];
      feats.forEach((f, i) => {
        if (ql && !cols.some((c) => key(f.properties[c[0]]).toLowerCase().includes(ql))) return;
        rows.push([f, i]);
      });
      $('#tcount').textContent = `${fmtN(rows.length)} dari ${fmtN(feats.length)} objek${rows.length > LIMIT ? ` (menampilkan ${LIMIT})` : ''}`;
      $('#tb').innerHTML = rows.slice(0, LIMIT).map(([f, i]) => `<tr class="clickable" data-i="${i}">${cols.map((c) => { const v = f.properties[c[0]]; return `<td class="${typeof v === 'number' ? 'num' : ''}">${fmtVal(c[0], v)}</td>`; }).join('')}</tr>`).join('');
    };
    draw('');
    $('#tq').oninput = (e) => draw(e.target.value);
    $('#tb').onclick = (e) => {
      const tr = e.target.closest('tr'); if (!tr) return;
      const f = feats[+tr.dataset.i];
      closeModal();
      if (!live[m.id]) activate(m.id);
      flash([{ f, meta: m }], true);
    };
    $('#tcsv').onclick = () => {
      const q = (v) => '"' + key(v).replace(/"/g, '""') + '"';
      const csv = '\ufeff' + cols.map((c) => q(c[1])).join(';') + '\n' + feats.map((f) => cols.map((c) => q(f.properties[c[0]])).join(';')).join('\n');
      const a = document.createElement('a');
      a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
      a.download = m.id + '.csv'; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 2000);
    };
  }

  /* ------------------------------------------------ identifikasi objek */
  const hiLayer = L.featureGroup().addTo(map);
  function flash(hits, zoom) {
    hiLayer.clearLayers();
    hits.forEach(({ f }) => {
      const g = L.geoJSON(f, {
        pane: 'highlight', interactive: false,
        style: { color: '#22d3ee', weight: 3.5, fillColor: '#22d3ee', fillOpacity: 0.12, opacity: 1 },
        pointToLayer: (_, ll) => L.circleMarker(ll, { pane: 'highlight', radius: 13, color: '#22d3ee', weight: 3, fillOpacity: 0.1 }),
      });
      hiLayer.addLayer(g);
    });
    if (zoom && hiLayer.getBounds().isValid()) {
      const b = hiLayer.getBounds();
      if (b.getNorthEast().equals(b.getSouthWest())) map.setView(b.getCenter(), Math.max(map.getZoom(), 17));
      else map.fitBounds(b, { padding: [60, 60], maxZoom: 18 });
    }
  }
  function ringHas(ring, x, y) {
    let c = false;
    for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
      const xi = ring[i][0], yi = ring[i][1], xj = ring[j][0], yj = ring[j][1];
      if (yi > y !== yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) c = !c;
    }
    return c;
  }
  function polyHas(poly, x, y) {
    if (!ringHas(poly[0], x, y)) return false;
    for (let k = 1; k < poly.length; k++) if (ringHas(poly[k], x, y)) return false;
    return true;
  }
  function bboxOf(g) {
    let a = 1e9, b = 1e9, c = -1e9, d = -1e9;
    (function w(x) { if (typeof x[0] === 'number') { if (x[0] < a) a = x[0]; if (x[0] > c) c = x[0]; if (x[1] < b) b = x[1]; if (x[1] > d) d = x[1]; } else x.forEach(w); })(g.coordinates);
    return [a, b, c, d];
  }
  function segDist(px, py, ax, ay, bx, by) {
    const dx = bx - ax, dy = by - ay, l2 = dx * dx + dy * dy;
    let t = l2 ? ((px - ax) * dx + (py - ay) * dy) / l2 : 0; t = Math.max(0, Math.min(1, t));
    return Math.hypot(px - (ax + t * dx), py - (ay + t * dy));
  }
  function identify(ll) {
    const lat = ll.lat, lng = ll.lng, k = Math.cos((lat * Math.PI) / 180);
    const mpp = (40075016.686 * k) / (256 * 2 ** map.getZoom());
    const tolM = mpp * 10;
    const px = lng * k * 111320, py = lat * 110574;
    const out = [];
    for (let i = order.length - 1; i >= 0; i--) {
      const id = order[i], m = byId.get(id), fc = store[id];
      if (!fc || m.geom === 'raster') continue;
      const found = [];
      for (const f of fc.features) {
        const g = f.geometry; const bb = f._bb || (f._bb = bboxOf(g));
        const padLng = tolM / (111320 * k), padLat = tolM / 110574;
        if (lng < bb[0] - padLng || lng > bb[2] + padLng || lat < bb[1] - padLat || lat > bb[3] + padLat) continue;
        let hit = false;
        if (m.geom === 'poly') {
          const polys = g.type === 'Polygon' ? [g.coordinates] : g.coordinates;
          hit = polys.some((p) => polyHas(p, lng, lat));
        } else if (m.geom === 'line') {
          const lines = g.type === 'LineString' ? [g.coordinates] : g.coordinates;
          outer: for (const ln of lines) for (let s = 1; s < ln.length; s++) {
            if (segDist(px, py, ln[s - 1][0] * k * 111320, ln[s - 1][1] * 110574, ln[s][0] * k * 111320, ln[s][1] * 110574) <= tolM) { hit = true; break outer; }
          }
        } else {
          hit = Math.hypot(px - g.coordinates[0] * k * 111320, py - g.coordinates[1] * 110574) <= tolM * 1.3;
        }
        if (hit) found.push(f);
      }
      if (found.length) out.push({ meta: m, feats: found });
    }
    return out;
  }
  function popupHTML(res, bodyMax) {
    const total = res.reduce((a, r) => a + r.feats.length, 0);
    const sec = res.map((r, idx) => {
      const m = r.meta, shown = r.feats.slice(0, 5);
      const feats = shown.map((f) => {
        const cols = m.fields.length ? m.fields : Object.keys(f.properties).filter((k) => k[0] !== '_').map((k) => [k, k]);
        const rows = cols.filter((c) => f.properties[c[0]] !== undefined && f.properties[c[0]] !== '').map((c) => `<tr><td>${esc(c[1])}</td><td>${fmtVal(c[0], f.properties[c[0]])}</td></tr>`).join('');
        return `<div class="pop-feat"><table>${rows || '<tr><td colspan="2">Tidak ada atribut</td></tr>'}</table></div>`;
      }).join('');
      const first = r.feats[0], it = itemFor(m, first);
      return `<details class="pop-layer" ${idx < 3 ? 'open' : ''}><summary>${swatch(m, it)}<span>${esc(m.name)}</span><span class="c">${r.feats.length}</span></summary>${feats}${r.feats.length > shown.length ? `<div class="pop-more">+ ${r.feats.length - shown.length} objek lain di titik ini</div>` : ''}</details>`;
    }).join('');
    return `<div class="pop-head">${total} objek pada ${res.length} layer</div><div class="pop-body" style="max-height:${bodyMax}px">${sec}</div>`;
  }

  let measuring = false;
  map.on('click', (e) => {
    if (measuring) return;
    if (!order.length) { hiLayer.clearLayers(); return; }
    const res = identify(e.latlng);
    if (!res.length) { hiLayer.clearLayers(); map.closePopup(); toast('Tidak ada objek pada titik ini'); return; }
    flash(res.flatMap((r) => r.feats.slice(0, 5).map((f) => ({ f, meta: r.meta }))));
    const sz = map.getSize();
    const lg = $('#legendBox');
    const rightPad = lg.hidden ? 70 : lg.offsetWidth + 34;
    const bodyMax = Math.max(160, sz.y - 200);
    L.popup({
      maxWidth: Math.min(480, sz.x - 50), minWidth: Math.min(300, sz.x - 50), className: 'idpop', closeOnClick: false,
      autoPanPaddingTopLeft: [24, 24], autoPanPaddingBottomRight: [mobile() ? 24 : rightPad, 96],
    }).setLatLng(e.latlng).setContent(popupHTML(res, bodyMax)).openOn(map);
  });
  map.on('popupclose', () => hiLayer.clearLayers());

  /* ----------------------------------------------------- alat ukur */
  const mLayer = L.featureGroup().addTo(map);
  let mMode = 'dist', mPts = [], mDone = false;
  const R = 6371008.8;
  const rad = (d) => (d * Math.PI) / 180;
  function dist(a, b) {
    const dLat = rad(b.lat - a.lat), dLng = rad(b.lng - a.lng);
    const h = Math.sin(dLat / 2) ** 2 + Math.cos(rad(a.lat)) * Math.cos(rad(b.lat)) * Math.sin(dLng / 2) ** 2;
    return 2 * R * Math.asin(Math.sqrt(h));
  }
  function areaOf(pts) {
    if (pts.length < 3) return 0;
    let s = 0;
    for (let i = 0; i < pts.length; i++) { const p = pts[i], q = pts[(i + 1) % pts.length]; s += rad(q.lng - p.lng) * (2 + Math.sin(rad(p.lat)) + Math.sin(rad(q.lat))); }
    return Math.abs((s * R * R) / 2);
  }
  const fmtLen = (m) => (m >= 1000 ? (m / 1000).toLocaleString('id-ID', { maximumFractionDigits: 3 }) + ' km' : m.toLocaleString('id-ID', { maximumFractionDigits: 1 }) + ' m');
  function mDraw() {
    mLayer.clearLayers();
    const opt = { color: '#fbbf24', weight: 3, dashArray: '6 5', pane: 'highlight' };
    if (mMode === 'area' && mPts.length > 2) L.polygon(mPts, { ...opt, fillColor: '#fbbf24', fillOpacity: 0.2 }).addTo(mLayer);
    else if (mPts.length > 1) L.polyline(mPts, opt).addTo(mLayer);
    mPts.forEach((p) => L.circleMarker(p, { radius: 5, color: '#fff', weight: 2, fillColor: '#f59e0b', fillOpacity: 1, pane: 'highlight' }).addTo(mLayer));
    let t;
    if (!mPts.length) t = 'Klik pada peta untuk mulai mengukur.';
    else if (mMode === 'dist') {
      let d = 0; for (let i = 1; i < mPts.length; i++) d += dist(mPts[i - 1], mPts[i]);
      t = `Panjang total<br><b>${fmtLen(d)}</b><br><span class="note">${mPts.length} titik</span>`;
    } else {
      const a = areaOf(mPts); let per = 0;
      for (let i = 0; i < mPts.length; i++) per += dist(mPts[i], mPts[(i + 1) % mPts.length]);
      t = mPts.length < 3 ? 'Tambahkan minimal 3 titik.' : `Luas<br><b>${(a / 10000).toLocaleString('id-ID', { maximumFractionDigits: 2 })} ha</b> <span class="note">(${a.toLocaleString('id-ID', { maximumFractionDigits: 0 })} m²)</span><br><span class="note">Keliling ${fmtLen(per)}</span>`;
    }
    $('#mResult').innerHTML = t;
  }
  function setMeasure(on) {
    measuring = on; $('#measureBox').hidden = !on; $('#btnMeasure').classList.toggle('on', on);
    $('#map').style.cursor = on ? 'crosshair' : '';
    if (on) { map.closePopup(); hiLayer.clearLayers(); } else { mPts = []; mLayer.clearLayers(); }
    mDraw();
  }
  map.on('click', (e) => { if (!measuring) return; if (mDone) { mPts = []; mDone = false; } mPts.push(e.latlng); mDraw(); });
  map.on('dblclick', () => { if (measuring) mDone = true; });
  $('#btnMeasure').onclick = () => setMeasure(!measuring);
  $('#mClose').onclick = () => setMeasure(false);
  $('#mReset').onclick = () => { mPts = []; mDone = false; mDraw(); };
  $('#mUndo').onclick = () => { mPts.pop(); mDraw(); };
  $('#mDist').onclick = () => { mMode = 'dist'; $('#mDist').classList.add('on'); $('#mArea').classList.remove('on'); mDraw(); };
  $('#mArea').onclick = () => { mMode = 'area'; $('#mArea').classList.add('on'); $('#mDist').classList.remove('on'); mDraw(); };

  /* ------------------------------------------------ kontrol lain */
  map.on('mousemove', (e) => { $('#cLat').textContent = 'Lat ' + e.latlng.lat.toFixed(6); $('#cLng').textContent = 'Lng ' + e.latlng.lng.toFixed(6); });
  map.on('zoomend', () => { $('#cZoom').textContent = 'Zoom ' + map.getZoom(); });
  $('#cZoom').textContent = 'Zoom ' + map.getZoom();

  $('#btnHome').onclick = () => map.fitBounds(home, { padding: [20, 20] });
  $('#btnFull').onclick = () => { if (document.fullscreenElement) document.exitFullscreen(); else document.documentElement.requestFullscreen && document.documentElement.requestFullscreen(); };

  const sel = $('#desaSel');
  CAT.desa.forEach((d, i) => { const o = document.createElement('option'); o.value = i; o.textContent = 'Desa ' + d.n; sel.appendChild(o); });
  sel.onchange = async () => {
    if (sel.value === '') return;
    const d = CAT.desa[+sel.value];
    map.fitBounds(d.b, { padding: [40, 40] });
    try {
      const m = byId.get('administrasi_ar_desakel'), fc = await loadFC(m);
      const f = fc.features.find((x) => x.properties.WADMKD === d.n);
      if (f) { flash([{ f, meta: m }]); setTimeout(() => hiLayer.clearLayers(), 4500); }
    } catch (e) { /* abaikan */ }
    closeSideOnMobile();
  };

  const mobile = () => window.matchMedia('(max-width:860px)').matches;
  function setSide(open) {
    document.body.classList.toggle('side-closed', !open);
    $('#scrim').hidden = !(open && mobile());
    setTimeout(() => map.invalidateSize(), 280);
  }
  function closeSideOnMobile() { if (mobile()) setSide(false); }
  $('#btnMenu').onclick = () => setSide(document.body.classList.contains('side-closed'));
  $('#scrim').onclick = () => setSide(false);
  window.addEventListener('resize', () => map.invalidateSize());

  $('#btnAbout').onclick = () => {
    const nL = CAT.layers.filter((l) => l.geom !== 'raster').length, nR = CAT.layers.length - nL;
    openModal('Tentang WebGIS RDTR Kecamatan Slahung', `<div class="about">
      <p>WebGIS ini menampilkan seluruh data spasial penyusunan <b>Rencana Detail Tata Ruang (RDTR) Kecamatan Slahung</b>, Kabupaten Ponorogo, Provinsi Jawa Timur — meliputi peta dasar, data tematik, kebencanaan, rencana tata ruang, serta hasil analisis spasial (kesesuaian lahan, aksesibilitas, pusat pelayanan, daya dukung dan daya tampung).</p>
      <dl class="kv"><dt>Jumlah layer</dt><dd>${nL} vektor + ${nR} raster</dd><dt>Cakupan</dt><dd>22 desa/kelurahan, Kecamatan Slahung</dd><dt>Sistem koordinat</dt><dd>Data asli UTM 49S (EPSG:32749) / WGS 84 — ditampilkan di WGS 84 (EPSG:4326)</dd><dt>Basemap</dt><dd>Google Satelit (bawaan), Google Hybrid/Jalan/Medan, OpenStreetMap, Carto</dd></dl>
      <h3>Cara menggunakan</h3>
      <ul><li><b>Katalog Layer</b>: buka kelompok, centang layer untuk menampilkannya. Tombol <b>⋯</b> menampilkan deskripsi, zoom, metadata, tabel atribut, dan unduhan shapefile.</li>
      <li><b>Klik peta</b> untuk mengidentifikasi semua objek dari layer aktif pada titik tersebut.</li>
      <li><b>Layer Aktif</b>: atur urutan tumpukan dan transparansi. <b>Legenda</b> muncul otomatis di kanan bawah.</li>
      <li>Layer analisis (mis. Kesesuaian Permukiman, Aksesibilitas, Klasifikasi Desa) memiliki tab <b>Metode & Hasil Analisis</b> dan tabel rekap per desa pada menu <b>Info & Metadata</b>.</li>
      <li>Tautan peta (URL) menyimpan layer aktif, basemap, dan posisi sehingga dapat dibagikan.</li></ul>
      <h3>Catatan</h3>
      <ul><li>Beberapa layer besar disederhanakan geometrinya (±2 m) dan bintik berukuran &lt; 0,5 ha pada layer raster-vektor dihilangkan agar ringan; sel grid dengan atribut sama digabung. Data lengkap tersedia pada ZIP shapefile.</li>
      <li>Layer <i>Kepadatan Dasimetrik Grid 100 m</i> belum dapat ditampilkan karena hanya berkas <code>.shx</code> yang terunggah (berkas .shp/.dbf/.prj belum ada).</li>
      <li>Data analisis bersifat indikatif untuk penyusunan RDTR; baca bagian <i>Keterbatasan</i> pada metode tiap analisis.</li>
      <li>Basemap Google dimuat langsung dari server tile Google dan tunduk pada ketentuan layanan Google.</li></ul></div>`);
  };

  /* ----------------------------------------------------- permalink */
  let hashT;
  function syncHash() {
    clearTimeout(hashT);
    hashT = setTimeout(() => {
      const c = map.getCenter();
      const h = `#b=${baseId}&v=${c.lat.toFixed(5)},${c.lng.toFixed(5)},${map.getZoom()}&l=${order.join(',')}`;
      try { history.replaceState(null, '', h); } catch (e) { /* file:// */ }
    }, 250);
  }
  map.on('moveend', syncHash);
  function parseHash() {
    const p = {}; location.hash.replace(/^#/, '').split('&').forEach((kv) => { const i = kv.indexOf('='); if (i > 0) p[kv.slice(0, i)] = kv.slice(i + 1); });
    return p;
  }

  /* -------------------------------------------------------------- init */
  buildGroups();
  const hp = parseHash();
  setBasemap(BASEMAPS.some((b) => b.id === hp.b) ? hp.b : 'sat');
  if (hp.v) {
    const [a, b, z] = hp.v.split(',').map(Number);
    if ([a, b, z].every(Number.isFinite)) map.setView([a, b], z);
  }
  const initial = hp.l !== undefined ? hp.l.split(',').filter((x) => byId.has(x)) : CAT.layers.filter((l) => l.on).map((l) => l.id);
  (async () => {
    for (const id of initial) await activate(id);
    // buka grup yang berisi layer aktif; selain itu buka grup pertama
    const open = new Set(initial.map((id) => byId.get(id).group));
    if (!open.size) open.add(CAT.groups[0].id);
    $$('.grp', groupsEl).forEach((g) => g.classList.toggle('open', open.has(g.dataset.g)));
    refreshUI();
  })();
  if (mobile()) { setSide(false); $('#legendBox').classList.add('closed'); $('#legendHead').setAttribute('aria-expanded', 'false'); }
  requestAnimationFrame(() => setTimeout(() => $('#loader').classList.add('done'), 350));
  setTimeout(() => ($('#loader').style.display = 'none'), 1200);
})();
