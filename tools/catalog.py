# -*- coding: utf-8 -*-
"""Katalog layer WebGIS RDTR Slahung: nama tampilan, pengelompokan, dan simbologi.

Kunci setiap layer = nama file shapefile (tanpa ekstensi) di dalam ZIP pada root repository.
Dipakai oleh tools/build_data.py.
"""

# ---------------------------------------------------------------- palet warna
RISK5 = {'Sangat Rendah': '#2e8b57', 'Rendah': '#9ccc3c', 'Sedang': '#ffe14d',
         'Tinggi': '#f7931e', 'Sangat Tinggi': '#d7263d'}
SUIT = {'S1 - Sangat sesuai': '#1a9850', 'S2 - Sesuai': '#a6d96a',
        'S3 - Sesuai marginal': '#fee08b', 'N - Tidak sesuai': '#f46d43',
        'N - Kendala mutlak': '#a50026',
        'Tidak dievaluasi (terbangun/badan air)': '#bdbdbd'}
QUAL = ['#4e79a7', '#f28e2b', '#59a14f', '#e15759', '#b07aa1', '#76b7b2', '#edc948',
        '#ff9da7', '#9c755f', '#bab0ac', '#2f6f8f', '#c9792b', '#7aa33f', '#a64b64',
        '#6f6bb5', '#3a9d8f', '#d4a017', '#8c564b']
LC = {  # penutup/penggunaan lahan
    'badan air': '#3b8ed0', 'sungai': '#3b8ed0', 'hutan': '#1b6b3a', 'hutan rimba': '#1b6b3a',
    'hutan sejenis': '#3f8f4f', 'lahan terbangun': '#d9534f', 'terbangun': '#d9534f',
    'tegalan': '#e0b84c', 'ladang': '#e0b84c', 'perkebunan': '#8e6b3e', 'kebun': '#8e6b3e',
    'sawah': '#9bd36a', 'semak': '#9aa86b', 'rumput': '#c5d86d', 'tanah terbuka': '#cfc3a5',
    'kampung': '#e57373', 'permukiman': '#e57373',
}

GROUPS = [
    ('admin',   'Batas Administrasi',                    '#e11d48', '🗺️'),
    ('dasar',   'Peta Dasar & Topografi',                '#a16207', '⛰️'),
    ('hidro',   'Hidrologi & Air Tanah',                 '#0284c7', '💧'),
    ('infra',   'Transportasi & Infrastruktur',          '#475569', '🛣️'),
    ('sarana',  'Permukiman & Sarana Prasarana',         '#c2410c', '🏘️'),
    ('lahan',   'Penggunaan & Tutupan Lahan',            '#15803d', '🌾'),
    ('fisik',   'Kondisi Fisik & Sumber Daya Alam',      '#7c3aed', '🪨'),
    ('bencana', 'Kebencanaan (Data Sektoral)',           '#dc2626', '⚠️'),
    ('hutan',   'Kawasan Hutan, Perizinan & Pertanahan', '#166534', '🌲'),
    ('rtr',     'Rencana Tata Ruang & Program',          '#0f766e', '📐'),
    ('a_lahan', 'Analisis RDTR: Kesesuaian Lahan',       '#2563eb', '🧭'),
    ('a_akses', 'Analisis RDTR: Aksesibilitas',          '#2563eb', '🚗'),
    ('a_pusat', 'Analisis RDTR: Pusat Pelayanan & Desa', '#2563eb', '📍'),
    ('a_bnc',   'Analisis RDTR: Kebencanaan',            '#2563eb', '🛟'),
    ('d3tlh',   'Daya Dukung & Daya Tampung (D3TLH)',    '#9333ea', '⚖️'),
    ('raster',  'Citra & Raster',                        '#b45309', '🛰️'),
]

# ------------------------------------------------------------ label atribut
LABELS = {
    'NAMOBJ': 'Nama Objek', 'NAMAOBJ': 'Nama Objek', 'REMARK': 'Keterangan', 'WADMKD': 'Desa/Kelurahan',
    'WADMKC': 'Kecamatan', 'WADMKK': 'Kabupaten', 'WADMPR': 'Provinsi', 'LUAS_HA': 'Luas (ha)',
    'LUASWH': 'Luas Wilayah', 'KODE': 'Kode', 'KELAS': 'Kelas', 'NAMA': 'Klasifikasi',
    'ARAHAN': 'Arahan Pemanfaatan', 'KDPKAB': 'Kode Kab/Kota', 'KDPPUM': 'Kode Provinsi',
    'KDCPUM': 'Kode Kecamatan', 'KDEBPS': 'Kode Desa (BPS)', 'KDBBPS': 'Kode Kab/Kota (BPS)',
    'UUPP': 'Dasar Hukum', 'STATUS': 'Status', 'TIPADM': 'Tipe Administrasi', 'DESA': 'Desa',
    'DESA_': 'Desa', 'KATEGORI': 'Kategori', 'BOBOT': 'Bobot Skala Pelayanan', 'SUMBER': 'Sumber Data',
    'ELEVAS': 'Elevasi (m)', 'VALKNT': 'Ketinggian Kontur (m)', 'JNSKNT': 'Kode Jenis Kontur',
    'PEND25': 'Penduduk 2025 (jiwa)', 'LUAS_BPS': 'Luas BPS (km²)', 'KPDT_BPS': 'Kepadatan BPS (jiwa/km²)',
    'R_2325': 'Laju Pertumbuhan 2023–2025 (%/th)', 'KLS_DESA': 'Klasifikasi Desa (Swasembada/Swakarya)',
    'IDM25': 'Status IDM 2025', 'MKM_HA': 'Luas Permukiman (ha)', 'KPDT_NET': 'Kepadatan Netto (jiwa/ha permukiman)',
    'SK_PADAT': 'Skor Kepadatan', 'SISA_MIN': 'Sisa Skor Minimum', 'KLS_BPS20': 'Klasifikasi BPS 2020',
    'PUSAT_RTRW': 'Pusat Pelayanan (RTRW)', 'ORDE_SKALO': 'Orde Skalogram', 'N_KEG': 'Jumlah Titik Kegiatan',
    'WAKTU_WP': 'Waktu ke Pusat WP (menit)', 'TIPOLOGI': 'Tipologi Desa', 'KAND_INTI': 'Kandidat Inti Perkotaan',
    'JML_JENIS': 'Jumlah Jenis Fasilitas', 'TOTAL_UNIT': 'Total Unit Fasilitas', 'IDX_SENTR': 'Indeks Sentralitas',
    'ORDE': 'Orde Desa', 'BOBOT_KEG': 'Bobot Kegiatan', 'LQ': 'Location Quotient (LQ)', 'LQ_NILAI': 'Skor LQ',
    'SOURCE_ID': 'ID Sel', 'W_SUM': 'Jumlah Bobot Kegiatan', 'GIZSCORE': 'Z-Score Gi*', 'GIPVALUE': 'P-Value Gi*',
    'NNEIGHBORS': 'Jumlah Tetangga', 'GI_BIN': 'Kelas Gi*', 'G_NILAI': 'Skor Gi*',
    'T_PUSATWP': 'Waktu ke Pusat WP (menit)', 'T_PPL': 'Waktu ke PPL (menit)', 'T_BUPATI': 'Waktu ke Kantor Bupati (menit)',
    'HANSEN_B1': 'Indeks Hansen (b=1)', 'HANSEN_B2': 'Indeks Hansen (b=2)', 'KRPT_JLN': 'Kerapatan Jalan (km/km²)',
    'SKA_TWP': 'Waktu ke Pusat WP – Skenario A', 'SKB_TWP': 'Waktu ke Pusat WP – Skenario B',
    'SKB_STATUS': 'Status Skenario B (Ruas Terputus)', 'FUNGSI': 'Fungsi Jalan', 'SKENARIO': 'Skenario',
    'PANJANG_M': 'Panjang (m)', 'KENDALA': 'Kode Kendala', 'KET_KDL': 'Jenis Kendala', 'LBS': 'Masuk Lahan Baku Sawah',
    'SAWAH_EKS': 'Sawah Eksisting', 'R_LONGSOR': 'Kelas Longsor', 'R_BANJIR': 'Kelas Banjir',
    'K_MODEL': 'Kelas Model Longsor', 'K_ZKGT': 'Kelas ZKGT (PVMBG)', 'KECAMATAN': 'Kecamatan', 'HECTARES': 'Luas (ha)',
    'GENESIS': 'Bentang Lahan (Genesis)', 'XVEG_OK': 'Vegetasi Alami', 'KLS_PNTNG': 'Kelas Prioritas Jasa Ekosistem',
    'KBA_250': 'Bentang Alam (1:250.000)', 'KVA_250': 'Vegetasi Alami (1:250.000)', 'KLS_P1': 'Kelas Jasa Ekosistem P1',
    'KLS_P2': 'Kelas Jasa Ekosistem P2 (Penyediaan Air)', 'IJLH_P2': 'Indeks Jasa Ekosistem P2', 'N_AIR': 'Nilai Air (m³/th)',
    'SUNGAI': 'Sungai Acuan', 'DEBIT': 'Debit (m³/th)', 'KET': 'Status Daya Dukung', 'KETERANGAN': 'Keterangan',
    'KET21': 'Status Daya Dukung 2021', 'JPD24': 'Jumlah Penduduk 2024', 'JPD29': 'Proyeksi Penduduk 2029',
    'JPD22': 'Jumlah Penduduk 2022', 'JPD21': 'Jumlah Penduduk 2021', 'L_GRID': 'Luas Grid (ha)', 'BBT_PL': 'Bobot Penutup Lahan',
    'PIJ': 'Pij', 'KBI': 'Kebutuhan Pangan (Kbi)', 'HA': 'Luas (ha)', 'L_PL': 'Penutup Lahan',
    'SKLKP': 'Kemampuan: Kemudahan Dikerjakan', 'NKP': 'Nilai Kemudahan Dikerjakan', 'SKLLM': 'Kemampuan: Lereng', 'SKLER': 'Kemampuan: Erosi',
    'SKLKA': 'Kemampuan: Ketersediaan Air', 'SKLKD': 'Kemampuan: Kestabilan Lereng/Pondasi', 'SKLMORF': 'Kemampuan: Morfologi',
    'SKLBC': 'Kemampuan: Bencana Alam', 'SKLDR': 'Kemampuan: Drainase', 'KELASKL': 'Kelas Kemampuan Lahan',
    'KLASFSKL': 'Klasifikasi Kemampuan Pengembangan', 'SLOPE': 'Kelas Lereng', 'TOPOGRAFI': 'Ketinggian (mdpl)',
    'SYMBOLS': 'Simbol', 'NAME': 'Nama Formasi', 'FORMATION': 'Formasi (EN)', 'CLASS_LITH': 'Klasifikasi Litologi',
    'T_CLASS_EN': 'Lingkungan Pengendapan', 'B_CLASS_EN': 'Lingkungan Pengendapan (Dasar)', 'SIMOBJ': 'Simbol',
    'UMUROBJ': 'Umur Geologi', 'FAOSOIL': 'Kode FAO', 'DOMSOI': 'Kode Dominan', 'KET_': 'Keterangan',
    'LITOLOGI': 'Litologi', 'KELULUSAN': 'Kelulusan Air', 'UMUR': 'Umur', 'DESKRIPSI': 'Deskripsi',
    'SYS_AQ': 'Sistem Akuifer', 'PROD': 'Produktivitas Akuifer', 'KETERUSAN': 'Keterusan', 'DEBIT_': 'Debit',
    'KLS_NRCAIR': 'Kelas Neraca Air', 'KLS_IPA': 'Kelas Indeks Penggunaan Air', 'KLS_KTRS': 'Kelas Ketersediaan',
    'NAMA_WS': 'Wilayah Sungai', 'NAMA_WD': 'Wilayah Sungai Detail', 'KTRS_AIR': 'Ketersediaan Air (juta m³/th)',
    'KBTH_AIR': 'Kebutuhan Air (juta m³/th)', 'NRC_AIR': 'Neraca Air', 'IPA': 'Indeks Penggunaan Air',
    'THN_DAT': 'Tahun Data', 'POPULASI': 'Populasi', 'CRHHJN': 'Curah Hujan Tahunan', 'POENAG': 'Potensi Energi Angin',
    'POENMT': 'Potensi Energi Surya', 'KLAS_EROSI': 'Kelas Erosi', 'BPDASHL': 'BPDAS', 'KELAS_': 'Kelas',
    'ZONA': 'Zona Kerentanan Gerakan Tanah', 'KLSGTN': 'Kode Kelas Gerakan Tanah', 'TAHUN': 'Tahun',
    'KRBID': 'ID KRB', 'GRIDCODE': 'Kode Kelas', 'BANJIR': 'Kelas Bahaya Banjir', 'GEMPABUMI': 'Kelas Bahaya Gempabumi',
    'GUNUNGAPI': 'Kelas Bahaya Gunungapi', 'LIFUEKFASI': 'Kelas Bahaya Likuefaksi', 'KERENTANAN': 'Kelas Kerentanan',
    'FUNGSITAP': 'Kode Fungsi Kawasan Hutan', 'NKWS': 'Nama Kawasan Hutan', 'NOSKTAP': 'Nomor SK Penetapan',
    'TGLSKTAP': 'Tanggal SK Penetapan', 'KRITERIA': 'Kriteria', 'PIPPIB': 'Keterangan PIPPIB',
    'SKEMA': 'Skema (Tata Ruang/Kawasan Hutan)', 'KODE_TIPOL': 'Kode Tipologi', 'TIPOLOGI': 'Tipologi',
    'KTGR_KTDSN': 'Kategori Ketidaksesuaian', 'DSR_HUKUM': 'Dasar Hukum', 'LUAS_PITTI': 'Luas PITTI (ha)',
    'OPRBLK': 'Operator Blok', 'EFFDAT': 'Berlaku Sejak', 'EXPDAT': 'Berakhir', 'RTRKAW': 'Kode Kawasan',
    'RTRPKK': 'Pola Ruang Kabupaten', 'RTRPPR': 'Pola Ruang Provinsi', 'RTRSYS': 'Pola Ruang', 'RTRPNS': 'Pola Ruang Nasional',
    'NOTHPD': 'Dasar Hukum (Perda)', 'NOTHPP': 'Dasar Hukum (PP)', 'NOTHPR': 'Dasar Hukum', 'JNSRPR': 'Jenis Rencana Pola Ruang',
    'JNSRSR': 'Jenis Rencana Struktur Ruang', 'JENIS': 'Jenis', 'SERVICE': 'Layanan', 'FREKUENSI': 'Frekuensi',
    'LOW_LIMIT': 'Batas Bawah', 'UPP_LIMIT': 'Batas Atas', 'STAT_RCN': 'Status Rencana', 'DMN_RCN': 'Dimensi Pembangunan',
    'PRIO_RCN': 'Prioritas Nasional', 'KET_RCN': 'Keterangan Rencana', 'THN_RCN': 'Tahun Rencana', 'TRG_RCN': 'Tahun Target',
    'PLKSN_RCN': 'Pelaksana', 'NAMA_RCN': 'Nama Rencana', 'RUAS_PROV': 'Ruas Jalan Provinsi', 'DIMENSI': 'Dimensi',
    'PRIORITAS': 'Prioritas', 'TAHUN_': 'Tahun', 'TARGET': 'Target', 'PELAKSANA': 'Pelaksana',
    'NAMRJL': 'Nama Ruas Jalan', 'TOLRJL': 'Kode Jalan Tol', 'STARJL': 'Kode Status Jalan',
    'PTNOBJNAME': 'Penggunaan Tanah', 'PTNSBJNAME': 'Subjek Penggunaan Tanah', 'IG25K_PENG': 'Luas (m²)',
    'KETERANGAN_': 'Keterangan', 'ID_PL_PERU': 'ID Penutupan Lahan', 'PL_AWAL': 'Tahun Awal', 'PL_AKHIR': 'Tahun Akhir',
    'Q_NAME19': 'Penggunaan Lahan (2019)', 'LUAS_POLYG': 'Luas Poligon', 'JNSPDG': 'Kode Jenis Padang',
    'JNSSWH': 'Kode Jenis Sawah', 'JNSSLK': 'Kode Jenis Ladang', 'JNSSMK': 'Kode Jenis Semak',
    'JNSKBNSMS': 'Kode Jenis Kebun (Semusim)', 'JNSKBNTHN': 'Kode Jenis Kebun (Tahunan)',
    'FTYPE': 'Tipe Fitur', 'KLSTPN': 'Kelas Toponimi', 'NAMLOK': 'Nama Lokal', 'KOORDX': 'Koordinat X (Bujur)',
    'KOORDY': 'Koordinat Y (Lintang)', 'PJGJAR': 'Panjang Jaringan (km)', 'REGPLN': 'Region PLN',
    'JNKPOS': 'Kode Jenis Kantor Pos', 'JPLYRS': 'Kode Jenis Pelayanan RS', 'TIPRST': 'Kode Tipe RS',
    'KDLNTI': 'Kode Lantai', 'JMLBTG': 'Jumlah Bentang', 'LAYER': 'Layer Sumber', 'FGSFNP': 'Kode Fungsi Pemerintahan',
    'FGSPRP': 'Kode Fungsi Peribadatan', 'JNSPDK': 'Kode Jenis Pendidikan', 'SRNPDG': 'Kode Sarana Perdagangan',
    'FGSUSH': 'Kode Fungsi Usaha', 'TPP': 'Kode Tipe Pemakaman', 'JKK': 'Jumlah KK', 'JMLHUNI': 'Jumlah Hunian',
    'LKONOF': 'Lokasi Konstruksi', 'DAYA': 'Daya', 'PSSKBL': 'Posisi Kabel', 'JENISPTHN': 'Jenis Patahan',
    'PJGPTHN': 'Panjang Patahan (km)', 'LOKASI': 'Lokasi', 'GEOLOGI': 'Geologi', 'SJRHGEMPA': 'Sejarah Gempa',
    'KLSSTR': 'Kelas Struktur', 'JNSKOM': 'Jenis Komoditas', 'LBUNSUR': 'Lambang Unsur', 'KELLGM': 'Kelompok Logam',
    'LOKASILGM': 'Lokasi', 'STATDIKLGM': 'Status Penyelidikan', 'JNSKOMBL': 'Jenis Komoditas', 'LBUNSURBL': 'Lambang Unsur',
    'KELKOMBL': 'Kelompok Komoditas', 'LOKASIBL': 'Lokasi', 'STATDIKBL': 'Status Penyelidikan', 'ACUAN': 'Acuan',
    'STATUS_': 'Status', 'NM_INF': 'Nama Informasi', 'KD_INF': 'Kode Informasi', 'NAMA_BALAI': 'Balai',
    'NAMA_DAS': 'DAS', 'DESA_': 'Desa', 'KECAMATAN_': 'Kecamatan', 'KABUPATEN': 'Kabupaten', 'PROVINSI': 'Provinsi',
    'JNS_SUMUR': 'Jenis Sumur', 'NM_SUMUR': 'Nama Sumur', 'KELEMBAGAA': 'Kelembagaan', 'KDLM_AT': 'Kedalaman Air Tanah (m)',
    'Q1': 'Q1', 'Q2': 'Q2', 'AREA': 'Luas Area', 'LUAS': 'Luas', 'PROVINSI_': 'Provinsi',
    'NSLOPE': 'Nilai Lereng', 'NTOPOGRAFI': 'Nilai Topografi', 'NKP_': '', 'KETERANGAN__': '',
    'IJLH_C1': 'Indeks Jasa Budaya C1', 'KLS_C1': 'Kelas Jasa Budaya C1',
}

# kolom teknis yang tidak ditampilkan di popup
SKIP = {'METADATA', 'SRS_ID', 'FCODE', 'LCODE', 'RULEID', 'RULEID_1', 'RULEID_KSP', 'OBJECTID_1', 'OBJECTID',
        'ORIG_FID', 'FID_', 'SHAPE_LENG', 'SHAPE_AREA', 'SHAPE_LE_1', 'SHAPE_LE_2', 'SHAPE_LEN', 'ID',
        'KOORD_X', 'KOORD_Y', 'LAT', 'LON'}


# ---------------------------------------------------------------- helper gaya
def _risk(levels, colors=None):
    c = colors or RISK5
    return {l: c[l.replace('Kerawanan ', '').replace('Kerentanan ', '').replace('Risiko ', '')] for l in levels}


def poly(fill, op=0.55, stroke=None, w=1):
    return dict(kind='single', geom='poly', fill=fill, op=op, stroke=stroke or fill, w=w)


def outline(color, w=2, dash=None, op=0.0):
    return dict(kind='single', geom='poly', fill=color, op=op, stroke=color, w=w, dash=dash)


def line(color, w=2, dash=None):
    return dict(kind='single', geom='line', stroke=color, w=w, dash=dash)


def dot(color, r=5, icon=None):
    return dict(kind='single', geom='point', fill=color, r=r, icon=icon)


def cat(by, geom='poly', colors=None, op=0.6, w=0.8, stroke='#ffffff', order=None, labels=None, **kw):
    """colors: dict nilai->warna | list (palet) | None (palet kualitatif otomatis)."""
    return dict(kind='cat', geom=geom, by=by, colors=colors, op=op, w=w, stroke=stroke, order=order,
                labels=labels or {}, **kw)


# ------------------------------------------------------------------- katalog
# key: (grup, nama tampilan, gaya, opsi)
# opsi: fields=[...] (urutan kolom popup), label='KOLOM', tol=toleransi simplifikasi (derajat),
#       on=True (aktif saat dibuka), desc='deskripsi', folder_info=kunci METODE
def _r(prefix, lv):
    return {f'{prefix} {l}': RISK5[l] for l in lv}


LAYERS = {}

def add(stem, group, name, style, **opt):
    LAYERS[stem] = dict(group=group, name=name, style=style, **opt)


# ---- Batas administrasi
add('ADMINISTRASI_AR_DESAKEL', 'admin', 'Batas Desa/Kelurahan', outline('#fde047', 2.2), label='WADMKD', on=True,
    fields=['WADMKD', 'WADMKC', 'WADMKK', 'WADMPR', 'LUAS_HA', 'KDEBPS', 'KDCPUM', 'Status'],
    desc='Batas wilayah administrasi 22 desa/kelurahan di Kecamatan Slahung (hasil kesepakatan batas).')
add('ADMINISTRASI_AR_DESAKEL_25K', 'admin', 'Batas Desa/Kelurahan (RBI 1:25.000)', outline('#fb7185', 1.6, '6 4'), label='WADMKD',
    desc='Batas desa/kelurahan pada Rupabumi Indonesia skala 1:25.000.')
add('ADMINISTRASI_AR_KECAMATAN', 'admin', 'Batas Kecamatan Slahung', outline('#c084fc', 3.2), on=True,
    desc='Batas Kecamatan Slahung, Kabupaten Ponorogo.')
add('ADMINISTRASI_AR_KECAMATAN_25K', 'admin', 'Batas Kecamatan (RBI 1:25.000)', outline('#a855f7', 2, '8 5'))
add('ADMINISTRASI_AR_KECAMATAN_SATUPETA', 'admin', 'Batas Kecamatan (Satu Peta)', outline('#8b5cf6', 2, '3 5'))
add('ADMINISTRASI_AR_KABKOTA_25K', 'admin', 'Batas Kabupaten Ponorogo (RBI 1:25.000)', outline('#2dd4bf', 3))
add('ADMINISTRASI_AR_KABKOTA_50K', 'admin', 'Batas Kabupaten Ponorogo (1:50.000)', outline('#14b8a6', 2.4, '8 5'))
add('ADMINISTRASI_AR_KABKOTA_SATUPETA', 'admin', 'Batas Kabupaten Ponorogo (Satu Peta)', outline('#0d9488', 2, '3 5'))
add('ADMINISTRASI_LN', 'admin', 'Garis Batas Desa/Kelurahan', line('#f97316', 1.6, '5 3'),
    desc='Segmen garis batas antar desa/kelurahan beserta pasangan wilayah yang berbatasan.')
add('ADMINISTRASI_LN_KABKOTA_25K', 'admin', 'Garis Batas Kabupaten (RBI 1:25.000)', line('#22d3ee', 3, '10 5'))
add('ADMINISTRASI_LN_KABKOTA_SATUPETA', 'admin', 'Garis Batas Kabupaten (Satu Peta)', line('#06b6d4', 2.4, '4 4'))

# ---- Peta dasar & topografi
add('TOPONIMI_PT_25K', 'dasar', 'Toponimi (Nama Rupabumi)', cat('REMARK', 'point', colors={'Desa': '#f59e0b', 'Kecamatan': '#ef4444', 'Kelurahan': '#f59e0b'}, r=4, label_zoom=15,
                                              labels={'': 'Nama rupabumi lainnya'}),
    label='NAMOBJ', fields=['NAMOBJ', 'REMARK', 'FTYPE', 'KLSTPN', 'NAMLOK', 'KOORDX', 'KOORDY'],
    desc='Nama-nama rupabumi (desa, permukiman, puncak, alur sungai) dari RBI 1:25.000.')
add('KONTUR_LN_25K', 'dasar', 'Garis Kontur (interval 12,5 m)', dict(kind='contour', geom='line', stroke='#b45309', w=0.8),
    fields=['VALKNT'], tol=0.00002, desc='Garis kontur RBI 1:25.000. Kontur indeks (kelipatan 50 m) ditebalkan.')
add('SPOTHEIGHT_PT_25K', 'dasar', 'Titik Tinggi (Spot Height)', dot('#fbbf24', 3), label='ELEVAS',
    fields=['ELEVAS', 'NAMOBJ'])
add('TOPOGRAFI_AR_RTRW', 'dasar', 'Ketinggian Tempat (Topografi)', cat('Topografi', colors=['#86efac', '#fde047']),
    fields=['Topografi', 'NTopografi'], tol=0.00008)
add('KEMIRINGANLERENG_AR_RTRW', 'dasar', 'Kelas Kemiringan Lereng',
    cat('Slope', colors={'0-2%': '#1a9850', '2-5%': '#91cf60', '5-15%': '#fee08b', '15-40%': '#fc8d59', '>40%': '#d73027'},
        labels={'0-2%': 'Datar (0–2%)', '2-5%': 'Berombak (2–5%)', '5-15%': 'Berbukit (5–15%)', '15-40%': 'Curam (15–40%)', '>40%': 'Sangat Curam (>40%)'}),
    fields=['Slope', 'Keterangan'], tol=0.00008, min_m2=5000,
    desc='Kelas lereng hasil vektorisasi DEM 10 m; bintik < 0,5 ha dihilangkan agar ringan.')

# ---- Hidrologi & air tanah
add('SUNGAI_LN_25K', 'hidro', 'Jaringan Sungai', cat('REMARK', 'line', colors={'Sungai': '#38bdf8', 'Sungai Satu Garis': '#38bdf8', 'Alur Sungai': '#7dd3fc'}, w=1.6),
    label='NAMOBJ', fields=['NAMOBJ', 'REMARK'], desc='Jaringan sungai/alur sungai RBI 1:25.000.')
add('SUNGAI_AR_25K', 'hidro', 'Badan Sungai (Area)', poly('#38bdf8', 0.7))
add('AIRTANAH_PT_SATUPETA', 'hidro', 'Sumur Air Tanah', dot('#0ea5e9', 7, '💧'),
    fields=['nm_sumur', 'nm_inf', 'desa', 'kecamatan', 'kabupaten', 'jns_sumur', 'jns_pom', 'thn_buat', 'kdlm_at', 'dbt_air_ba', 'irigasi', 'pjn_pipa', 'kelembagaa', 'keterangan', 'thn_dat', 'nama_balai', 'nama_ws'],
    desc='Sumur air tanah (JIAT) hasil inventarisasi BBWS Bengawan Solo.')
add('CAT_AR_250K', 'hidro', 'Cekungan Air Tanah (CAT)', poly('#0ea5e9', 0.4), fields=['namobj', 'lokasi', 'area', 'q1', 'q2'])
add('HIDROGEOLOGI_LITOLOGI_AR_SATUPETA', 'hidro', 'Hidrogeologi: Litologi & Kelulusan Air',
    cat('kelulusan'), fields=['litologi', 'kelulusan', 'deskripsi', 'umur'], tol=0.00005)
add('HIDROGEOLOGI_PRODUKTIVITAS_AR_SATUPETA', 'hidro', 'Hidrogeologi: Produktivitas Akuifer',
    cat('prod'), fields=['prod', 'sys_aq', 'keterusan', 'debit'], tol=0.00005)
add('KETERSEDIAANAIR_AR_SATUPETA', 'hidro', 'Ketersediaan Air (Wilayah Sungai)',
    cat('nm_inf'), fields=['nm_inf', 'nama_ws', 'kls_nrcair', 'kls_ipa', 'kls_ktrs', 'ktrs_air', 'kbth_air', 'nrc_air', 'ipa', 'rki', 'populasi', 'thn_dat'], tol=0.00005)
add('NERACASDA_AR_50K', 'hidro', 'Neraca Sumber Daya Air',
    cat('kls_ipa', colors={'Kritis Berat': '#d7263d', 'Kritis Ringan': '#f7931e'}),
    fields=['nm_inf', 'nama_ws', 'kls_nrcair', 'kls_ipa', 'ktrs_air', 'kbth_air', 'nrc_air', 'ipa', 'rmh_tangga', 'prkotaan', 'industri', 'irigasi', 'ptrnakan', 'populasi', 'thn_dat'], tol=0.00005)

# ---- Transportasi & infrastruktur
add('JALAN_LN_25K', 'infra', 'Jaringan Jalan',
    cat('REMARK', 'line', colors={
        'Jalan Kolektor': dict(c='#ef4444', w=4), 'Jalan Lokal': dict(c='#f97316', w=3),
        'Jalan Lingkungan': dict(c='#facc15', w=2.4), 'Jalan Lain': dict(c='#f1f5f9', w=1.8),
        'Jalan Setapak': dict(c='#e2e8f0', w=1.2, d='3 3')},
        order=['Jalan Kolektor', 'Jalan Lokal', 'Jalan Lingkungan', 'Jalan Lain', 'Jalan Setapak']),
    fields=['REMARK'], tol=0.00002, desc='Jaringan jalan RBI 1:25.000 menurut fungsi jalan.')
add('JEMBATAN_LN_25K', 'infra', 'Jembatan (Garis)', line('#f43f5e', 5))
add('JEMBATAN_PT_25K', 'infra', 'Jembatan (Titik)', dot('#f43f5e', 5))
add('TONGGAKKM_PT_25K', 'infra', 'Tonggak Kilometer', dot('#64748b', 5))
add('JALANREL_LN_SATUPETA', 'infra', 'Jalur Kereta Api', line('#111827', 3, '8 6'))
add('STASIUNKA_PT_SATUPETA', 'infra', 'Stasiun Kereta Api', dot('#1d4ed8', 9, '🚉'), fields=['bt', 'kodkod', 'wadmkk', 'wadmpr'])
add('JARINGANLISTRIK_LN_SATUPETA', 'infra', 'Jaringan Listrik (Transmisi)', line('#eab308', 2.5, '2 5'), fields=['namobj', 'pjgjar', 'regpln'])
add('KABELLISTRIK_LN_25K', 'infra', 'Kabel Listrik', line('#fde047', 2.5, '2 5'))
add('PIPAMINYAK_LN_25K', 'infra', 'Pipa Minyak/Gas', line('#c026d3', 3))
add('KANTORPOS_PT_25K', 'infra', 'Kantor Pos', dot('#f97316', 9, '✉️'))

# ---- Permukiman & sarana prasarana
POINT_CAT = {
    'Masjid': dict(c='#16a34a', i='🕌'), 'Gereja': dict(c='#7c3aed', i='⛪'),
    'Tempat ibadah lain': dict(c='#7c3aed', i='🛐'),
    'Pendidikan/Penelitian Lainnya': dict(c='#2563eb', i='🎓'), 'Pendidikan (jenjang belum teridentifikasi)': dict(c='#2563eb', i='🎓'),
    'Kantor Kepala Desa': dict(c='#dc2626', i='🏛️'), 'Kantor Camat': dict(c='#b91c1c', i='🏢'), 'Kantor Polisi': dict(c='#1e3a8a', i='👮'),
    'Kantor Pemerintahan': dict(c='#dc2626', i='🏛️'),
    'Rumah Sakit Khusus': dict(c='#e11d48', i='🏥'), 'Faskes (jenis belum teridentifikasi)': dict(c='#e11d48', i='🏥'),
    'Pusat Bisnis dan Perdagangan Lainnya': dict(c='#d97706', i='🛒'), 'Pasar': dict(c='#d97706', i='🛒'),
    'Jasa/perkantoran lain': dict(c='#0891b2', i='💼'), 'Stasiun/Terminal': dict(c='#0f766e', i='🚌'),
    'Pemakaman Bukan Umum': dict(c='#6b7280', i='🪦'), 'Pemakaman Umum': dict(c='#4b5563', i='🪦'),
}
add('PERMUKIMAN_AR_25K', 'sarana', 'Area Permukiman & Tempat Kegiatan', poly('#fb923c', 0.55, '#c2410c', 0.6))
add('PERUMAHAN_PT_25K', 'sarana', 'Bangunan/Gedung (Perumahan)', dot('#f97316', 2.2), fields=['REMARK', 'JKK', 'JMLHUNI'], desc='1.080 titik bangunan pada RBI 1:25.000.')
add('PENDIDIKAN_PT_25K', 'sarana', 'Sarana Pendidikan', cat('REMARK', 'point', colors=POINT_CAT), fields=['REMARK', 'NAMOBJ'])
add('SARANAIBADAH_PT_25K', 'sarana', 'Sarana Peribadatan', cat('REMARK', 'point', colors=POINT_CAT), fields=['REMARK', 'NAMOBJ'])
add('PEMERINTAHAN_PT_25K', 'sarana', 'Kantor Pemerintahan', cat('REMARK', 'point', colors=POINT_CAT), fields=['REMARK', 'NAMOBJ'])
add('RUMAHSAKIT_PT_25K', 'sarana', 'Rumah Sakit/Fasilitas Kesehatan', cat('REMARK', 'point', colors=POINT_CAT), fields=['REMARK', 'NAMOBJ'])
add('NIAGA_PT_25K', 'sarana', 'Pusat Perdagangan & Bisnis', cat('REMARK', 'point', colors=POINT_CAT), fields=['REMARK', 'NAMOBJ'])
add('MAKAM_PT_25K', 'sarana', 'Pemakaman', cat('REMARK', 'point', colors=POINT_CAT), fields=['REMARK', 'NAMOBJ'])
add('SARANAFASILITAS_PT_RBI_OSM', 'sarana', 'Sarana & Fasilitas Terpadu (RBI + OSM)', cat('KATEGORI', 'point', colors=POINT_CAT),
    fields=['NAMA', 'KATEGORI', 'BOBOT', 'WADMKD', 'SUMBER'], desc='Gabungan sarana RBI 1:25.000 dan OpenStreetMap (2026) yang dipakai pada analisis konsentrasi kegiatan.')

# ---- Penggunaan & tutupan lahan
add('PENGGUNAANTANAH_AR_10K', 'lahan', 'Penggunaan Tanah (1:10.000)', cat('ptnobjname', colors=LC, op=0.65),
    fields=['ptnobjname', 'ptnsbjname', 'ig25k_peng', 'ptndate'], tol=0.00003)
add('NSDH_PENUTUPLAHAN_AR_SATUPETA', 'lahan', 'Perubahan Penutupan Lahan (NSDH)', cat('pl_awal', colors=['#65a30d', '#f59e0b'], labels={'2002': 'Penutupan lahan tahun 2002', '2006': 'Penutupan lahan tahun 2006'}),
    fields=['keterangan', 'pl_awal', 'pl_akhir'], tol=0.00004)
add('TUTUPANLAHAN_TL24_AR_RTRW', 'lahan', 'Tutupan Lahan 2024', cat('REMARK', colors=LC, op=0.7), fields=['REMARK', 'HA'], tol=0.00008)
add('TUTUPANLAHAN_TL29_AR_RTRW', 'lahan', 'Tutupan Lahan Proyeksi 2029', cat('REMARK', colors=LC, op=0.7), fields=['REMARK', 'HA'], tol=0.00008)
add('SAWAH_AR_25K', 'lahan', 'Sawah (RBI 1:25.000)', cat('REMARK', colors={'Sawah': '#86efac', 'Sawah Tadah Hujan': '#bef264'}))
add('LADANG_AR_25K', 'lahan', 'Tegalan/Ladang (RBI 1:25.000)', poly('#fcd34d', 0.65), fields=['REMARK'])
add('PERKEBUNAN_AR_25K', 'lahan', 'Perkebunan/Kebun (RBI 1:25.000)', poly('#a16207', 0.6), fields=['REMARK'])
add('SEMAKBELUKAR_AR_25K', 'lahan', 'Semak Belukar (RBI 1:25.000)', poly('#84a98c', 0.65), fields=['REMARK'])
add('HERBADANRUMPUT_AR_25K', 'lahan', 'Herba dan Rumput (RBI 1:25.000)', poly('#d9f99d', 0.7), fields=['REMARK'])
add('LAHANBAKUSAWAH_AR_50K', 'lahan', 'Lahan Baku Sawah (LBS)', poly('#4ade80', 0.6, '#166534', 0.6), fields=['q_name19', 'wadmkk', 'wadmpr'],
    desc='Lahan Baku Sawah berdasarkan Kementerian ATR/BPN (skala 1:50.000).')

# ---- Kondisi fisik & SDA
add('GEOLOGI_AR_RTRW', 'fisik', 'Geologi (Formasi Batuan)', cat('NAME'), fields=['NAME', 'SYMBOLS', 'CLASS_LITH', 'T_CLASS_EN'], tol=0.00005)
add('GEOLOGI_AR_SATUPETA', 'fisik', 'Geologi (Satu Peta)', cat('remark'), fields=['remark', 'simobj', 'umurobj', 'namobj'], tol=0.00005)
add('STRUKTURGEOLOGI_LN_SATUPETA', 'fisik', 'Struktur Geologi (Sesar)', cat('klsstr', 'line', colors={'Sesar': '#7f1d1d', 'Sesar Diperkirakan': '#b91c1c'}, w=2.4), fields=['namaobj', 'klsstr'])
add('PATAHANAKTIF_LN_50K', 'fisik', 'Patahan Aktif', line('#dc2626', 3.5), fields=['jenispthn', 'pjgpthn', 'lokasi', 'geologi', 'sjrhgempa'])
add('MINERALLOGAM_PT_SATUPETA', 'fisik', 'Mineral Logam', dot('#b45309', 10, '⛏️'), fields=['jnskom', 'lbunsur', 'kellgm', 'lokasilgm', 'statdiklgm'])
add('MINERALNONLOGAM_PT_SATUPETA', 'fisik', 'Mineral Bukan Logam & Batuan', dot('#78716c', 9, '🪨'), fields=['jnskombl', 'lbunsurbl', 'kelkombl', 'lokasibl', 'statdikbl', 'acuan'])
add('JENISTANAH_AR_RTRW', 'fisik', 'Jenis Tanah (FAO)', cat('KET', colors=['#a16207']), fields=['KET', 'FAOSOIL', 'DOMSOI'], tol=0.00008)
add('KEMAMPUANLAHAN_AR_RTRW', 'fisik', 'Kemampuan Lahan (SKL)',
    cat('KlasfSKL', colors={'Kemampuan Pengembangan Rendah': '#f46d43', 'Kemampuan Pengembangan Sedang': '#fee08b', 'Kemampuan Pengembangan Tinggi': '#1a9850'}),
    fields=['KlasfSKL', 'KelasKL', 'SKLKp', 'SKLLm', 'SKLEr', 'SKLKa', 'SKLKd', 'SKLMorf', 'SKLBc', 'SKLDr'], tol=0.00008, min_m2=5000)
add('CURAHHUJAN_AR_SATUPETA', 'fisik', 'Curah Hujan Tahunan', cat('crhhjn', colors=['#93c5fd', '#1d4ed8']), fields=['crhhjn'], tol=0.00008)
add('POTENSIENERGIANGIN_AR_SATUPETA', 'fisik', 'Potensi Energi Angin', poly('#67e8f9', 0.5), fields=['poenag'], tol=0.00008)
add('POTENSIENERGISURYA_AR_SATUPETA', 'fisik', 'Potensi Energi Surya', poly('#fde047', 0.5), fields=['poenmt'], tol=0.00008)

# ---- Kebencanaan (data sektoral)
add('KRB_BANJIR_AR_RTRW', 'bencana', 'KRB Banjir', cat('BANJIR', colors=RISK5, order=list(RISK5)), fields=['BANJIR'], tol=0.00008)
add('KRB_GEMPABUMI_AR_RTRW', 'bencana', 'KRB Gempabumi', cat('GEMPABUMI', colors=RISK5, order=list(RISK5)), fields=['GEMPABUMI'], tol=0.00008)
add('KRB_GEMPABUMI_AR_SATUPETA', 'bencana', 'KRB Gempabumi (Satu Peta)',
    cat('kelas', colors={'Kawasan Rawan Bencana Gempabumi Menengah': '#f7931e', 'Kawasan Rawan Bencana Gempabumi Tinggi': '#d7263d'}), fields=['kelas'], tol=0.00008)
add('KRB_GUNUNGAPI_AR_RTRW', 'bencana', 'KRB Gunungapi', cat('GUNUNGAPI', colors=RISK5), fields=['GUNUNGAPI'], tol=0.00008)
add('KRB_LIKUEFAKSI_AR_RTRW', 'bencana', 'KRB Likuefaksi', cat('LIFUEKFASI', colors=RISK5, order=list(RISK5)), fields=['LIFUEKFASI'], tol=0.00008)
add('KERENTANANLIKUEFAKSI_AR_100K', 'bencana', 'Kerentanan Likuefaksi (1:100.000)', poly('#f7931e', 0.5), fields=['keterangan', 'kerentanan'], tol=0.00008)
add('RAWANEROSI_AR_SATUPETA', 'bencana', 'Kelas Erosi Tanah',
    cat('klas_erosi', colors={'<= 15 Ton/Ha/Tahun': '#2e8b57', '> 15 - 60 Ton/Ha/Tahun': '#9ccc3c', '> 60 - 180 Ton/Ha/Tahun': '#ffe14d', '> 180 - 480 Ton/Ha/Tahun': '#f7931e', '> 480 Ton/Ha/Tahun': '#d7263d'},
        order=['<= 15 Ton/Ha/Tahun', '> 15 - 60 Ton/Ha/Tahun', '> 60 - 180 Ton/Ha/Tahun', '> 180 - 480 Ton/Ha/Tahun', '> 480 Ton/Ha/Tahun']),
    fields=['klas_erosi', 'bpdashl'], tol=0.00004)
add('RAWANKARHUTLA_AR_250K', 'bencana', 'Rawan Kebakaran Hutan & Lahan',
    cat('kelas', colors={'Sedang': '#ffe14d', 'Tinggi': '#f7931e', 'Sangat Tinggi': '#d7263d'}, order=['Sedang', 'Tinggi', 'Sangat Tinggi']), fields=['kelas', 'luas', 'provinsi'], tol=0.00004)
add('ZKGT_AR_SATUPETA', 'bencana', 'Zona Kerentanan Gerakan Tanah (ZKGT)',
    cat('zona', colors={'001': '#9ccc3c', '002': '#ffe14d', '003': '#f7931e', '004': '#d7263d'}, order=['001', '002', '003', '004'],
        labels={'001': 'Zona 001 (kerentanan terendah)', '002': 'Zona 002', '003': 'Zona 003', '004': 'Zona 004 (kerentanan tertinggi)'}),
    fields=['zona', 'klsgtn', 'tahun'], tol=0.00004)

# ---- Kawasan hutan, perizinan & pertanahan
add('KAWASANHUTAN_AR_SATUPETA', 'hutan', 'Kawasan Hutan (SK KLHK)', cat('fungsitap', colors=['#15803d', '#65a30d'], labels={'100100': 'Fungsi Kawasan Hutan 100100', '100300': 'Fungsi Kawasan Hutan 100300'}),
    fields=['fungsitap', 'nkws', 'nosktap', 'tglsktap'], tol=0.00003)
add('PIPPIB_AR_250K', 'hutan', 'PIPPIB (Penundaan Izin Baru)', poly('#b45309', 0.35, '#78350f', 1), fields=['pippib'], tol=0.00004)
add('PPTPKH_AR_SATUPETA', 'hutan', 'Penguasaan Tanah dalam Kawasan Hutan (PPTPKH)', cat('kriteria', colors=['#e11d48', '#f59e0b']), fields=['kriteria'], tol=0.00003)
add('WKMIGAS_AR_SATUPETA', 'hutan', 'Wilayah Kerja Migas', poly('#6b7280', 0.3, '#374151', 2), fields=['namobj', 'oprblk', 'status', 'effdat', 'expdat'])
add('PITTI_BATASDAERAH_TR_KH_AR', 'hutan', 'PITTI: Tipologi Ketidaksesuaian Tata Ruang–Kawasan Hutan',
    cat('tipologi', colors={'Tidak Bermasalah': '#4ade80', 'Indikasi Bermasalah': '#f87171'}, op=0.55, w=0.3),
    fields=['tipologi', 'ktgr_ktdsn', 'dsr_hukum'], tol=0.00003, dissolve_by=['tipologi', 'ktgr_ktdsn', 'dsr_hukum'],
    desc='Poligon bertetangga dengan atribut sama digabung (dissolve). PITTI = Penyelesaian Ketidaksesuaian Tata Ruang, Kawasan Hutan, Izin, dan Hak Atas Tanah.')
add('PITTI_HAKATASTANAH_AR', 'hutan', 'PITTI: Hak Atas Tanah',
    cat('tipologi', colors={'Tidak Bermasalah': '#4ade80', 'Indikasi Bermasalah': '#f87171'}, op=0.55, w=0.3),
    fields=['tipologi', 'ktgr_ktdsn', 'dsr_hukum'], tol=0.00003, dissolve_by=['tipologi', 'ktgr_ktdsn', 'dsr_hukum'],
    desc='Poligon bertetangga dengan atribut sama digabung (dissolve).')
add('PITTI_HGU_SAWIT_AR', 'hutan', 'PITTI: HGU Sawit', cat('skema'), fields=['skema', 'tipologi', 'luas_pitti', 'dsr_hukum'], tol=0.00004)
add('PITTI_PERTAMBANGAN_AR', 'hutan', 'PITTI: Pertambangan', cat('skema', colors={'HP/HP///': '#a16207', 'APL////': '#f59e0b', 'HL/HL///': '#166534'}),
    fields=['skema', 'tipologi', 'dsr_hukum'], tol=0.00004)

# ---- Rencana tata ruang & program
add('RTRWN_AR', 'rtr', 'RTRW Nasional: Pola Ruang', poly('#84cc16', 0.5), fields=['rtrpns', 'nothpp'], tol=0.00005)
add('RTRWN_POLARUANG_AR', 'rtr', 'RTRW Nasional: Pola Ruang (Hasil Analisis 2017)', cat('namobj'), fields=['namobj', 'nothpr', 'sbdata'], tol=0.00005)
add('RTRWN_KAWASANANDALAN_LN', 'rtr', 'RTRW Nasional: Kawasan Andalan', line('#7c3aed', 3), fields=['rtrpns', 'nothpp'])
add('RTRWN_STRUKTUR_TRANSPORTASI_LN', 'rtr', 'RTRW Nasional: Struktur Ruang Transportasi', line('#be123c', 3.5, '8 4'), fields=['sbdata', 'nothpr'])
add('RTRWP_AR', 'rtr', 'RTRW Provinsi Jawa Timur: Pola Ruang', cat('rtrsys'), fields=['rtrsys', 'nothpd', 'wadmpr'], tol=0.00004)
add('RTRWK_AR', 'rtr', 'RTRW Kabupaten Ponorogo: Pola Ruang', cat('rtrpkk'), fields=['rtrpkk', 'nothpd', 'wadmkk'], tol=0.00004)
add('RUANGUDARA_AR_50K', 'rtr', 'Ruang Udara (FIR/UTA/Sektor)', cat('namobj', op=0.25), fields=['namobj', 'jenis', 'service', 'low_limit', 'upp_limit', 'frekuensi'], tol=0.00008)
add('RKP_PKH_AR', 'rtr', 'RKP 2017: Program Keluarga Harapan', poly('#f472b6', 0.3, '#be185d', 2), fields=['remark', 'nama_rcn', 'dmn_rcn', 'prio_rcn', 'stat_rcn', 'thn_rcn', 'trg_rcn', 'plksn_rcn'])
add('RKP2018_PKH_AR', 'rtr', 'RKP 2018: Program Keluarga Harapan', poly('#fb7185', 0.3, '#be123c', 2), fields=['nama_rcn', 'dmn_rcn', 'prio_rcn', 'stat_rcn', 'thn_rcn', 'trg_rcn', 'plksn_rcn'])
add('RKP2018_JALAN_LN', 'rtr', 'RKP 2018: Pembangunan Jalan Pansela', line('#f43f5e', 4, '6 4'), fields=['namrjl', 'nama_rcn', 'stat_rcn', 'dmn_rcn', 'prio_rcn', 'thn_rcn', 'trg_rcn', 'plksn_rcn'])
add('RPJMN_RENCANAJALANPROVINSI_LN', 'rtr', 'RPJMN: Rencana Jalan Provinsi', line('#ea580c', 4, '6 4'), fields=['ruas_prov', 'nama_rcn', 'stat_rcn', 'dimensi', 'prioritas', 'tahun', 'target', 'pelaksana'])

# ---- Analisis RDTR: kesesuaian lahan
add('FUNGSIKAWASAN_AR', 'a_lahan', 'Fungsi Kawasan (Lindung/Penyangga/Budi Daya)',
    cat('NAMA', colors={'Kawasan Lindung': '#15803d', 'Kawasan Penyangga': '#facc15', 'Kawasan Budi Daya': '#fb923c'}, order=['Kawasan Lindung', 'Kawasan Penyangga', 'Kawasan Budi Daya']),
    fields=['NAMA', 'LUAS_HA'], tol=0.00003, info='FUNGSIKAWASAN_AR')
add('KENDALAMUTLAK_AR', 'a_lahan', 'Kendala Mutlak Pengembangan Permukiman',
    cat('NAMA', colors={'Badan air & sempadan sungai/waduk': '#3b82f6', 'Kawasan hutan (SK KLHK)': '#15803d', 'Lereng > 40%': '#a16207', 'Rawan longsor tinggi': '#dc2626'}),
    fields=['NAMA', 'LUAS_HA'], tol=0.00003, info='KENDALAMUTLAK_AR')
add('KESESUAIANPERMUKIMAN_AR', 'a_lahan', 'Kesesuaian Lahan untuk Permukiman', cat('NAMA', colors=SUIT, order=list(SUIT)),
    fields=['NAMA', 'KET_KDL', 'ARAHAN', 'LUAS_HA'], tol=0.00003, info='KESESUAIANPERMUKIMAN_AR')
add('LAHANTERSEDIA_PERMUKIMAN_AR', 'a_lahan', 'Lahan Tersedia untuk Permukiman', cat('NAMA', colors=SUIT, order=list(SUIT)),
    fields=['NAMA', 'ARAHAN', 'LUAS_HA'], tol=0.00003, info='LAHANTERSEDIA_PERMUKIMAN_AR')
add('KESESUAIANPANGAN_AR', 'a_lahan', 'Kesesuaian Lahan Pangan (Sawah)', cat('NAMA', colors=SUIT, order=list(SUIT)),
    fields=['NAMA', 'ARAHAN', 'LBS', 'SAWAH_EKS', 'LUAS_HA'], tol=0.00003, info='KESESUAIANPANGAN_AR')

# ---- Analisis RDTR: aksesibilitas
add('AKSESIBILITAS_AR', 'a_akses', 'Indeks Aksesibilitas Wilayah',
    cat('NAMA', colors={'Aksesibilitas Rendah': '#f46d43', 'Aksesibilitas Sedang': '#fee08b', 'Aksesibilitas Tinggi': '#1a9850'}, order=['Aksesibilitas Rendah', 'Aksesibilitas Sedang', 'Aksesibilitas Tinggi']),
    fields=['NAMA', 'ARAHAN', 'LUAS_HA'], tol=0.00003, info='AKSES_DESA_AR')
add('SERVICEAREA_PUSATWP_AR', 'a_akses', 'Area Layanan Waktu Tempuh dari Pusat WP',
    cat('NAMA', colors={'0-5 menit': '#1a9850', '5-10 menit': '#91cf60', '10-15 menit': '#fee08b', '15-30 menit': '#fc8d59', '> 30 menit': '#d73027'}, order=['0-5 menit', '5-10 menit', '10-15 menit', '15-30 menit', '> 30 menit']),
    fields=['NAMA', 'LUAS_HA'], tol=0.00003, info='AKSES_DESA_AR')
add('AKSES_DESA_AR', 'a_akses', 'Aksesibilitas per Desa',
    cat('SKB_STATUS', colors={'Tidak/sedikit terdampak': '#4ade80', 'TERISOLASI (tidak terjangkau)': '#ef4444'}, op=0.55, w=1.2, stroke='#0f172a'),
    label='WADMKD', fields=['WADMKD', 'T_PUSATWP', 'T_PPL', 'T_BUPATI', 'HANSEN_B1', 'HANSEN_B2', 'KRPT_JLN', 'SKA_TWP', 'SKB_TWP', 'SKB_STATUS'], tol=0.00003, info='AKSES_DESA_AR')
add('SKENARIO_RUAS_TERPUTUS_LN', 'a_akses', 'Skenario Ruas Jalan Terputus (Bencana)', cat('FUNGSI', 'line', colors={'Jalan Kolektor': '#ef4444', 'Jalan Lokal': '#f97316', 'Jalan Lingkungan': '#facc15', 'Jalan Lain': '#f8fafc', 'Jalan Setapak': '#cbd5e1'}, w=3),
    fields=['FUNGSI', 'SKENARIO', 'PANJANG_M'], info='AKSES_DESA_AR')

# ---- Analisis RDTR: pusat pelayanan & desa
add('KLASIFIKASIDESA_AR', 'a_pusat', 'Klasifikasi Desa Perkotaan–Perdesaan',
    cat('TIPOLOGI', colors=['#f59e0b', '#fb7185', '#34d399', '#60a5fa'], op=0.6, w=1.2, stroke='#0f172a'), label='DESA',
    fields=['DESA', 'TIPOLOGI', 'KLS_BPS20', 'KLS_DESA', 'IDM25', 'PUSAT_RTRW', 'ORDE_SKALO', 'PEND25', 'LUAS_BPS', 'KPDT_BPS', 'R_2325', 'MKM_HA', 'KPDT_NET', 'N_KEG', 'WAKTU_WP', 'KAND_INTI'], tol=0.00003, info='KLASIFIKASI_DESA')
add('ORDE_DESA_AR', 'a_pusat', 'Orde Desa (Skalogram)', cat('ORDE', colors={'I': '#7f1d1d', 'II': '#f97316', 'III': '#fde047'}, order=['I', 'II', 'III'], op=0.65, w=1.2, stroke='#0f172a'),
    label='WADMKD', fields=['WADMKD', 'ORDE', 'JML_JENIS', 'TOTAL_UNIT', 'IDX_SENTR'], tol=0.00003, info='KLASIFIKASI_DESA')
add('LQ_KEGIATAN_DESA_AR', 'a_pusat', 'Location Quotient (LQ) Kegiatan per Desa',
    cat('LQ_NILAI', colors={'1': '#fef3c7', '2': '#fcd34d', '3': '#f97316', '4': '#b91c1c'}, op=0.65, w=1.2, stroke='#0f172a',
        labels={'1': 'LQ < 0,5 (skor 1)', '2': 'LQ 0,5–1 (skor 2)', '3': 'LQ 1–1,5 (skor 3)', '4': 'LQ 1,5–2 (skor 4)'}),
    label='WADMKD', fields=['WADMKD', 'LQ', 'LQ_NILAI', 'BOBOT_KEG', 'MUKIM_HA'], tol=0.00003, info='HOTSPOT_GISTAR_GRID100M_AR')
add('KONSENTRASIKEGIATAN_AR', 'a_pusat', 'Konsentrasi Kegiatan',
    cat('NAMA', colors={'Konsentrasi Rendah': '#fef08a', 'Konsentrasi Sedang': '#fb923c', 'Konsentrasi Tinggi': '#b91c1c'}, order=['Konsentrasi Rendah', 'Konsentrasi Sedang', 'Konsentrasi Tinggi']),
    fields=['NAMA', 'ARAHAN', 'LUAS_HA'], tol=0.00003, info='HOTSPOT_GISTAR_GRID100M_AR')
add('HOTSPOT_GISTAR_GRID100M_AR', 'a_pusat', 'Hotspot Kegiatan (Getis-Ord Gi*, Grid 100 m)',
    cat('G_NILAI', colors={'2': dict(c='#e2e8f0', o=0.0), '3': '#fde047', '4': '#fb923c', '5': '#b91c1c'}, order=['2', '3', '4', '5'], op=0.7, w=0, stroke='#000000',
        labels={'2': 'Tidak signifikan', '3': 'Hotspot (kepercayaan 90%)', '4': 'Hotspot (kepercayaan 95%)', '5': 'Hotspot (kepercayaan 99%)'}),
    fields=['W_SUM', 'GiZScore', 'GiPValue', 'G_NILAI'], tol=0.00001, dissolve_by=['G_NILAI', 'W_SUM'], dissolve_only=('G_NILAI', 2),
    desc='Sel yang tidak signifikan digabung menjadi satu area latar; sel hotspot tetap per grid 100 m.')
add('TITIK_KEGIATAN_PT', 'a_pusat', 'Titik Kegiatan Berbobot (Skala Pelayanan)', cat('KATEGORI', 'point', colors=POINT_CAT),
    fields=['NAMA', 'KATEGORI', 'BOBOT', 'WADMKD', 'SUMBER'], info='HOTSPOT_GISTAR_GRID100M_AR')

# ---- Analisis RDTR: kebencanaan
add('RAWANBANJIR_AR', 'a_bnc', 'Kerawanan Banjir', cat('NAMA', colors=_r('Kerawanan', ['Rendah', 'Sedang', 'Tinggi']), order=['Kerawanan Rendah', 'Kerawanan Sedang', 'Kerawanan Tinggi']),
    fields=['NAMA', 'LUAS_HA'], tol=0.00003, info='RAWANBANJIR_AR')
add('RAWANLONGSOR_AR', 'a_bnc', 'Kerawanan Longsor', cat('NAMA', colors=_r('Kerawanan', ['Rendah', 'Sedang', 'Tinggi']), order=['Kerawanan Rendah', 'Kerawanan Sedang', 'Kerawanan Tinggi']),
    fields=['NAMA', 'K_MODEL', 'K_ZKGT', 'LUAS_HA'], tol=0.00003, info='RAWANLONGSOR_AR')
add('KERENTANAN_AR', 'a_bnc', 'Kerentanan Bencana', cat('NAMA', colors=_r('Kerentanan', ['Rendah', 'Sedang', 'Tinggi']), order=['Kerentanan Rendah', 'Kerentanan Sedang', 'Kerentanan Tinggi']),
    fields=['NAMA', 'LUAS_HA'], tol=0.00003, info='KERENTANAN_AR')
add('RISIKOBENCANA_AR', 'a_bnc', 'Risiko Bencana (Banjir & Longsor)', cat('NAMA', colors=_r('Risiko', ['Rendah', 'Sedang', 'Tinggi']), order=['Risiko Rendah', 'Risiko Sedang', 'Risiko Tinggi']),
    fields=['NAMA', 'R_LONGSOR', 'R_BANJIR', 'LUAS_HA'], tol=0.00003, info='KERENTANAN_AR')

# ---- D3TLH
add('D3TLH_JASAEKOSISTEM_AR_RTRW', 'd3tlh', 'Jasa Ekosistem (Kelas Prioritas)',
    cat('KLS_PNTNG', colors={'Prioritas I': '#15803d', 'Prioritas II': '#65a30d', 'Prioritas III': '#facc15', 'Prioritas IV': '#fb923c', 'Prioritas V': '#dc2626'}, order=['Prioritas I', 'Prioritas II', 'Prioritas III', 'Prioritas IV', 'Prioritas V']),
    fields=['KLS_PNTNG', 'REMARK', 'GENESIS', 'xveg_OK', 'KECAMATAN', 'HECTARES', 'KLS_P1', 'KLS_P2', 'KLS_P3', 'KLS_P4', 'KLS_P5'], tol=0.00008)
add('D3TLH_STATUSAIR24_AR_RTRW', 'd3tlh', 'Status Daya Dukung Air 2024',
    cat('KET', colors={'TERLAMPAUI': '#ef4444', 'BELUM TERLAMPAUI': '#4ade80'}, op=0.6, w=0), fields=['KET', 'REMARK', 'Sungai', 'N_Air', 'KLS_P2'], tol=0.00001, dissolve_by=['KET', 'REMARK', 'Sungai', 'N_Air', 'KLS_P2'],
    desc='Sel grid 150 m dengan atribut sama digabung (dissolve) agar ringan ditampilkan.')
add('D3TLH_STATUSAIR29_AR_RTRW', 'd3tlh', 'Status Daya Dukung Air Proyeksi 2029',
    cat('KET', colors={'TERLAMPAUI': '#ef4444', 'BELUM TERLAMPAUI': '#4ade80'}, op=0.6, w=0), fields=['KET', 'REMARK', 'Sungai', 'N_Air', 'KLS_P2'], tol=0.00001, dissolve_by=['KET', 'REMARK', 'Sungai', 'N_Air', 'KLS_P2'],
    desc='Sel grid 150 m dengan atribut sama digabung (dissolve) agar ringan ditampilkan.')
add('D3TLH_STATUSPANGAN29_AR_RTRW', 'd3tlh', 'Status Daya Dukung Pangan Proyeksi 2029',
    cat('KETERANGAN', colors={'TERLAMPAUI': '#ef4444', 'BELUM TERLAMPAUI': '#4ade80'}, op=0.6, w=0), fields=['KETERANGAN', 'REMARK', 'KLS_P1', 'KLS_P2'], tol=0.00001, dissolve_by=['KETERANGAN', 'REMARK', 'KLS_P1', 'KLS_P2'],
    desc='Sel grid dengan atribut sama digabung (dissolve) agar ringan ditampilkan.')

# raster diproses terpisah (lihat build_data.py)
RASTERS = [
    dict(id='raster_dem', name='Model Elevasi Digital (DEM 10 m)', group='raster', src='DEM_KONTUR25K_10M', kind='dem',
         desc='DEM resolusi 10 m yang dibangun dari kontur RBI 1:25.000, titik tinggi, dan sungai.'),
    dict(id='raster_hillshade', name='Bayangan Relief (Hillshade, turunan DEM)', group='raster', src='DEM_KONTUR25K_10M', kind='hillshade',
         desc='Bayangan relief dihitung dari DEM 10 m (azimut 315°, elevasi matahari 45°) untuk memperjelas bentuk lahan.'),
    dict(id='raster_lereng', name='Kemiringan Lereng (Raster, %)', group='raster', src='LERENG_PERSEN_DEM25K_10M', kind='slope',
         desc='Kemiringan lereng dalam persen yang diturunkan dari DEM 10 m.'),
]

# berkas pendukung per folder ZIP: METODE_DAN_HASIL.txt / 00_KETERANGAN.txt, CSV rekap, XLSX
