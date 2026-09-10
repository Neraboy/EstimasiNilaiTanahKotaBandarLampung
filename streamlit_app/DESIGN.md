---
version: alpha
name: Purwarupa Nilai Tanah Bandar Lampung
description: Identitas visual untuk purwarupa DSS pemutakhiran NJOP (peta zona dan kalkulator per bidang), bernuansa kadaster/pertanahan resmi, bukan gaya dashboard AI generik.

colors:
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

typography:
  headline:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    fontSize: 22px
    fontWeight: 650
    lineHeight: 1.3
  body:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontSize: 12px
    fontWeight: 650
    letterSpacing: 0.3px
    textTransform: uppercase

spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px

rounded:
  sm: 6px
  md: 10px
  lg: 14px

components:
  card:
    backgroundColor: "{colors.panel}"
    border: "1px solid {colors.border}"
    borderRadius: "{rounded.md}"
    padding: "{spacing.md}"
  button-primary:
    backgroundColor: "{colors.accent-dark}"
    textColor: "#ffffff"
    borderRadius: "{rounded.sm}"
  metric-positive:
    color: "{colors.positive}"
  metric-negative:
    color: "{colors.negative}"
---

## Overview

Purwarupa ini adalah alat bantu teknis untuk staf BPPRD, bukan produk konsumen atau demo
startup. Arahnya kadaster dan administratif: tenang, netral, dipercaya, mirip nuansa
peta resmi pertanahan (bhumi.atrbpn.go.id) dan dokumen pemerintahan, bukan gaya "dashboard
AI" dengan gradasi ungu-biru terang, ikon neon, atau kartu melayang berbayang tebal yang
umum dipakai demo produk SaaS. Nuansa krem/kertas dan cokelat tanah dipilih supaya
terasa dekat dengan konteks pertanahan/kadaster, bukan generik.

Palet ini SAMA dengan yang dipakai di purwarupa peta zona interaktif (HTML/Leaflet),
supaya kedua purwarupa terasa sebagai satu produk yang koheren, bukan dua alat terpisah
yang tidak berhubungan.

## Colors

Latar dasar krem hangat (`bg`), bukan putih polos atau gelap, supaya terasa seperti
kertas/dokumen, bukan layar aplikasi generik. Panel/kartu putih bersih dengan border
tipis warna krem gelap, bukan bayangan (shadow) tebal yang jadi ciri khas "desain AI".
Aksen warna cokelat tanah (`accent-dark`, #5a4a2f) dipakai untuk tombol utama dan judul
penting, bukan biru/ungu vibrant. Hijau tanah (`positive`) dan merah bata (`negative`)
untuk indikasi naik/turun pada faktor penentu nilai, dipilih redup, bukan warna terang
saturasi tinggi.

## Typography

Font sistem native (`-apple-system` dst.), bukan Google Font dekoratif. Judul tegas tapi
tidak besar berlebihan (22px), teks isi 14px dengan line-height lega untuk keterbacaan.
Label kategori (misal nama kolom form) memakai huruf kapital kecil dengan letter-spacing
tipis, gaya dokumen formulir resmi, bukan huruf tebal besar bergaya iklan.

## Layout

Struktur dua kolom (form di kiri, peta/hasil di kanan) dipertahankan, tapi setiap
kelompok elemen dibungkus jadi "kartu" dengan border tipis dan padding konsisten,
bukan widget lepas berjejer tanpa pengelompokan visual. Jarak antar elemen memakai
skala spacing yang jelas (4/8/16/24/32px), bukan jarak sembarangan bawaan Streamlit.

## Elevation & Depth

Nyaris tanpa bayangan (shadow). Kedalaman dibangun dari border tipis dan perbedaan warna
latar panel vs latar halaman, bukan drop-shadow lembut besar yang jadi ciri "kartu AI
melayang". Ini sesuai instruksi menghindari kesan desain yang dihasilkan AI generatif.

## Shapes

Sudut membulat halus (6-10px), tidak tajam siku (kesan terlalu formal/tua) dan tidak
terlalu bulat (kesan aplikasi konsumen). Konsisten di semua kartu, tombol, dan input.

## Components

Tombol utama ("Hitung indikasi nilai") memakai warna aksen gelap solid, teks putih,
sudut membulat kecil, tanpa gradient. Kartu hasil (indikasi nilai, faktor penentu,
rujukan kecamatan) memakai gaya kartu yang sama (border tipis, padding konsisten).
Bar faktor penentu nilai (SHAP dalam rupiah) memakai warna hijau tanah untuk faktor
yang menaikkan nilai dan merah bata untuk yang menurunkan, panjang bar proporsional
terhadap besar kontribusi, bukan bar chart pustaka default dengan warna kategori
acak.

## Do's and Don'ts

Jangan pakai gradient warna-warni, drop-shadow tebal, ikon emoji berlebihan, atau
badge/pill warna-warni yang jadi ciri khas tampilan hasil generatif AI standar. Jangan
pakai istilah pemasaran ("Powered by AI", "Smart Estimate"). Pakai istilah teknis yang
sudah dipakai di purwarupa peta zona (NIR, ZNT, indikasi awal) secara konsisten. Jangan
tampilkan warna terlalu jenuh (saturated) untuk elemen non-peringatan; simpan warna
kuat hanya untuk status peringatan data tipis/ekstrapolasi.
