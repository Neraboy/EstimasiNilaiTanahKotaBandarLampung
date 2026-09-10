"""
Kalkulator Indikasi Awal Nilai Tanah -- Kota Bandar Lampung
Purwarupa skripsi, BUKAN alat penetapan NJOP/ZNT/NIR resmi.
Identitas visual mengikuti DESIGN.md di folder ini.
"""
import json
import os

import folium
import joblib
import numpy as np
import pandas as pd
import shap
import streamlit as st
from streamlit_folium import st_folium

BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "data")

st.set_page_config(page_title="Kalkulator Indikasi Nilai Tanah - Bandar Lampung", layout="wide")

# --- Gaya visual (lihat DESIGN.md): krem/kertas + cokelat tanah, kartu berbatas tipis
# tanpa shadow tebal, tanpa gradient -- sengaja menghindari kesan "dashboard AI generik".
# Mengikuti tema sistem (terang/gelap otomatis) lewat prefers-color-scheme, selaras dengan
# [theme.light]/[theme.dark] di .streamlit/config.toml (lihat file itu untuk warna native
# widget Streamlit -- CSS di sini hanya untuk elemen kustom kartu/label/bar).
#
# Font: judul & sub-judul pakai stack -apple-system (SF Pro asli di Mac/iPhone, Segoe UI
# Bold sebagai fallback wajar di Windows -- SF Pro tidak bisa di-host sebagai file font
# karena lisensinya dibatasi khusus platform Apple). Teks deskripsi pakai Gotham, di-host
# sendiri lewat @font-face dari file berlisensi yang disediakan pengguna -- lihat
# static/README.md di folder ini untuk cara menaruh filenya. Selama file itu belum ada,
# browser otomatis jatuh ke fallback sans-serif tanpa error. ---
st.markdown(
    """
    <style>
    @font-face {
        font-family: "Gotham";
        src: url("app/static/fonts/Gotham-Book.woff2") format("woff2");
        font-weight: 400; font-style: normal; font-display: swap;
    }
    @font-face {
        font-family: "Gotham";
        src: url("app/static/fonts/Gotham-Medium.woff2") format("woff2");
        font-weight: 500; font-style: normal; font-display: swap;
    }

    :root {
        --bg: #f6f3ee; --panel: #ffffff; --ink: #1f2420; --ink-soft: #5a6058;
        --border: #dcd7cc; --accent: #7a6a4f; --accent-dark: #5a4a2f;
        --positive: #3f7a4f; --negative: #a33f2b;
        --warn-bg: #fdf1e8; --warn-border: #c97b2e; --warn-ink: #7a4413;
        --faktor-track: #efece4;
        --font-header: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        --font-body: "Gotham", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        /* Skala spacing 8px (lihat DESIGN.md -- prinsip diadaptasi dari disiplin spacing Nike) */
        --sp-xxs: 2px; --sp-xs: 4px; --sp-sm: 8px; --sp-md: 16px; --sp-lg: 24px;
        --sp-xl: 32px; --sp-section: 48px;
    }
    @media (prefers-color-scheme: dark) {
        :root {
            --bg: #1c1a16; --panel: #262219; --ink: #ece7db; --ink-soft: #b7ac97;
            --border: #453e30; --accent: #c9a877; --accent-dark: #dab98a;
            --positive: #6fbf7f; --negative: #e07a5f;
            --warn-bg: #3a2c1c; --warn-border: #c97b2e; --warn-ink: #f0c896;
            --faktor-track: #332e24;
        }
    }

    .stApp { background: var(--bg); }
    body, p, span, div, label, li { font-family: var(--font-body); }
    /* Kontras tipografi 3 tingkat: header > sub-header (.label-kecil) > body -- tidak ada
       tingkat perantara, lihat DESIGN.md bagian Typography. */
    h1, h2, h3 {
        color: var(--ink) !important; font-family: var(--font-header) !important;
        font-weight: 700 !important;
    }
    .block-container { padding-top: var(--sp-xl); }

    /* Kartu sungguhan lewat st.container(border=True, key="kartu_...") -- bukan div HTML
       yang dibuka/ditutup lewat st.markdown terpisah (itu TIDAK benar-benar membungkus
       widget Streamlit di antaranya, hanya membuat kotak kosong). Selector attribute
       [class*=] menjangkau semua key yang diawali "kartu" sekaligus. */
    div[class*="st-key-kartu"] {
        background: var(--panel) !important; border: 1px solid var(--border) !important;
        border-radius: 10px !important;
    }
    .label-kecil {
        font-family: var(--font-header); font-size: 12.5px; font-weight: 700; letter-spacing: .4px;
        text-transform: uppercase; color: var(--ink); margin-bottom: var(--sp-xs);
    }
    .peringatan-disclaimer {
        background: var(--warn-bg); border: 1px solid var(--warn-border); border-radius: 10px;
        padding: var(--sp-sm) var(--sp-md); color: var(--warn-ink); font-size: 14px; line-height: 1.55;
    }
    .hasil-angka { font-size: 30px; font-weight: 700; color: var(--accent-dark); margin: var(--sp-xxs) 0; }
    .hasil-sub { font-size: 12.5px; color: var(--ink-soft); }
    .hasil-dasar {
        font-size: 13.5px; color: var(--ink-soft); padding: var(--sp-sm) 0 var(--sp-md) 0;
        border-bottom: 1px solid var(--border); margin-bottom: var(--sp-sm);
    }

    /* Semua bar faktor mulai rata kiri -- arah naik/turun dibedakan HANYA lewat warna,
       bukan lewat sisi mana bar itu mulai (lebih mudah dibaca sebagai satu barisan). */
    .faktor-baris {
        display: flex; align-items: center; gap: var(--sp-sm); margin: var(--sp-xs) 0; font-size: 13.5px;
    }
    .faktor-nama { width: 230px; flex: none; color: var(--ink); }
    .faktor-bar-wrap { flex: 1; background: var(--faktor-track); border-radius: 4px; height: 18px; position: relative; }
    .faktor-bar { height: 18px; border-radius: 4px; }
    .faktor-nilai { width: 130px; flex: none; text-align: right; font-weight: 600; font-size: 13px; }

    /* Peta referensi kecamatan (iframe streamlit-folium) -- sudut dibuat membulat
       konsisten dengan kartu lain, bukan kotak siku bawaan iframe. */
    iframe[title="streamlit_folium.st_folium"] {
        border-radius: 10px; overflow: hidden; border: 1px solid var(--border);
    }

    /* Satu kosakata bentuk tombol saja (sudut membulat kecil, bukan pil) -- status default,
       hover, dan ditekan didefinisikan terpisah dan eksplisit, lihat DESIGN.md komponen
       button-primary / button-primary-pressed. */
    div.stButton > button[kind="primary"] {
        background: var(--accent-dark); border: none; border-radius: 6px; color: #fff;
        font-family: var(--font-header); transition: filter 0.1s ease;
    }
    div.stButton > button[kind="primary"]:hover { filter: brightness(0.94); }
    div.stButton > button[kind="primary"]:active { filter: brightness(0.85); }

    [data-testid="stMetric"] {
        background: var(--panel); border: 1px solid var(--border); border-radius: 10px;
        padding: var(--sp-sm) var(--sp-md);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_model():
    model = joblib.load(os.path.join(DATA, "model_final.joblib"))
    info = json.load(open(os.path.join(DATA, "fitur_info.json")))
    return model, info


@st.cache_data
def load_grid():
    return pd.read_csv(os.path.join(DATA, "grid_lookup.csv"))


@st.cache_data
def load_kecamatan_nir():
    return pd.read_csv(os.path.join(DATA, "kecamatan_nir.csv"))


@st.cache_data
def load_zona_geojson():
    with open(os.path.join(DATA, "kecamatan_zona.geojson")) as f:
        return json.load(f)


@st.cache_resource
def load_shap_explainer(_model):
    return shap.TreeExplainer(_model.named_steps["est"])


model, info = load_model()
grid = load_grid()
kec_nir = load_kecamatan_nir()
zona_geojson = load_zona_geojson()
explainer = load_shap_explainer(model)

FITUR = info["FITUR"]
JARAK_COLS = [
    "jarak_ke_transportasi", "jarak_ke_pendidikan", "jarak_ke_pemerintahan",
    "jarak_ke_kolektor_sekunder", "jarak_ke_kolektor_primer", "jarak_ke_kesehatan",
    "jarak_ke_CBD", "jarak_ke_arteri_sekunder", "jarak_ke_arteri_primer",
]

# Rentang data latih, untuk peringatan ekstrapolasi (lihat expander di bagian bawah halaman)
RENTANG_LATIH = {
    "luas": (56, 10000),
    "latitude": (-5.47485144929159, -5.34246958998922),
    "longitude": (105.190345574862, 105.333857363892),
}

# Nama fitur teknis -> label yang bisa dipahami orang awam
LABEL_FITUR = {
    "num__ln_luas": "Luas tanah",
    "num__latitude": "Posisi lintang (utara-selatan)",
    "num__longitude": "Posisi bujur (barat-timur)",
    "num__jarak_ke_transportasi": "Jarak ke transportasi umum",
    "num__jarak_ke_pendidikan": "Jarak ke fasilitas pendidikan",
    "num__jarak_ke_pemerintahan": "Jarak ke kantor pemerintahan",
    "num__jarak_ke_kolektor_sekunder": "Jarak ke jalan kolektor sekunder",
    "num__jarak_ke_kolektor_primer": "Jarak ke jalan kolektor primer",
    "num__jarak_ke_kesehatan": "Jarak ke fasilitas kesehatan",
    "num__jarak_ke_CBD": "Jarak ke pusat kota (CBD)",
    "num__jarak_ke_arteri_sekunder": "Jarak ke jalan arteri sekunder",
    "num__jarak_ke_arteri_primer": "Jarak ke jalan arteri primer",
    "num__banjir": "Riwayat rawan banjir",
    "num__longsor": "Riwayat rawan longsor",
    "kat__jenis_hak_SHM": "Jenis hak: SHM",
    "kat__zonasi_Permukiman": "Zonasi: Permukiman",
}

st.title("Kalkulator Indikasi Awal Nilai Tanah")
st.caption("Purwarupa skripsi -- Kota Bandar Lampung -- Model Random Forest")

st.markdown(
    """
    <div class="peringatan-disclaimer">
    <b>Ini BUKAN alat penetapan NJOP, ZNT, atau NIR resmi.</b> Angka yang keluar dari
    kalkulator ini adalah indikasi awal untuk satu bidang berdasarkan model machine
    learning skripsi. Menurunkan indikasi ini menjadi ZNT dan NIR resmi adalah proses
    dan kewenangan BPPRD sendiri, bukan keluaran otomatis dari alat ini.
    </div>
    """,
    unsafe_allow_html=True,
)
st.write("")

col_form, col_map = st.columns([1, 1.3])

with col_form:
    with st.container(border=True, key="kartu_data_bidang"):
        st.markdown('<div class="label-kecil">1. Data bidang</div>', unsafe_allow_html=True)
        luas = st.number_input(
            "Luas tanah (m²)", min_value=1, max_value=100000, value=170, step=1,
            help=f"Rentang data latih model: {RENTANG_LATIH['luas'][0]:,} - {RENTANG_LATIH['luas'][1]:,} m². "
                 "Di luar rentang ini, model melakukan ekstrapolasi dan hasilnya kurang bisa diandalkan.",
        )
        jenis_hak = st.selectbox("Jenis hak", ["SHM", "SHGB"])
        zonasi = st.selectbox("Zonasi (RTRW)", ["Permukiman", "NonPermukiman"])
        banjir = st.radio("Riwayat rawan banjir di lokasi ini?", ["Tidak", "Ya"], horizontal=True)
        longsor = st.radio("Riwayat rawan longsor di lokasi ini?", ["Tidak", "Ya"], horizontal=True)

    with st.container(border=True, key="kartu_lokasi_bidang"):
        st.markdown('<div class="label-kecil">2. Lokasi bidang</div>', unsafe_allow_html=True)
        st.caption("Klik peta di sebelah kanan untuk menandai lokasi, atau isi koordinat manual di bawah.")
        lat_manual = st.number_input("Lintang (latitude)", value=-5.4295, format="%.6f")
        lon_manual = st.number_input("Bujur (longitude)", value=105.2625, format="%.6f")

with col_map:
    st.markdown('<div class="label-kecil">Peta referensi kecamatan</div>', unsafe_allow_html=True)
    try:
        CARTO_KEY = st.secrets.get("CARTO_API_KEY", "")
    except Exception:
        CARTO_KEY = ""
    tile_url = "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
    if CARTO_KEY:
        tile_url += f"?key={CARTO_KEY}"
    else:
        st.caption(
            'Peta dasar belum diberi API key CARTO, jadi bisa muncul watermark '
            '"API KEY REQUIRED". Tambahkan CARTO_API_KEY di Settings > Secrets '
            "aplikasi Streamlit Cloud."
        )
    m = folium.Map(location=[-5.4295, 105.2625], zoom_start=12, tiles=None)
    folium.TileLayer(
        tiles=tile_url,
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains="abcd",
        max_zoom=19,
    ).add_to(m)
    folium.GeoJson(
        zona_geojson,
        name="Kecamatan",
        style_function=lambda f: {
            "fillColor": "#efa761" if not f["properties"].get("peringatan_data_tipis") else "#fdf1e8",
            "color": "#5a4a2f",
            "weight": 1,
            "fillOpacity": 0.35,
        },
        tooltip=folium.GeoJsonTooltip(fields=["kecamatan"], aliases=["Kecamatan:"]),
    ).add_to(m)
    map_state = st_folium(m, height=430, width=None, key="peta_lokasi")

    if map_state and map_state.get("last_clicked"):
        lat_manual = map_state["last_clicked"]["lat"]
        lon_manual = map_state["last_clicked"]["lng"]
        st.caption(f"Lokasi dari klik peta: {lat_manual:.6f}, {lon_manual:.6f}")

st.write("")
hitung = st.button("Hitung indikasi nilai", type="primary", use_container_width=True)

if hitung:
    # --- Cari titik grid terdekat untuk meminjam 9 fitur jarak jaringan jalan ---
    d2 = (grid["latitude"] - lat_manual) ** 2 + (grid["longitude"] - lon_manual) ** 2
    idx_terdekat = d2.idxmin()
    titik = grid.loc[idx_terdekat]
    jarak_ke_titik_m = np.sqrt(d2.loc[idx_terdekat]) * 111000  # derajat -> meter, aproksimasi kasar

    baris = {
        "ln_luas": np.log(luas),
        "latitude": lat_manual,
        "longitude": lon_manual,
        "banjir": 1.0 if banjir == "Ya" else 0.0,
        "longsor": 1.0 if longsor == "Ya" else 0.0,
        "jenis_hak": jenis_hak,
        "zonasi": zonasi,
    }
    for c in JARAK_COLS:
        baris[c] = titik[c]

    X = pd.DataFrame([baris])[FITUR]
    pred_ln = model.predict(X)[0]
    pred_per_m2 = float(np.exp(pred_ln))
    pred_total = pred_per_m2 * luas

    with st.container(border=True, key="kartu_hasil"):
        st.markdown('<div class="label-kecil">Hasil</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.metric("Indikasi awal nilai per m²", f"Rp{pred_per_m2:,.0f}")
        c2.metric("Indikasi awal total bidang", f"Rp{pred_total:,.0f}")

    # --- Peringatan ekstrapolasi ---
    peringatan = []
    if not (RENTANG_LATIH["luas"][0] <= luas <= RENTANG_LATIH["luas"][1]):
        peringatan.append(
            f"Luas {luas:,} m² di luar rentang data latih ({RENTANG_LATIH['luas'][0]:,}-"
            f"{RENTANG_LATIH['luas'][1]:,} m²). Random Forest tidak bisa diandalkan untuk "
            "ekstrapolasi di luar rentang data yang pernah dilihatnya saat training."
        )
    if not (RENTANG_LATIH["latitude"][0] <= lat_manual <= RENTANG_LATIH["latitude"][1]) or not (
        RENTANG_LATIH["longitude"][0] <= lon_manual <= RENTANG_LATIH["longitude"][1]
    ):
        peringatan.append("Lokasi berada di luar cakupan area data transaksi yang dipakai melatih model.")
    if jarak_ke_titik_m > 350:
        peringatan.append(
            f"Fitur jarak jaringan jalan dipinjam dari titik referensi grid sejauh "
            f"~{jarak_ke_titik_m:,.0f} meter dari lokasi yang kamu tandai (grid berjarak 500 m, "
            "jadi ini di luar radius aproksimasi yang wajar). Anggap indikasi ini lebih kasar dari biasanya."
        )
    else:
        st.caption(
            f"Fitur jarak jaringan jalan dipinjam dari titik referensi grid terdekat "
            f"(~{jarak_ke_titik_m:,.0f} meter dari lokasi yang ditandai), bukan dihitung ulang presisi "
            "untuk lokasi persis ini."
        )
    for p in peringatan:
        st.markdown(f'<div class="peringatan-disclaimer" style="margin-top:8px;">{p}</div>', unsafe_allow_html=True)

    # --- Faktor penentu nilai (SHAP, diterjemahkan ke rupiah) ---
    pra = model.named_steps["pra"]
    est_input = pra.transform(X)
    nama_teknis = list(pra.get_feature_names_out())
    shap_values = explainer.shap_values(est_input)[0]

    # Nilai dasar model (expected_value, skala ln) -> rupiah/m2. Ini titik awal sebelum
    # faktor-faktor di bawah menambah/mengurangi, bukan cuma daftar faktor lepas tanpa acuan.
    base_ln = explainer.expected_value
    if hasattr(base_ln, "__len__"):
        base_ln = base_ln[0]
    base_per_m2 = float(np.exp(base_ln))

    kontribusi = []
    for nama, sv in zip(nama_teknis, shap_values):
        rp = pred_per_m2 * (np.exp(sv) - 1)  # aproksimasi lokal, lihat catatan di bawah
        kontribusi.append((LABEL_FITUR.get(nama, nama), rp))
    kontribusi.sort(key=lambda t: -abs(t[1]))
    top = kontribusi[:6]
    maks_abs = max(abs(v) for _, v in top) or 1.0

    with st.container(border=True, key="kartu_faktor"):
        st.markdown('<div class="label-kecil">Faktor yang paling memengaruhi angka ini</div>', unsafe_allow_html=True)
        st.caption(
            "Menunjukkan enam faktor dengan pengaruh terbesar terhadap indikasi nilai per m² di atas, "
            "dalam perkiraan rupiah, bukan grafik teknis. Hijau menaikkan nilai, merah menurunkan."
        )
        st.markdown(
            f'<div class="hasil-dasar">Nilai dasar model (rata-rata bidang sejenis di data latih): '
            f'<b>Rp{base_per_m2:,.0f} / m²</b> &rarr; disesuaikan oleh faktor-faktor di bawah &rarr; '
            f'hasil akhir <b>Rp{pred_per_m2:,.0f} / m²</b></div>',
            unsafe_allow_html=True,
        )
        for nama, rp in top:
            warna = "var(--positive)" if rp >= 0 else "var(--negative)"
            lebar = max(6, abs(rp) / maks_abs * 100)
            tanda = "+" if rp >= 0 else "-"
            st.markdown(
                f"""
                <div class="faktor-baris">
                  <div class="faktor-nama">{nama}</div>
                  <div class="faktor-bar-wrap">
                    <div class="faktor-bar" style="width:{lebar:.0f}%; background:{warna};"></div>
                  </div>
                  <div class="faktor-nilai" style="color:{warna};">{tanda} Rp{abs(rp):,.0f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.caption(
            "Angka rupiah di atas perkiraan pengaruh tiap faktor secara lokal untuk bidang ini saja "
            "(bukan aturan umum berlaku sama untuk semua bidang), dihitung mulai dari nilai dasar model "
            "di atas -- jumlah totalnya tidak dijamin pas sama dengan indikasi nilai akhir karena model "
            "dilatih pada skala logaritmik."
        )

    # --- Rujukan nilai tengah kecamatan ---
    kecamatan_lokasi = titik["kecamatan"]
    baris_kec = kec_nir[kec_nir["kecamatan"] == kecamatan_lokasi]
    if len(baris_kec):
        b = baris_kec.iloc[0]
        with st.container(border=True, key="kartu_rujukan_kecamatan"):
            st.markdown(f'<div class="label-kecil">Rujukan: kecamatan {kecamatan_lokasi}</div>', unsafe_allow_html=True)
            st.write(
                f"Nilai tengah kecamatan ini (dari kerja zonasi purwarupa, "
                f"dasar: {'transaksi riil' if b['dasar']=='transaksi' else 'estimasi model, data tipis'}, "
                f"n = {int(b['n_tx'])} transaksi): **Rp{b['nir']:,.0f} / m²**"
            )
            if b["dasar"] != "transaksi":
                st.caption(
                    "Kecamatan ini datanya tipis (kurang dari 3 transaksi riil), jadi rujukan di atas "
                    "juga berbasis estimasi model, bukan transaksi riil."
                )
            st.caption(
                "Rujukan ini konteks pembanding tingkat kecamatan, bukan validasi bahwa indikasi per bidang "
                "di atas benar. Menetapkan ZNT dan NIR resmi dari kumpulan indikasi per bidang seperti ini "
                "adalah proses tersendiri yang jadi kewenangan dan pekerjaan BPPRD."
            )

st.write("")
with st.expander("Keterbatasan yang perlu diketahui sebelum memakai angka ini"):
    st.markdown(
        """
- Model diuji dengan cross-validation dan menghasilkan **COD 34,38-39,00** per bidang,
  gagal memenuhi ambang praktik terbaik IAAO (COD 5-20 untuk kategori tanah kosong).
  PMK 85/2024 sendiri tidak menetapkan ambang COD/PRD/PRB, jadi ini bukan pelanggaran
  regulasi, tapi tetap keterbatasan akurasi yang nyata dan harus disadari pemakai.
- MAPE model berkisar 43-49% tergantung skema pengujian. Untuk satu bidang spesifik,
  simpangan indikasi dari nilai pasar sebenarnya bisa cukup besar.
- Fitur jarak jaringan jalan pada kalkulator ini dipinjam dari titik grid prediksi
  terdekat (grid 500 meter), bukan dihitung ulang presisi untuk lokasi persis yang
  ditandai.
- Random Forest tidak bisa diandalkan untuk memprediksi kombinasi input yang jauh di
  luar rentang data 196 bidang yang dipakai melatihnya.
- Faktor penentu nilai di atas adalah aproksimasi SHAP yang dikonversi dari skala
  logaritmik ke rupiah untuk kemudahan baca, bukan dekomposisi rupiah yang presisi.
        """
    )
