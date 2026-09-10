---
version: alpha
name: Purwarupa Nilai Tanah Bandar Lampung
description: Identitas visual untuk purwarupa DSS pemutakhiran NJOP (peta zona dan kalkulator per bidang), bernuansa kadaster/pertanahan resmi. Struktur tipografi dan spacing diadaptasi dari sistem desain e-commerce (Nike) untuk disiplin kontras dan ritme, warna dan nada tetap kadaster/resmi -- bukan gaya toko maupun dashboard AI generik.

colors:
  light:
    bg: "#f6f3ee"
    panel: "#ffffff"
    ink: "#1f2420"
    ink-soft: "#5a6058"
    border: "#dcd7cc"
    accent: "#7a6a4f"
    accent-dark: "#5a4a2f"
    positive: "#3f7a4f"
    negative: "#a33f2b"
    warn-bg: "#fdf1e8"
    warn-border: "#c97b2e"
    warn-ink: "#7a4413"
    faktor-track: "#efece4"
  dark:
    bg: "#1c1a16"
    panel: "#262219"
    ink: "#ece7db"
    ink-soft: "#b7ac97"
    border: "#453e30"
    accent: "#c9a877"
    accent-dark: "#dab98a"
    positive: "#6fbf7f"
    negative: "#e07a5f"
    warn-bg: "#3a2c1c"
    warn-border: "#c97b2e"
    warn-ink: "#f0c896"
    faktor-track: "#332e24"

typography:
  header:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    fontSize: 22px
    fontWeight: 700
    lineHeight: 1.3
    use: Judul halaman (st.title) -- satu-satunya elemen di tingkat ini, seperti "billboard" kecil di atas seluruh form
  sub-header:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    fontSize: 12px
    fontWeight: 500
    letterSpacing: 0.3px
    textTransform: uppercase
    use: Label kartu/bagian ("1. Data bidang", "Hasil", "Faktor yang paling memengaruhi angka ini")
  body:
    fontFamily: "Gotham, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
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

components:
  card:
    backgroundColor: "{colors.light.panel}"
    border: "1px solid {colors.light.border}"
    borderRadius: "{rounded.md}"
    padding: "{spacing.md} {spacing.lg}"
  button-primary:
    backgroundColor: "{colors.light.accent-dark}"
    textColor: "#ffffff"
    borderRadius: "{rounded.sm}"
  button-primary-pressed:
    backgroundColor: "{colors.light.accent-dark}"
    filter: brightness(0.9)
    note: Feedback tekan yang jelas tapi tidak dramatis -- bukan animasi scale/opacity ala aplikasi konsumen
  metric-positive:
    color: "{colors.light.positive}"
  metric-negative:
    color: "{colors.light.negative}"
---

## Overview

Purwarupa ini adalah alat bantu teknis untuk staf BPPRD, bukan produk konsumen atau demo
startup atau toko daring. Arahnya kadaster dan administratif: tenang, netral, dipercaya,
mirip nuansa peta resmi pertanahan (bhumi.atrbpn.go.id) dan dokumen pemerintahan.

Struktur (bukan warna) sebagian diadaptasi dari sistem desain e-commerce Nike: kontras
tipografi yang tegas antara judul dan isi, skala spacing berbasis 8px yang konsisten, dan
kartu benar-benar flat tanpa shadow. Yang SENGAJA TIDAK diambil dari Nike: palet
hitam-putih-merah, tombol berbentuk pil (pill), headline raksasa 96px, dan nada suara
"athletic/kinetic" -- semua itu cocok untuk menjual sepatu, bukan untuk alat penilaian
tanah pemerintah. Warna dan nada tetap krem/kertas dan cokelat tanah seperti sebelumnya.

Palet ini SAMA dengan yang dipakai di purwarupa peta zona interaktif (HTML/Leaflet),
supaya kedua purwarupa terasa sebagai satu produk yang koheren, bukan dua alat terpisah
yang tidak berhubungan. Sejak revisi ini, palet juga punya varian gelap (`colors.dark`)
yang otomatis aktif mengikuti pengaturan terang/gelap sistem pengguna.

## Colors

Latar dasar krem hangat (`bg`), bukan putih polos atau gelap, supaya terasa seperti
kertas/dokumen, bukan layar aplikasi generik. Panel/kartu putih bersih dengan border
tipis warna krem gelap, bukan bayangan (shadow) tebal yang jadi ciri khas "desain AI".
Aksen warna cokelat tanah (`accent-dark`, #5a4a2f) dipakai untuk tombol utama dan judul
penting, bukan biru/ungu vibrant dan bukan hitam pekat ala Nike. Hijau tanah (`positive`)
dan merah bata (`negative`) untuk indikasi naik/turun pada faktor penentu nilai, dipilih
redup, bukan warna terang saturasi tinggi -- dan tidak pernah dipakai sebagai warna badge
atau latar dekoratif, hanya untuk sinyal semantik (naik/turun/peringatan), sama seperti
prinsip Nike membatasi warna semantik hanya untuk sinyal harga/status.

Mode gelap (`colors.dark`) membalik kontras dengan nuansa yang sama: latar cokelat tua
hangat, panel sedikit lebih terang, teks krem terang, aksen cokelat muda keemasan --
bukan hitam pekat/abu netral generik, supaya tetap terasa satu keluarga dengan mode
terang.

## Typography

Tiga tingkat kontras yang jelas dan disiplin dipakai konsisten (prinsip "billboard di
atas, isi tenang di bawah" dari sistem Nike, diskalakan jauh lebih kecil karena ini alat
kerja bukan materi kampanye): `header` (22px, tegas, dipakai HANYA untuk judul halaman),
`sub-header` (12px kapital kecil dengan letter-spacing, dipakai untuk label kartu/bagian,
gaya dokumen formulir resmi), dan `body` (14px, line-height lega, dipakai untuk semua isi).
Tidak ada tingkat perantara -- lompatan tegas dari judul ke label kecil ke isi ini yang
membuat halaman terasa terstruktur tanpa perlu banyak ukuran font.

Font header/sub-header pakai stack sistem native (`-apple-system` dst., SF Pro asli di
perangkat Apple, Segoe UI di Windows). Font isi (`body`) pakai Gotham yang di-host sendiri
dari file berlisensi (lihat `static/README.md`), jatuh ke stack sistem native bila file
belum tersedia.

## Layout

Struktur dua kolom (form di kiri, peta/hasil di kanan) dipertahankan, tapi setiap
kelompok elemen dibungkus jadi "kartu" dengan border tipis dan padding konsisten,
bukan widget lepas berjejer tanpa pengelompokan visual. Jarak antar elemen memakai
skala spacing berbasis 8px yang eksplisit (2/4/8/16/24/32px, dengan 48px sebagai jarak
"section" antar blok besar), bukan jarak sembarangan bawaan Streamlit -- prinsip ini
diambil langsung dari disiplin skala 8px sistem Nike, walau sistem Nike memakai angka yang
sedikit berbeda untuk kebutuhan katalog produk.

## Elevation & Depth

Nyaris tanpa bayangan (shadow), sama seperti prinsip "flat, no elevation" yang dipegang
ketat oleh sistem Nike untuk kartu produknya. Kedalaman dibangun dari border tipis dan
perbedaan warna latar panel vs latar halaman, bukan drop-shadow lembut besar yang jadi
ciri "kartu AI melayang". Ini sesuai instruksi menghindari kesan desain yang dihasilkan
AI generatif, dan sekaligus konsisten dengan prinsip "cards do not lift" dari referensi.

## Shapes

Sudut membulat halus (6-10px), tidak tajam siku (kesan terlalu formal/tua) dan tidak
terlalu bulat (kesan aplikasi konsumen) -- secara sadar TIDAK memakai bentuk pil
(`border-radius` penuh) seperti tombol Nike, karena itu akan membuat tombol utama
terlihat seperti tombol "Beli Sekarang" toko daring, bukan alat kerja pemerintah.
Konsisten di semua kartu, tombol, dan input -- satu kosakata bentuk saja, tidak
dicampur dengan bentuk lain, mengikuti prinsip Nike "jangan perkenalkan bentuk tombol
ketiga".

## Components

Tombol utama ("Hitung indikasi nilai") memakai warna aksen gelap solid, teks putih,
sudut membulat kecil, tanpa gradient. Status ditekan (`button-primary-pressed`)
diberi feedback jelas lewat `filter: brightness(0.9)`, didefinisikan eksplisit sebagai
entri komponen terpisah -- bukan ditumpuk jadi satu deskripsi prosa -- mengikuti
kebiasaan sistem Nike mendokumentasikan status default dan aktif/ditekan secara terpisah
untuk tiap komponen.

Kartu hasil (indikasi nilai, faktor penentu, rujukan kecamatan) memakai gaya kartu yang
sama (border tipis, padding konsisten). Bar faktor penentu nilai (SHAP dalam rupiah)
memakai warna hijau tanah untuk faktor yang menaikkan nilai dan merah bata untuk yang
menurunkan, panjang bar proporsional terhadap besar kontribusi, bukan bar chart pustaka
default dengan warna kategori acak.

## Do's and Don'ts

Jangan pakai gradient warna-warni, drop-shadow tebal, ikon emoji berlebihan, atau
badge/pill warna-warni yang jadi ciri khas tampilan hasil generatif AI standar. Jangan
pakai istilah pemasaran ("Powered by AI", "Smart Estimate", "Shop Now"). Jangan pakai
tombol berbentuk pil, headline raksasa, atau palet hitam-putih-merah ala toko daring --
prinsip struktural sistem referensi (kontras tipografi, spacing 8px, flat card) boleh
dipakai, warnanya tidak. Pakai istilah teknis yang sudah dipakai di purwarupa peta zona
(NIR, ZNT, indikasi awal) secara konsisten. Jangan tampilkan warna terlalu jenuh
(saturated) untuk elemen non-peringatan; simpan warna kuat hanya untuk status peringatan
data tipis/ekstrapolasi.
