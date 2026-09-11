---
version: alpha
name: Purwarupa Nilai Tanah Bandar Lampung
description: Identitas visual untuk purwarupa DSS pemutakhiran NJOP (peta zona dan kalkulator per bidang). Palet navy dan emas diambil dari identitas resmi Politeknik Keuangan Negara STAN (bukan gambar slide judulnya, hanya warnanya), dipasangkan dengan tekstur grunge halus supaya latar tidak terlalu polos. Struktur tipografi dan spacing tetap mengikuti disiplin kontras dan ritme yang diadaptasi dari sistem desain e-commerce (Nike) pada revisi sebelumnya.

colors:
  light:
    bg: "#f4f4f0"
    panel: "#ffffff"
    ink: "#10233f"
    ink-soft: "#55627d"
    border: "#d7dbe3"
    gold: "#8a6d16"
    btn-bg: "#10233f"
    btn-text: "#f4f4f0"
    positive: "#2f7d5c"
    negative: "#b23a2c"
    warn-bg: "#fbf1da"
    warn-border: "#b8912f"
    warn-ink: "#6b4e08"
    faktor-track: "#ecebe4"
  dark:
    bg: "#071c38"
    panel: "#10284d"
    ink: "#f2f0e6"
    ink-soft: "#a7b2c6"
    border: "#27436d"
    gold: "#e8cf6b"
    btn-bg: "#c9a227"
    btn-text: "#10233f"
    positive: "#4fbf82"
    negative: "#e2604a"
    warn-bg: "#2c2410"
    warn-border: "#c9a227"
    warn-ink: "#f0d998"
    faktor-track: "#16305a"

typography:
  header:
    fontFamily: "'Nunito', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    fontSize: 22px
    fontWeight: 700
    lineHeight: 1.3
    use: Judul halaman (st.title) -- satu-satunya elemen di tingkat ini, seperti "billboard" kecil di atas seluruh form
  sub-header:
    fontFamily: "'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    fontSize: 12.5px
    fontWeight: 600
    letterSpacing: 0.4px
    textTransform: uppercase
    use: Label kartu/bagian ("1. Data bidang", "Hasil", "Faktor yang paling memengaruhi angka ini")
  body:
    fontFamily: "'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.55
    use: Semua teks isi -- deskripsi, disclaimer, caption, hasil kalkulasi

spacing:
  xxs: 2px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  section: 48px

rounded:
  sm: 6px
  md: 10px
  lg: 14px

elevation:
  flat:
    shadow: none
    use: Perlakuan default untuk semua kartu, tombol, input -- tidak ada elemen yang "melayang"
  hairline:
    treatment: "1px solid {colors.light.border}"
    use: Pembatas antar baris/kartu bila diperlukan

texture:
  grunge-overlay:
    source: static/textures/grunge.png (noise + goresan tipis yang dibuat sendiri, bukan diambil dari foto/gambar berhak cipta)
    opacity: 0.05 (light) / 0.08 (dark)
    blendMode: overlay
    use: Lapisan tekstur di atas latar solid supaya tidak terasa polos/flat, terinspirasi kesan "kertas bertekstur" pada slide judul PKN STAN -- BUKAN gambar itu sendiri

components:
  card:
    backgroundColor: "{colors.light.panel}"
    border: "1px solid {colors.light.border}"
    borderRadius: "{rounded.md}"
    padding: "{spacing.md} {spacing.lg}"
  button-primary:
    backgroundColor: "{colors.light.btn-bg}"
    textColor: "{colors.light.btn-text}"
    borderRadius: "{rounded.sm}"
    note: Warna terbalik per mode -- navy-emas di terang, emas-navy di gelap -- supaya CTA selalu menampilkan pasangan navy+emas, bukan cuma satu warna
  button-primary-pressed:
    backgroundColor: "{colors.light.btn-bg}"
    filter: brightness(0.9)
    note: Feedback tekan yang jelas tapi tidak dramatis -- bukan animasi scale/opacity ala aplikasi konsumen
  metric-positive:
    color: "{colors.light.positive}"
  metric-negative:
    color: "{colors.light.negative}"
---

## Overview

Purwarupa ini adalah alat bantu teknis untuk staf BPPRD, bukan produk konsumen atau demo
startup atau toko daring. Palet navy dan emas diambil dari identitas resmi Politeknik
Keuangan Negara STAN (dasar penilai membuat purwarupa ini) -- disaring dari warna sebuah
slide judul sidang, BUKAN gambar slide itu sendiri. Memakai gambar itu langsung sebagai
latar akan menabrak logo dan teks "D-IV Manajemen Aset Publik" yang tidak relevan dengan
kalkulator BPPRD, dan elemen-elemen tetapnya akan tertutup kartu form. Yang diambil hanya
tiga hal: warna navy dominan, aksen emas, dan kesan tekstur "kertas bertekstur"-nya --
dibangun ulang sebagai lapisan noise/goresan tipis buatan sendiri (`static/textures/grunge.png`),
bukan gambar berhak cipta pihak lain.

Struktur (tipografi, spacing, elevation datar) tetap mengikuti prinsip yang diadaptasi
dari sistem desain e-commerce Nike pada revisi sebelumnya: kontras tipografi tegas, skala
spacing 8px, kartu flat tanpa shadow. Warna sekarang berpindah dari krem/cokelat tanah ke
navy/emas institusional -- perubahan yang justru memperkuat kesan "instrumen resmi
pemerintah" dibanding palet sebelumnya, karena ini benar-benar warna lembaga yang
menaungi penelitian ini, bukan warna netral generik.

## Colors

Latar navy dalam (`bg`) di mode gelap meniru warna dominan identitas PKN STAN (disampel
langsung dari slide judul: `#00234c`, dihaluskan sedikit jadi `#071c38` untuk latar
halaman yang lebih dalam dari panel kartu di atasnya). Mode terang membalik ke krem
dingin (`#f4f4f0`) dengan teks navy (`ink`) menggantikan tinta hijau-hitam sebelumnya --
tetap terasa satu keluarga lewat penggunaan navy sebagai warna teks utama di kedua mode.

Emas (`gold`) dipakai konsisten sebagai aksen kedua di kedua mode: emas tua (`#8a6d16`)
di atas latar terang supaya kontras cukup, emas terang (`#e8cf6b`) di atas latar gelap.
Dipakai untuk angka hasil kalkulasi (`hasil-angka`) dan penekanan kecil lain, TIDAK
untuk latar dekoratif atau badge -- prinsip lama "warna aksen bukan untuk hiasan"
dipertahankan.

Tombol utama (`btn-bg`/`btn-text`) sengaja membalik pasangan navy-emas per mode: navy
padat dengan teks emas-krem di mode terang, emas padat dengan teks navy di mode gelap.
Efeknya, tombol aksi utama SELALU menampilkan pasangan warna navy+emas bersama-sama,
bukan cuma satu warna brand terisolasi -- ini yang membuat identitasnya terasa utuh di
kedua mode, bukan sekadar "ganti satu warna aksen".

Hijau (`positive`) dan merah (`negative`) untuk sinyal naik/turun pada faktor penentu
nilai disesuaikan sedikit temperaturnya supaya cocok berdampingan dengan navy (lebih
dingin dari versi cokelat-tanah sebelumnya), tetap redup, bukan warna terang saturasi
tinggi.

## Texture

Latar solid navy/krem diberi lapisan tekstur tipis (`static/textures/grunge.png`) --
noise halus dan goresan tipis acak, dibuat sendiri secara prosedural, BUKAN diambil dari
foto atau gambar berhak cipta apa pun. Opacity sangat rendah (5-8%) dengan
`mix-blend-mode: overlay`, supaya latar terasa seperti kertas/dokumen bertekstur alih-alih
warna flat polos -- terinspirasi kesan tekstur pada slide judul PKN STAN, tanpa meniru
gambarnya secara langsung. Tekstur ini dekoratif murni: tidak boleh mengganggu kontras
atau keterbacaan teks di atasnya, karena itu opacity dijaga sangat rendah dan hanya
diterapkan di lapisan latar paling belakang, bukan di atas kartu/panel.

## Typography

Tiga tingkat kontras yang jelas dan disiplin dipakai konsisten (prinsip "billboard di
atas, isi tenang di bawah" dari sistem Nike, diskalakan jauh lebih kecil karena ini alat
kerja bukan materi kampanye): `header` (22px, tegas, dipakai HANYA untuk judul halaman),
`sub-header` (12.5px kapital kecil tebal dengan letter-spacing, dipakai untuk label
kartu/bagian, gaya dokumen formulir resmi), dan `body` (14px, line-height lega, dipakai
untuk semua isi). Tidak ada tingkat perantara -- lompatan tegas dari judul ke label kecil
ke isi ini yang membuat halaman terasa terstruktur tanpa perlu banyak ukuran font.

Font judul pakai Nunito (Bold), semua yang lain -- label kartu/bagian, tombol, dan
seluruh teks isi -- pakai Poppins, dimuat lewat Google Fonts CDN langsung di `app.py`
(bukan file lokal). Keduanya font open-license (SIL OFL), boleh disebarluaskan bebas
lewat repo publik. SF Pro dan Gotham sempat dipertimbangkan tapi sengaja TIDAK dipakai:
metadata file SF Pro yang beredar menyebut lisensinya terikat "iOS Software License
Agreement" milik Apple sendiri (tidak untuk web di luar platform Apple), dan bundel
Gotham yang sempat diberikan berisi Gotham, Gotham Rounded, dan Gotham Narrow lengkap
semua bobot dalam satu folder -- pola khas font bajakan, bukan pembelian lisensi
webfont resmi dari Hoefler & Frere-Jones. Menaruh file semacam itu di repo GitHub
publik berarti menyebarluaskan font berhak cipta tanpa izin, jadi keduanya tidak
dipakai; fallback ke stack sistem native (`-apple-system`, Segoe UI) tetap aktif bila
Google Fonts gagal dimuat.

## Layout

Struktur dua kolom (form di kiri, peta/hasil di kanan) dipertahankan, tapi setiap
kelompok elemen dibungkus jadi "kartu" (lewat `st.container(border=True, key=...)`, bukan
div HTML yang dibuka/ditutup lewat `st.markdown` terpisah -- itu tidak benar-benar
membungkus widget Streamlit di antaranya) dengan border tipis dan padding konsisten,
bukan widget lepas berjejer tanpa pengelompokan visual. Jarak antar elemen memakai
skala spacing berbasis 8px yang eksplisit (2/4/8/16/24/32px, dengan 48px sebagai jarak
"section" antar blok besar), bukan jarak sembarangan bawaan Streamlit.

## Elevation & Depth

Nyaris tanpa bayangan (shadow). Kedalaman dibangun dari border tipis dan perbedaan warna
latar panel vs latar halaman (di mode gelap, panel navy sedikit lebih terang dari latar
navy dalam di belakangnya), bukan drop-shadow lembut besar yang jadi ciri "kartu AI
melayang". Satu-satunya elemen non-flat adalah lapisan tekstur grunge tipis di latar
paling belakang (lihat bagian Texture), yang murni dekoratif dan tidak menambah kesan
"melayang" pada kartu manapun.

## Shapes

Sudut membulat halus (6-10px), tidak tajam siku (kesan terlalu formal/tua) dan tidak
terlalu bulat (kesan aplikasi konsumen) -- secara sadar TIDAK memakai bentuk pil
(`border-radius` penuh). Konsisten di semua kartu, tombol, dan input -- satu kosakata
bentuk saja, tidak dicampur dengan bentuk lain. Peta referensi kecamatan (iframe) ikut
dibulatkan sudutnya supaya konsisten dengan kartu lain.

## Components

Tombol utama ("Hitung indikasi nilai") memakai pasangan warna `btn-bg`/`btn-text` yang
terbalik per mode (lihat bagian Colors), sudut membulat kecil, tanpa gradient. Status
ditekan (`button-primary-pressed`) diberi feedback jelas lewat `filter: brightness(0.9)`,
didefinisikan eksplisit sebagai entri komponen terpisah.

Kartu hasil (indikasi nilai, faktor penentu, rujukan kecamatan) memakai gaya kartu yang
sama (border tipis, padding konsisten, latar panel navy/putih sesuai mode). Angka hasil
kalkulasi utama ditampilkan dalam warna emas (`gold`) sebagai penekanan, bukan warna tinta
biasa. Bar faktor penentu nilai (SHAP dalam rupiah) selalu mulai rata kiri, memakai warna
hijau untuk faktor yang menaikkan nilai dan merah untuk yang menurunkan -- arah dibedakan
HANYA lewat warna, bukan sisi mulai bar, dan didahului baris "nilai dasar model" sebagai
titik acuan sebelum daftar faktor.

## Do's and Don'ts

Jangan pakai gambar slide judul PKN STAN secara langsung sebagai latar -- ambil warna dan
kesan teksturnya saja, bukan logo/teks/komposisinya. Jangan pakai gradient warna-warni,
drop-shadow tebal, ikon emoji berlebihan, atau badge/pill warna-warni yang jadi ciri khas
tampilan hasil generatif AI standar. Jangan pakai istilah pemasaran ("Powered by AI",
"Smart Estimate"). Jangan pakai tombol berbentuk pil atau headline raksasa. Jangan biarkan
opacity tekstur grunge naik sampai mengganggu kontras teks -- batasi di kisaran 5-8% dan
hanya di lapisan latar paling belakang. Pakai istilah teknis yang sudah dipakai di
purwarupa peta zona (NIR, ZNT, indikasi awal) secara konsisten. Jangan tampilkan warna
terlalu jenuh (saturated) untuk elemen non-peringatan; simpan warna kuat hanya untuk
status peringatan data tipis/ekstrapolasi.
