# -*- coding: utf-8 -*-
"""Membangun data WebGIS dari shapefile (ZIP) di root repository.

Jalankan dari root repo:   python3 tools/build_data.py

Keluaran (folder data/):
  catalog.js              katalog layer, gaya/legenda, daftar desa
  layers/<id>.js          GeoJSON (WGS84) per layer, dibungkus agar bisa dimuat tanpa server
  raster/<id>.png         raster (DEM, hillshade, lereng) hasil reproyeksi ke WGS84
  info/<folder>.js        teks metode & tabel rekap (CSV/XLSX) per kelompok analisis

Ketergantungan: pyshp, pyproj, shapely, numpy, pillow, openpyxl
"""
import csv, glob, io, json, math, os, re, sys, tempfile, zipfile
from collections import Counter

import numpy as np
import shapefile
from PIL import Image
from pyproj import CRS, Transformer
from shapely.geometry import shape, mapping
from shapely.ops import transform as shp_transform

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import catalog as C  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data')
DEFAULT_TOL = 0.00002   # ~2 m
DEC = 5                 # ~1 m


# ------------------------------------------------------------------ utilitas
def jsdump(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':'))


def write_js(path, call, key, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f'{call}({jsdump(key)},{jsdump(obj)});')


def norm_val(v):
    """Nilai atribut -> tipe JSON ringkas (None bila kosong)."""
    if v is None:
        return None
    if isinstance(v, bytes):
        v = v.decode('utf-8', 'replace')
    if isinstance(v, float):
        if math.isnan(v):
            return None
        if v == int(v) and abs(v) < 1e12:
            return int(v)
        return round(v, 4)
    if isinstance(v, str):
        v = v.strip().replace('\x00', '')
        return v if v else None
    if hasattr(v, 'isoformat'):
        return v.isoformat()
    return v


def key_of(v):
    return '' if v is None else str(v)


def pretty(name):
    return re.sub(r'\s+', ' ', name.replace('_', ' ')).strip().title()


def label_of(field):
    return C.LABELS.get(field.upper()) or C.LABELS.get(field.upper().rstrip('_')) or pretty(field)


def round_coords(c):
    if isinstance(c[0], (int, float)):
        return [round(c[0], DEC), round(c[1], DEC)]
    return [round_coords(x) for x in c]


def clean_ring_list(coords, gtype):
    """Buang titik duplikat berurutan setelah pembulatan & ring yang rusak."""
    def dedupe(r, closed):
        out = []
        for p in r:
            if not out or p != out[-1]:
                out.append(p)
        if closed and out and out[0] != out[-1]:
            out.append(out[0])
        return out
    if gtype == 'Polygon':
        rings = [dedupe(r, True) for r in coords]
        rings = [r for r in rings if len(r) >= 4]
        return rings
    if gtype == 'LineString':
        r = dedupe(coords, False)
        return r if len(r) >= 2 else None
    return coords


def geojson_geom(g):
    m = mapping(g)
    t = m['type']
    c = round_coords(m['coordinates'])
    if t == 'Polygon':
        c = clean_ring_list(c, 'Polygon')
        return {'type': 'Polygon', 'coordinates': c} if c else None
    if t == 'MultiPolygon':
        polys = [clean_ring_list(p, 'Polygon') for p in c]
        polys = [p for p in polys if p]
        if not polys:
            return None
        return {'type': 'Polygon', 'coordinates': polys[0]} if len(polys) == 1 else {'type': 'MultiPolygon', 'coordinates': polys}
    if t == 'LineString':
        c = clean_ring_list(c, 'LineString')
        return {'type': 'LineString', 'coordinates': c} if c else None
    if t == 'MultiLineString':
        ls = [clean_ring_list(x, 'LineString') for x in c]
        ls = [x for x in ls if x]
        if not ls:
            return None
        return {'type': 'LineString', 'coordinates': ls[0]} if len(ls) == 1 else {'type': 'MultiLineString', 'coordinates': ls}
    return {'type': t, 'coordinates': c}


M2_PER_DEG2 = 111320.0 * 110574.0 * 0.99   # lintang ~8 deg LS


def drop_small(g, m2):
    """Buang bagian poligon & lubang yang lebih kecil dari m2 (bintik hasil vektorisasi raster)."""
    from shapely.geometry import Polygon, MultiPolygon
    thr = m2 / M2_PER_DEG2
    parts = list(g.geoms) if g.geom_type == 'MultiPolygon' else [g]
    out = []
    for p in parts:
        if p.area < thr:
            continue
        holes = [r for r in p.interiors if Polygon(r).area >= thr]
        out.append(Polygon(p.exterior, holes))
    if not out:
        return g.__class__()
    return out[0] if len(out) == 1 else MultiPolygon(out)


def geom_class(shape_type_name):
    n = shape_type_name.upper()
    if 'POLYGON' in n:
        return 'poly'
    if 'LINE' in n:
        return 'line'
    return 'point'


def rep_point(g):
    t = g.geom_type
    if t in ('Polygon', 'MultiPolygon'):
        p = g.representative_point()
    elif t in ('LineString', 'MultiLineString'):
        p = g.interpolate(0.5, normalized=True)
    else:
        p = g.centroid
    return round(p.x, DEC), round(p.y, DEC)


# ------------------------------------------------------------ ekstraksi ZIP
def extract_all(tmp):
    index = {}      # stem -> (folder, path.shp)
    folders = {}    # folder -> dir
    for z in sorted(glob.glob(os.path.join(ROOT, '*.zip'))):
        folder = os.path.splitext(os.path.basename(z))[0]
        d = os.path.join(tmp, folder)
        os.makedirs(d, exist_ok=True)
        with zipfile.ZipFile(z) as zf:
            zf.extractall(d)
        folders[folder] = d
        for p in glob.glob(os.path.join(d, '**', '*.shp'), recursive=True):
            index[os.path.splitext(os.path.basename(p))[0]] = (folder, p)
    return index, folders


# --------------------------------------------------------------------- gaya
def resolve_color(val, colors, idx):
    """Return dict(c=..., ...) untuk satu nilai kategori."""
    entry = None
    if isinstance(colors, dict):
        if val in colors:
            entry = colors[val]
        else:
            lv = val.lower()
            for k, v in colors.items():
                if k.lower() == lv:
                    entry = v
                    break
            if entry is None:
                for k, v in colors.items():
                    if k.lower() in lv:
                        entry = v
                        break
    elif isinstance(colors, list):
        entry = colors[idx % len(colors)]
    if entry is None:
        entry = C.QUAL[idx % len(C.QUAL)]
    return dict(c=entry) if isinstance(entry, str) else dict(entry)


def build_style(spec, counts):
    s = {k: v for k, v in spec.items() if k not in ('colors', 'order', 'labels', 'by')}
    if spec['kind'] != 'cat':
        return s
    by = spec['by']
    values = [v for v in counts]
    order = spec.get('order') or []
    colors = spec.get('colors')
    ordered = [v for v in order if v in counts]
    rest = [v for v in values if v not in ordered]
    if isinstance(colors, dict) and not order:
        ordered = [v for v in colors if v in counts]
        rest = [v for v in values if v not in ordered]

    def nat(v):
        try:
            return (0, float(v), v)
        except ValueError:
            return (1, 0, v)
    if all(nat(v)[0] == 0 for v in rest) and rest:
        rest.sort(key=nat)
    else:
        rest.sort(key=lambda v: (-counts[v], v))
    items = []
    for i, v in enumerate(ordered + rest):
        e = resolve_color(v, colors, i)
        it = dict(v=v, l=spec.get('labels', {}).get(v, v if v != '' else '(tanpa data)'), c=e['c'], n=counts[v])
        for k in ('w', 'd', 'o', 'i'):
            if k in e:
                it[k] = e[k]
        items.append(it)
    s['by'] = by
    s['items'] = items
    return s


# ------------------------------------------------------------------- vektor
def process_vector(stem, folder, shp, cfg, bounds_acc):
    r = shapefile.Reader(shp, encoding='utf-8', encodingErrors='replace')
    prj = open(shp[:-4] + '.prj', encoding='utf-8', errors='ignore').read()
    src = CRS.from_wkt(prj)
    tr = None if src.to_epsg() == 4326 else Transformer.from_crs(src, 4326, always_xy=True)
    gclass = geom_class(r.shapeTypeName)
    dbf_fields = [f[0] for f in r.fields[1:]]
    lower = {f.lower(): f for f in dbf_fields}

    want = cfg.get('fields')
    if want:
        fields = [lower[w.lower()] for w in want if w.lower() in lower]
        missing = [w for w in want if w.lower() not in lower]
        if missing:
            print(f'   ! {stem}: kolom tidak ada: {missing}')
    else:
        fields = [f for f in dbf_fields if f.upper() not in C.SKIP]
    label_f = lower.get(cfg['label'].lower()) if cfg.get('label') else None
    style_f = None
    spec = cfg['style']
    if spec['kind'] == 'cat':
        style_f = lower[spec['by'].lower()]
        spec = dict(spec, by=style_f)
    keep = list(dict.fromkeys(fields + ([style_f] if style_f else [])))

    tol = cfg.get('tol', DEFAULT_TOL)
    dis = cfg.get('dissolve_by')
    dis_only = cfg.get('dissolve_only')   # (kolom, nilai) -> hanya fitur ini yang digabung
    items = []                            # (geometri WGS84, props, kunci_gabung, label)
    fvals = {f: set() for f in keep}
    for sr in r.iterShapeRecords():
        if sr.shape.shapeType == shapefile.NULL:
            continue
        try:
            g = shape(sr.shape.__geo_interface__)
        except Exception:
            continue
        if g.is_empty:
            continue
        if tr is not None:
            g = shp_transform(lambda x, y, z=None: tr.transform(x, y), g)
        else:
            g = shp_transform(lambda x, y, z=None: (x, y), g)
        rec = sr.record.as_dict()
        props = {}
        for f in keep:
            v = norm_val(rec.get(f))
            if v is None or (not want and v in (0, '0', '-', '0.0')):
                continue
            props[f] = v
        gk = None
        if dis:
            if dis_only is None or key_of(props.get(lower[dis_only[0].lower()])) == str(dis_only[1]):
                gk = tuple(key_of(props.get(lower[d.lower()])) for d in dis)
        if gclass != 'point' and tol and not dis:
            g = g.simplify(tol, preserve_topology=True)
            if g.is_empty:
                continue
        if cfg.get('min_m2') and gclass == 'poly':
            g = drop_small(g, cfg['min_m2'])
            if g.is_empty:
                continue
        label_v = norm_val(rec.get(label_f)) if label_f else None
        items.append((g, props, gk, label_v))

    if dis:
        from shapely.ops import unary_union
        groups, out_items = {}, []
        dkeys = [lower[d.lower()] for d in dis]
        for g, props, gk, lv in items:
            if gk is None:
                out_items.append((g, props, None, lv))
            else:
                groups.setdefault(gk, []).append((g, props))
        for gk, mem in groups.items():
            u = unary_union([m[0] for m in mem])
            props = {k: v for k, v in mem[0][1].items() if k in dkeys}
            out_items.append((u, props, gk, None))
        items = out_items
        if tol:
            items = [(g.simplify(tol, preserve_topology=True), p, k, lv) for g, p, k, lv in items]

    feats, counts = [], Counter()
    minx = miny = 1e9
    maxx = maxy = -1e9
    for g, props, gk, lv in items:
        if g.is_empty:
            continue
        gj = geojson_geom(g)
        if gj is None:
            continue
        for f, v in props.items():
            fvals.setdefault(f, set()).add(v)
        if style_f:
            counts[key_of(props.get(style_f))] += 1
        if label_f and lv is not None and lv not in (0, '0', '-'):
            lx, ly = rep_point(g)
            props['_lbl'] = (str(round(lv, 1)) if isinstance(lv, float) else str(lv))
            props['_lx'], props['_ly'] = lx, ly
        b = g.bounds
        minx, miny, maxx, maxy = min(minx, b[0]), min(miny, b[1]), max(maxx, b[2]), max(maxy, b[3])
        feats.append({'type': 'Feature', 'properties': props, 'geometry': gj})
    if not feats:
        print(f'   ! {stem}: tidak ada fitur')
        return None

    # kolom yang benar-benar punya data (urutan sesuai konfigurasi)
    shown = [f for f in fields if fvals.get(f)]
    style = build_style(spec, counts) if spec['kind'] == 'cat' else dict(spec)
    style['geom'] = gclass if spec.get('geom') != 'point' or gclass == 'point' else gclass
    if spec['kind'] == 'cat' and style_f:
        style['by'] = style_f
    lid = stem.lower()
    fc = {'type': 'FeatureCollection', 'features': feats}
    path = os.path.join(OUT, 'layers', lid + '.js')
    write_js(path, '__L', lid, fc)
    bounds_acc.append((minx, miny, maxx, maxy))
    return dict(
        id=lid, file=f'data/layers/{lid}.js', n=len(feats), geom=gclass, style=style,
        fields=[[f, label_of(f)] for f in shown],
        label=bool(label_f), bounds=[[miny, minx], [maxy, maxx]],
        kb=os.path.getsize(path) // 1024, shp=stem + '.shp',
    )


# ------------------------------------------------------------------- raster
def read_geotiff(path):
    import tifffile
    t = tifffile.TiffFile(path)
    a = t.pages[0].asarray().astype('float64')
    a[a < -1e30] = np.nan
    return a


def build_rasters(folders):
    out = []
    src_tif = {
        'DEM_KONTUR25K_10M': os.path.join(folders['DEM_KONTUR25K_10M'], 'DEM_KONTUR25K_10M.tif'),
        'LERENG_PERSEN_DEM25K_10M': os.path.join(folders['KEMIRINGANLERENG_AR_RTRW'], 'LERENG_PERSEN_DEM25K_10M.tif'),
    }
    # parameter georeferensi (UTM 49S, piksel 10 m, sudut kiri-atas 536890, 9120950)
    X0, Y0, PX = 536890.0, 9120950.0, 10.0
    cache = {}
    to_utm = Transformer.from_crs(4326, 32749, always_xy=True)
    to_ll = Transformer.from_crs(32749, 4326, always_xy=True)
    for rc in C.RASTERS:
        arr = cache.get(rc['src'])
        if arr is None:
            arr = cache[rc['src']] = read_geotiff(src_tif[rc['src']])
        H, W = arr.shape
        if rc['kind'] == 'hillshade':
            z = np.where(np.isnan(arr), np.nanmean(arr), arr)
            dzdy, dzdx = np.gradient(z, PX)
            az, alt = math.radians(315), math.radians(45)
            slope = np.arctan(np.hypot(dzdx, dzdy) * 1.6)   # eksagerasi vertikal 1.6x
            aspect = np.arctan2(dzdy, -dzdx)
            hs = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect - math.pi / 2)
            hs = np.clip(hs, 0, 1)
            val = hs
        else:
            val = arr
        # grid keluaran lat/lon
        lons0, lats0 = to_ll.transform([X0, X0 + W * PX, X0, X0 + W * PX], [Y0, Y0, Y0 - H * PX, Y0 - H * PX])
        west, east, north, south = min(lons0), max(lons0), max(lats0), min(lats0)
        ow, oh = W, H
        lon = west + (np.arange(ow) + 0.5) * (east - west) / ow
        lat = north - (np.arange(oh) + 0.5) * (north - south) / oh
        LON, LAT = np.meshgrid(lon, lat)
        ux, uy = to_utm.transform(LON, LAT)
        col = np.floor((ux - X0) / PX).astype(int)
        row = np.floor((Y0 - uy) / PX).astype(int)
        ok = (col >= 0) & (col < W) & (row >= 0) & (row < H)
        res = np.full((oh, ow), np.nan)
        res[ok] = val[row[ok], col[ok]]
        rgba = np.zeros((oh, ow, 4), dtype=np.uint8)
        valid = ~np.isnan(res)
        legend = []
        if rc['kind'] == 'dem':
            stops = [(90, (27, 122, 61)), (200, (163, 201, 87)), (350, (242, 227, 148)), (550, (217, 164, 91)), (750, (167, 106, 61)), (950, (250, 250, 250))]
            xs = [s[0] for s in stops]
            for ch in range(3):
                rgba[..., ch] = np.where(valid, np.interp(np.nan_to_num(res), xs, [s[1][ch] for s in stops]), 0)
            rgba[..., 3] = np.where(valid, 255, 0)
            legend = [dict(l=f'{v} m', c='#%02x%02x%02x' % c) for v, c in stops]
            legend[0]['l'] = '≤ 90 m'
            legend[-1]['l'] = '≥ 950 m'
        elif rc['kind'] == 'slope':
            edges = [2, 5, 15, 40]
            cols = [(26, 152, 80), (145, 207, 96), (254, 224, 139), (252, 141, 89), (215, 48, 39)]
            labels = ['0–2% (datar)', '2–5% (berombak)', '5–15% (berbukit)', '15–40% (curam)', '> 40% (sangat curam)']
            cls = np.digitize(np.nan_to_num(res), edges)
            for ch in range(3):
                rgba[..., ch] = np.where(valid, np.array([c[ch] for c in cols])[cls], 0)
            rgba[..., 3] = np.where(valid, 255, 0)
            legend = [dict(l=l, c='#%02x%02x%02x' % c) for l, c in zip(labels, cols)]
        else:  # hillshade
            s = np.nan_to_num(res, nan=0.5)
            dark = np.clip((0.55 - s) / 0.55, 0, 1)
            light = np.clip((s - 0.75) / 0.25, 0, 1)
            alpha = np.maximum(dark * 0.85, light * 0.35)
            rgba[..., 0] = rgba[..., 1] = rgba[..., 2] = np.where(s > 0.75, 255, 0)
            rgba[..., 3] = np.where(valid, (alpha * 255).astype(np.uint8), 0)
            legend = [dict(l='Lereng menghadap sinar (terang)', c='#f8fafc'), dict(l='Lereng membelakangi sinar (gelap)', c='#111827')]
        path = os.path.join(OUT, 'raster', rc['id'] + '.png')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        Image.fromarray(rgba, 'RGBA').save(path, optimize=True)
        out.append(dict(id=rc['id'], name=rc['name'], group=rc['group'], desc=rc['desc'], raster=f"data/raster/{rc['id']}.png",
                        bounds=[[south, west], [north, east]], legend=legend, kb=os.path.getsize(path) // 1024,
                        shp=os.path.basename(src_tif[rc['src']]), zip=os.path.basename(os.path.dirname(src_tif[rc['src']])) + '.zip',
                        geom='raster', n=0, fields=[]))
        print(f"   raster {rc['id']}: {os.path.getsize(path)//1024} KB")
    return out


# --------------------------------------------------------- info (metode/tabel)
def num_or_text(s):
    s = s.strip()
    if re.fullmatch(r'-?\d+(,\d+)?', s):
        return float(s.replace(',', '.'))
    return s


TITLE_FIX = [('Kesesuaianpermukiman', 'Kesesuaian Permukiman'), ('Kesesuaianpangan', 'Kesesuaian Pangan'),
             ('Lahantersedia', 'Lahan Tersedia'), ('Rawanbanjir', 'Rawan Banjir'), ('Rawanlongsor', 'Rawan Longsor'),
             ('Fungsikawasan', 'Fungsi Kawasan'), ('Risikobencana', 'Risiko Bencana'), (' Per ', ' per '), ('Nni', 'NNI')]


def table_title(fn):
    t = os.path.splitext(fn)[0].replace('_', ' ').strip().title()
    for a, b in TITLE_FIX:
        t = t.replace(a, b)
    return t


def xlsx_tables(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    texts, tables = [], []
    for ws in wb:
        rows = [[norm_val(c) for c in r] for r in ws.iter_rows(values_only=True)]
        rows = [r for r in rows if any(c is not None for c in r)]
        if not rows:
            continue
        maxc = max(sum(1 for c in r if c is not None) for r in rows)
        if maxc <= 1:
            texts.append(f'[{ws.title}]\n' + '\n'.join(str(r[0]) for r in rows if r[0] is not None))
            continue
        hi = next(i for i, r in enumerate(rows) if sum(1 for c in r if c is not None) >= max(2, int(maxc * 0.6)))
        head = [('' if c is None else str(c)) for c in rows[hi]]
        width = max(i for i, c in enumerate(rows[hi]) if c is not None) + 1
        body = [['' if c is None else c for c in r[:width]] for r in rows[hi + 1:]]
        note = ' '.join(str(c) for r in rows[:hi] for c in r if c is not None)
        tables.append(dict(title=ws.title.replace('_', ' '), note=note, cols=head[:width], rows=body))
    return texts, tables


def build_info(folders):
    info = {}
    for folder, d in folders.items():
        texts, tables = [], []
        for f in sorted(os.listdir(d)):
            p = os.path.join(d, f)
            if f.upper().startswith('METODE') and f.endswith('.txt'):
                texts.insert(0, open(p, encoding='utf-8-sig', errors='replace').read().strip())
            elif f.endswith('.txt'):
                texts.append(open(p, encoding='utf-8-sig', errors='replace').read().strip())
            elif f.endswith('.csv'):
                with open(p, encoding='utf-8-sig', errors='replace', newline='') as fh:
                    rows = list(csv.reader(fh, delimiter=';'))
                if rows:
                    tables.append(dict(title=table_title(f), cols=rows[0], rows=[[num_or_text(c) for c in r] for r in rows[1:]]))
            elif f.endswith('.xlsx'):
                tx, tb = xlsx_tables(p)
                texts += tx
                tables += tb
        if texts or tables:
            info[folder] = dict(text='\n\n'.join(texts), tables=tables)
            write_js(os.path.join(OUT, 'info', folder + '.js'), '__I', folder, info[folder])
    return info


# ---------------------------------------------------------------------- main
def main():
    import shutil
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    with tempfile.TemporaryDirectory(prefix='rdtr_') as tmp:
        index, folders = extract_all(tmp)
        unknown = sorted(set(index) - set(C.LAYERS))
        missing = sorted(set(C.LAYERS) - set(index))
        if unknown:
            print('Shapefile belum terdaftar di katalog:', unknown)
        if missing:
            print('Terdaftar tetapi tidak ditemukan:', missing)
        info = build_info(folders)
        layers, allb = [], []
        gorder = {g[0]: i for i, g in enumerate(C.GROUPS)}
        for stem, cfg in C.LAYERS.items():
            if stem not in index:
                continue
            folder, shp = index[stem]
            print(f'-> {stem}')
            rec = process_vector(stem, folder, shp, cfg, allb)
            if rec is None:
                continue
            rec.update(name=cfg['name'], group=cfg['group'], zip=folder + '.zip', folder=folder,
                       desc=cfg.get('desc', ''), on=bool(cfg.get('on')), info=folder if folder in info else None)
            layers.append(rec)
        rasters = build_rasters(folders)
        for rr in rasters:
            rr['folder'] = rr['zip'][:-4]
            rr['on'] = False
            rr['info'] = rr['folder'] if rr['folder'] in info else None
        # daftar desa untuk fitur "Zoom ke desa"
        desa = []
        r = shapefile.Reader(index['ADMINISTRASI_AR_DESAKEL'][1], encoding='utf-8')
        prj = open(index['ADMINISTRASI_AR_DESAKEL'][1][:-4] + '.prj', encoding='utf-8', errors='ignore').read()
        tr = Transformer.from_crs(CRS.from_wkt(prj), 4326, always_xy=True)
        for sr in r.iterShapeRecords():
            b = sr.shape.bbox
            x0, y0 = tr.transform(b[0], b[1])
            x1, y1 = tr.transform(b[2], b[3])
            desa.append(dict(n=sr.record['WADMKD'], b=[[round(y0, 5), round(x0, 5)], [round(y1, 5), round(x1, 5)]]))
        desa.sort(key=lambda d: d['n'])
        layers.sort(key=lambda l: (gorder[l['group']], list(C.LAYERS).index(l['shp'][:-4])))
        allr = layers + rasters
        cat = dict(
            title='WebGIS RDTR Kecamatan Slahung', groups=[dict(id=g[0], name=g[1], color=g[2], icon=g[3]) for g in C.GROUPS],
            layers=allr, desa=sorted(desa, key=lambda d: d['n']),
            bounds=[[min(b[1] for b in allb), min(b[0] for b in allb)], [max(b[3] for b in allb), max(b[2] for b in allb)]],
        )
        # batas Slahung: pakai kecamatan
        kec = next(l for l in layers if l['id'] == 'administrasi_ar_kecamatan')
        cat['bounds'] = kec['bounds']
        with open(os.path.join(OUT, 'catalog.js'), 'w', encoding='utf-8') as f:
            f.write('window.CATALOG=' + jsdump(cat) + ';')
        tot = sum(l['kb'] for l in allr)
        print(f'\nSelesai: {len(layers)} layer vektor, {len(rasters)} raster, {tot/1024:.1f} MB total')


if __name__ == '__main__':
    main()
