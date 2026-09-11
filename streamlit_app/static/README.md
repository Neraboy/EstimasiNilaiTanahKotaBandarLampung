# Isi folder static/

Folder ini dipakai untuk aset yang di-serve langsung oleh Streamlit
(`server.enableStaticServing = true` di `.streamlit/config.toml`, repo root).

- `textures/grunge.png` -- tekstur noise/goresan tipis buatan sendiri untuk latar
  halaman (lihat DESIGN.md bagian Texture). Aman disebarluaskan, bukan hasil scan
  atau gambar berhak cipta pihak lain.

Font Nunito (judul) dan Poppins (semua teks lain) dimuat lewat Google Fonts CDN
langsung di `app.py`, TIDAK di-host lokal di sini -- keduanya font open-license
(SIL OFL), tidak butuh file lokal maupun static serving.

Catatan: SF Pro dan Gotham sempat dipertimbangkan untuk teks judul/isi, tapi tidak
jadi dipakai. SF Pro cuma boleh dipakai untuk software di platform Apple sendiri
(lisensinya eksplisit menyebut "iOS Software License Agreement" pada metadata
filenya), dan Gotham perlu lisensi webfont terpisah dari Hoefler & Frere-Jones yang
tidak bisa dipastikan dari bundel file yang sempat diberikan (satu folder berisi
Gotham, Gotham Rounded, dan Gotham Narrow lengkap semua bobot -- pola khas bundel
font bajakan, bukan hasil pembelian lisensi resmi). Menaruh file semacam itu di repo
GitHub publik berarti menyebarluaskan font berhak cipta tanpa izin, jadi keduanya
sengaja tidak dipakai di purwarupa ini.
