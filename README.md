# WebGIS RDTR Kecamatan Slahung

WebGIS Rencana Detail Tata Ruang (RDTR) **Kecamatan Slahung, Kabupaten Ponorogo, Jawa Timur**.
Menampilkan seluruh data shapefile (ZIP) pada repository ini — 115 layer vektor dan 3 raster —
dengan nama layer berbahasa Indonesia, simbologi/legenda per layer, dan basemap **Google Satelit**.

## Fitur

- **Katalog layer** terkelompok (16 kelompok): batas administrasi, peta dasar & topografi, hidrologi, infrastruktur,
  permukiman & sarana, penggunaan/tutupan lahan, kondisi fisik, kebencanaan, kawasan hutan & perizinan,
  rencana tata ruang, hasil analisis RDTR (kesesuaian lahan, aksesibilitas, pusat pelayanan, kebencanaan), dan D3TLH.
- **Basemap**: Google Satelit (bawaan), Google Satelit + Label, Google Peta Jalan, Google Medan, OpenStreetMap, Carto Terang/Gelap.
- **Legenda otomatis**, pengaturan **urutan tumpukan** dan **transparansi** per layer.
- **Klik peta** = identifikasi semua objek dari seluruh layer aktif pada titik tersebut (atribut berlabel Indonesia).
- **Tabel atribut** (filter, zoom ke objek, unduh CSV), **Info & Metadata**, serta **Metode & Hasil Analisis** dan
  **tabel rekap per desa** (dari file `METODE_DAN_HASIL.txt`, CSV, dan XLSX di dalam ZIP).
- Pencarian layer, zoom ke desa, alat ukur jarak/luas, koordinat kursor, skala, layar penuh,
  tautan yang menyimpan layer aktif + basemap + posisi peta, tampilan responsif (HP/tablet).
- Tautan **Unduh ZIP** pada tiap layer mengarah ke shapefile asli di repository.

## Menjalankan

Situs ini statis (HTML + JavaScript + Leaflet), tanpa server khusus.

- **GitHub Pages**: *Settings → Pages → Build and deployment → Deploy from a branch*, pilih branch dan folder `/ (root)`.
  Situs akan tersedia di `https://<pengguna>.github.io/RDTR_Slahung/`.
- **Lokal**: buka `index.html` langsung di browser, atau jalankan `python3 -m http.server` lalu buka `http://localhost:8000`.
  (Basemap memerlukan koneksi internet.)

## Struktur

```
index.html            halaman utama
assets/app.js|css     logika dan tampilan WebGIS
assets/vendor/leaflet pustaka Leaflet 1.9.4 (BSD-2-Clause)
data/                 data hasil olahan (dibuat otomatis)
  catalog.js            katalog layer, simbologi, legenda, daftar desa
  layers/*.js           GeoJSON WGS84 per layer (dimuat saat layer dicentang)
  raster/*.png          DEM, hillshade, dan lereng (sudah direproyeksi ke WGS84)
  info/*.js             teks metode & tabel rekap per kelompok analisis
tools/catalog.py      nama tampilan, pengelompokan, dan simbologi tiap layer (EDIT di sini)
tools/build_data.py   konversi ZIP shapefile → data/
*.zip                 data shapefile sumber
```

## Memperbarui data

Jika ZIP diganti/ditambah, jalankan dari root repository:

```bash
pip install pyshp pyproj shapely numpy pillow openpyxl tifffile imagecodecs
python3 tools/build_data.py
```

Layer baru perlu didaftarkan di `tools/catalog.py` (nama, kelompok, gaya); skrip akan memberi peringatan
bila ada shapefile yang belum terdaftar.

## Catatan data

- Seluruh data dikonversi dari UTM 49S (EPSG:32749) / WGS84 ke WGS84 (EPSG:4326) untuk web.
- Geometri disederhanakan ±2 m; bintik < 0,5 ha pada layer *Kemampuan Lahan* dan *Kelas Kemiringan Lereng*
  dihilangkan; sel grid bertetangga dengan atribut sama pada layer *D3TLH Status Daya Dukung*, *PITTI*, dan latar *Hotspot* digabung
  agar ringan di browser. Data lengkap tetap tersedia pada ZIP.
- `KEPADATAN_DASIMETRIK_GRID100M_AR.shx` hanya berisi berkas indeks; berkas `.shp`, `.dbf`, dan `.prj` belum terunggah
  sehingga layer kepadatan penduduk dasimetrik belum dapat ditampilkan. Unggah ZIP lengkapnya lalu daftarkan di `tools/catalog.py`.
- Kode klasifikasi tanpa keterangan di data sumber (mis. fungsi kawasan hutan `100100`/`100300`) ditampilkan apa adanya.
- Basemap Google dimuat langsung dari server tile Google dan tunduk pada ketentuan layanan Google.
