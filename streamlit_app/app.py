"""
Indikasi Awal Nilai Tanah -- Kota Bandar Lampung
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

st.set_page_config(page_title="Purwarupa Indikasi Nilai Pasar Tanah - Bandar Lampung", layout="wide")

# --- Gaya visual, lihat DESIGN.md untuk penjelasan lengkap palet, tipografi, dan alasan
# penolakan SF Pro/Gotham (lisensi). PENTING: st.markdown menjalankan parser markdown
# lebih dulu sebelum unsafe_allow_html menyisipkan HTML mentahnya, jadi blok <style> di
# bawah ini SENGAJA tidak diberi komentar CSS prosa (terutama yang memuat tanda hubung
# ganda atau tanda bintang tunggal seperti selektor "*"): markdown mengubah "--" jadi en
# dash dan bisa memakan tanda bintang sebagai penanda italic, yang pernah membuat sisa
# CSS di bawahnya ikut terpotong/hilang saat dirender. Semua penjelasan ada di DESIGN.md.
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
    :root {
        --bg: #f4f4f0; --panel: #ffffff; --ink: #10233f; --ink-soft: #55627d;
        --border: #d7dbe3; --gold: #8a6d16; --btn-bg: #10233f; --btn-text: #f4f4f0;
        --positive: #2f7d5c; --negative: #b23a2c;
        --warn-bg: #fbf1da; --warn-border: #b8912f; --warn-ink: #6b4e08;
        --faktor-track: #ecebe4;
        --font-header: "Nunito", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        --font-body: "Nunito", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        --sp-xxs: 2px; --sp-xs: 4px; --sp-sm: 8px; --sp-md: 16px; --sp-lg: 24px;
        --sp-xl: 32px; --sp-section: 48px;
        --tex-opacity: 1;
    }
    @media (prefers-color-scheme: dark) {
        :root {
            --bg: #000000; --panel: #141414; --ink: #f2f0e6; --ink-soft: #a8a8a8;
            --border: #2c2c2c; --gold: #e8cf6b; --btn-bg: #c9a227; --btn-text: #10233f;
            --positive: #4fbf82; --negative: #e2604a;
            --warn-bg: #2c2410; --warn-border: #c9a227; --warn-ink: #f0d998;
            --faktor-track: #1e1e1e;
            --tex-opacity: 1;
        }
    }
    body, p, span, div, label, li { font-family: var(--font-body); }
    h1, h2, h3 {
        color: var(--ink) !important; font-family: var(--font-header) !important;
        font-weight: 700 !important;
    }
    .block-container { padding-top: var(--sp-xl); }
    div[class*="st-key-kartu"] {
        background: var(--panel) !important; border: 1px solid var(--border) !important;
        border-radius: 10px !important;
    }
    div[class*="st-key-kartu_rujukan_kecamatan_bahaya"] {
        background: var(--warn-bg) !important; border: 1px solid var(--warn-border) !important;
        border-radius: 10px !important;
    }
    div[class*="st-key-kartu_rujukan_kecamatan"] {
        padding: 12px 18px 20px 18px !important;
    }
    div[class*="st-key-kartu_rujukan_kecamatan"] [data-testid="stVerticalBlock"] {
        gap: 0.35rem !important;
    }
    div[class*="st-key-kartu_rujukan_kecamatan"] .element-container {
        margin: 0 !important;
    }
    .label-kecil {
        font-family: var(--font-body); font-size: 12.5px; font-weight: 600; letter-spacing: .4px;
        text-transform: uppercase; color: var(--ink); margin-bottom: var(--sp-xs);
    }
    .peringatan-disclaimer {
        background: var(--warn-bg); border: 1px solid var(--warn-border); border-radius: 10px;
        padding: var(--sp-sm) var(--sp-md); color: var(--warn-ink); font-size: 14px; line-height: 1.55;
        margin-top: var(--sp-sm); margin-bottom: var(--sp-xxs);
    }
    .rujukan-baris {
        font-size: 14px; color: var(--ink); line-height: 1.6; margin: var(--sp-xxs) 0;
    }
    .hasil-angka { font-size: 30px; font-weight: 700; color: var(--gold); margin: var(--sp-xxs) 0; }
    .hasil-sub { font-size: 12.5px; color: var(--ink-soft); }
    .hasil-dasar {
        font-size: 13.5px; color: var(--ink-soft); padding: var(--sp-sm) 0 var(--sp-md) 0;
        border-bottom: 1px solid var(--border); margin-bottom: var(--sp-sm);
    }
    .faktor-baris {
        display: flex; align-items: center; gap: var(--sp-sm); margin: var(--sp-xs) 0; font-size: 13.5px;
    }
    .faktor-nama { width: 230px; flex: none; color: var(--ink); }
    .faktor-bar-wrap { flex: 1; background: var(--faktor-track); border-radius: 4px; height: 18px; position: relative; }
    .faktor-bar { height: 18px; border-radius: 4px; }
    .faktor-nilai { width: 130px; flex: none; text-align: right; font-weight: 600; font-size: 13px; }
    iframe[title="streamlit_folium.st_folium"] {
        border-radius: 10px; overflow: hidden; border: 1px solid var(--border);
    }
    div.stButton > button[kind="primary"] {
        background: var(--btn-bg); border: none; border-radius: 6px; color: var(--btn-text);
        font-family: var(--font-body); font-weight: 600; transition: filter 0.1s ease;
    }
    div.stButton > button[kind="primary"]:hover { filter: brightness(0.94); }
    div.stButton > button[kind="primary"]:active { filter: brightness(0.85); }
    [data-testid="stMetric"] {
        background: var(--panel); border: 1px solid var(--border); border-radius: 10px;
        padding: var(--sp-sm) var(--sp-md);
    }
    [data-testid="stMetricValue"] { color: var(--gold) !important; }
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
def load_grid_kemiling_padat():
    path = os.path.join(DATA, "grid_lookup_kemiling_100m.csv")
    return pd.read_csv(path) if os.path.exists(path) else None


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
grid_kemiling_padat = load_grid_kemiling_padat()
kec_nir = load_kecamatan_nir()
zona_geojson = load_zona_geojson()
explainer = load_shap_explainer(model)

FITUR = info["FITUR"]
JARAK_COLS = [
    "jarak_ke_transportasi", "jarak_ke_pendidikan", "jarak_ke_pemerintahan",
    "jarak_ke_kolektor_sekunder", "jarak_ke_kolektor_primer", "jarak_ke_kesehatan",
    "jarak_ke_CBD", "jarak_ke_arteri_sekunder", "jarak_ke_arteri_primer",
]
# MAPE hasil spatial block cross-validation (situasi ekstrapolasi), dipakai sebagai
# lebar rentang indikasi nilai. Bukan selang kepercayaan statistik formal, cuma
# perkiraan kasar dari rata-rata simpangan persen model saat diuji pada kecamatan
# yang tidak pernah dilihatnya. Lihat Status_Skripsi.md Bagian 4.1.
MAPE_SPATIAL = 0.4919


def warna_gradien_data(n_transaksi, n_maks=15):
    """Merah (data pembanding sedikit) ke hijau (data pembanding banyak), dibatasi n_maks."""
    lo = (178, 58, 44)
    hi = (47, 125, 92)
    t = min(n_transaksi / n_maks, 1.0)
    r = round(lo[0] + (hi[0] - lo[0]) * t)
    g = round(lo[1] + (hi[1] - lo[1]) * t)
    b = round(lo[2] + (hi[2] - lo[2]) * t)
    return f"#{r:02x}{g:02x}{b:02x}"

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

st.title("Purwarupa Indikasi Awal Nilai Pasar Tanah")
st.caption("Purwarupa ini merupakan implementasi model machine learning berupa Random Forest untuk mengestimasi nilai tanah Kota Bandar Lampung")

st.markdown(
    """
    <div class="peringatan-disclaimer">
    <b>Ini BUKAN alat penetapan NJOP, ZNT, atau NIR resmi.</b> Angka yang keluar dari
    purwarupa ini adalah indikasi awal untuk satu bidang berdasarkan model machine
    learning. Menurunkan indikasi nilai awal ini menjadi NJOP/ZNT/NIR resmi adalah
    proses dan kewenangan BPPRD sendiri. Alat ini dirancang sebagai alat bantu untuk
    indikasi nilai awal.
    </div>
    """,
    unsafe_allow_html=True,
)
st.write("")

col_form, col_map = st.columns([1, 1.3])

with col_form:
    with st.container(border=True, key="kartu_luas_bidang"):
        st.markdown('<div class="label-kecil">1. Luas bidang</div>', unsafe_allow_html=True)
        luas = st.number_input(
            "Luas tanah (m²)", value=170, step=1,
            help=f"Rentang data latih model: {RENTANG_LATIH['luas'][0]:,} - {RENTANG_LATIH['luas'][1]:,} m². "
                 "Di luar rentang ini, model melakukan ekstrapolasi dan hasilnya kurang bisa diandalkan.",
        )

    with st.container(border=True, key="kartu_data_bidang"):
        st.markdown('<div class="label-kecil">2. Data bidang lainnya</div>', unsafe_allow_html=True)
        jenis_hak = st.selectbox("Jenis hak", ["SHM", "SHGB"])
        zonasi = st.selectbox("Zonasi (RTRW)", ["Permukiman", "NonPermukiman"])
        banjir = st.radio("Riwayat rawan banjir di lokasi ini?", ["Tidak", "Ya"], horizontal=True)
        longsor = st.radio("Riwayat rawan longsor di lokasi ini?", ["Tidak", "Ya"], horizontal=True)

    with st.container(border=True, key="kartu_lokasi_bidang"):
        st.markdown('<div class="label-kecil">3. Lokasi bidang</div>', unsafe_allow_html=True)
        sumber_lokasi = st.radio(
            "Sumber koordinat",
            ["Klik peta", "Input manual"],
            horizontal=True,
            help="Pilih salah satu. Kalau \"Klik peta\" dipilih, angka lintang/bujur di bawah "
                 "diabaikan dan lokasi dari titik yang kamu klik di peta yang dipakai -- begitu "
                 "juga sebaliknya, supaya tidak tertukar antara dua sumber koordinat.",
        )
        lat_input = st.number_input(
            "Lintang (latitude)", value=-5.4295, format="%.6f",
            disabled=(sumber_lokasi == "Klik peta"),
            help="Posisi utara-selatan di bumi, dalam derajat desimal. Nilai negatif berarti "
                 "di belahan bumi selatan (Bandar Lampung sekitar -5,4 derajat).",
        )
        lon_input = st.number_input(
            "Bujur (longitude)", value=105.2625, format="%.6f",
            disabled=(sumber_lokasi == "Klik peta"),
            help="Posisi barat-timur di bumi, dalam derajat desimal. Bandar Lampung sekitar "
                 "105,2 derajat (di sebelah timur garis 0 derajat yang melewati Greenwich).",
        )

with col_map:
    st.markdown('<div class="label-kecil">Peta referensi kecamatan</div>', unsafe_allow_html=True)
    st.caption(
        "Warna zona menunjukkan jumlah transaksi pembanding, bukan tinggi rendahnya harga. "
        "Semakin hijau, semakin banyak data pembanding dan semakin dapat diandalkan. Semakin "
        "merah, semakin sedikit data pembanding dan indikasi nilainya semakin berpotensi "
        "meleset jauh. Arahkan kursor ke tiap zona untuk melihat jumlah data pembanding "
        "kecamatan tersebut."
    )
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
    if "titik_klik_peta" not in st.session_state:
        st.session_state["titik_klik_peta"] = None

    m = folium.Map(location=[-5.4295, 105.2625], zoom_start=12, tiles=None)
    folium.TileLayer(
        tiles=tile_url,
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains="abcd",
        max_zoom=19,
    ).add_to(m)
    # Warna zona mengikuti jumlah transaksi pembanding (n_transaksi). Tooltip cuma
    # menampilkan kecamatan dan jumlah data pembanding, tidak ada lagi angka NIR
    # (dihapus total per keputusan 13 September, lihat Status_Skripsi.md Bagian 5).
    folium.GeoJson(
        zona_geojson,
        name="Kecamatan",
        style_function=lambda f: {
            "fillColor": warna_gradien_data(f["properties"].get("n_transaksi", 0)),
            "color": "#5a4a2f",
            "weight": 1,
            "fillOpacity": 0.55,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["kecamatan", "n_transaksi"],
            aliases=["Kecamatan:", "Data pembanding:"],
        ),
    ).add_to(m)
    if st.session_state["titik_klik_peta"]:
        folium.Marker(
            location=st.session_state["titik_klik_peta"],
            icon=folium.Icon(color="red", icon="map-pin", prefix="fa"),
        ).add_to(m)
    map_state = st_folium(m, height=430, width=None, key="peta_lokasi")

    if map_state and map_state.get("last_clicked"):
        titik_baru = (map_state["last_clicked"]["lat"], map_state["last_clicked"]["lng"])
        if titik_baru != st.session_state["titik_klik_peta"]:
            st.session_state["titik_klik_peta"] = titik_baru
            st.rerun()

    if st.session_state["titik_klik_peta"]:
        st.caption(
            f"Lokasi dari klik peta: {st.session_state['titik_klik_peta'][0]:.6f}, "
            f"{st.session_state['titik_klik_peta'][1]:.6f}"
        )
    elif sumber_lokasi == "Klik peta":
        st.caption("Belum ada titik yang diklik di peta.")

if sumber_lokasi == "Klik peta" and st.session_state["titik_klik_peta"]:
    lat_manual, lon_manual = st.session_state["titik_klik_peta"]
else:
    lat_manual, lon_manual = lat_input, lon_input

st.write("")
hitung = st.button("Hitung indikasi nilai", type="primary", use_container_width=True)

BATAS_JARAK_GRID_M = 5000  # di atas ini, lokasi dianggap mustahil berada di wilayah studi
LUAS_MIN_M2 = 1
LUAS_MAKS_M2 = 100000

if hitung and not (LUAS_MIN_M2 <= luas <= LUAS_MAKS_M2):
    st.error(
        f"Luas {luas:,.0f} m² tidak valid. Masukkan luas tanah antara {LUAS_MIN_M2:,} dan "
        f"{LUAS_MAKS_M2:,} m². Purwarupa tidak menghitung indikasi nilai untuk angka ini, "
        "periksa kembali luas yang dimasukkan."
    )
    st.stop()

if hitung:
    # --- Cari titik grid terdekat untuk meminjam 9 fitur jarak jaringan jalan ---
    d2 = (grid["latitude"] - lat_manual) ** 2 + (grid["longitude"] - lon_manual) ** 2
    idx_terdekat = d2.idxmin()
    titik = grid.loc[idx_terdekat]
    jarak_ke_titik_m = np.sqrt(d2.loc[idx_terdekat]) * 111000  # derajat -> meter, aproksimasi kasar

    if jarak_ke_titik_m > BATAS_JARAK_GRID_M:
        st.error(
            f"Lokasi yang ditandai berjarak sekitar {jarak_ke_titik_m/1000:,.0f} km dari titik "
            "referensi grid terdekat, jauh di luar wilayah Kota Bandar Lampung yang dicakup model. "
            "Purwarupa tidak menghitung indikasi nilai untuk lokasi ini. Periksa kembali koordinat "
            "yang dimasukkan."
        )
        st.stop()

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

    # --- Perbandingan opsional: grid referensi lebih rapat (100 m, khusus Kemiling) ---
    # Proof-of-concept sidang, lihat Status_Skripsi.md Bagian 4.3. Cuma aktif kalau
    # lokasi yang ditandai jatuh dekat cakupan grid padat itu (dalam radius 150 meter
    # dari titik grid terdekatnya) -- otomatis nonaktif di luar itu, tidak perlu
    # deteksi batas kecamatan terpisah.
    pred_padat_per_m2 = None
    jarak_ke_titik_padat_m = None
    if grid_kemiling_padat is not None:
        d2_padat = (
            (grid_kemiling_padat["latitude"] - lat_manual) ** 2
            + (grid_kemiling_padat["longitude"] - lon_manual) ** 2
        )
        idx_padat = d2_padat.idxmin()
        jarak_ke_titik_padat_m = np.sqrt(d2_padat.loc[idx_padat]) * 111000
        if jarak_ke_titik_padat_m <= 150:
            titik_padat = grid_kemiling_padat.loc[idx_padat]
            baris_padat = dict(baris)
            for c in JARAK_COLS:
                baris_padat[c] = titik_padat[c]
            X_padat = pd.DataFrame([baris_padat])[FITUR]
            pred_padat_per_m2 = float(np.exp(model.predict(X_padat)[0]))

    batas_bawah_m2 = pred_per_m2 * (1 - MAPE_SPATIAL)
    batas_atas_m2 = pred_per_m2 * (1 + MAPE_SPATIAL)
    batas_bawah_total = batas_bawah_m2 * luas
    batas_atas_total = batas_atas_m2 * luas

    with st.container(border=True, key="kartu_hasil"):
        st.markdown('<div class="label-kecil">Hasil (Grid 500m)</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.metric("Indikasi awal nilai per m²", f"Rp{pred_per_m2:,.0f}")
        c2.metric("Indikasi awal total bidang", f"Rp{pred_total:,.0f}")
        st.markdown(
            f'<div class="hasil-sub" style="margin-top:8px;">Rentang per m²: '
            f"Rp{batas_bawah_m2:,.0f} sampai Rp{batas_atas_m2:,.0f}</div>"
            f'<div class="hasil-sub">Rentang total bidang: '
            f"Rp{batas_bawah_total:,.0f} sampai Rp{batas_atas_total:,.0f}</div>",
            unsafe_allow_html=True,
        )
        st.caption(
            "Rentang ini dari MAPE hasil spatial block cross-validation (49,19%), bukan "
            "selang kepercayaan statistik formal. Anggap sebagai perkiraan kasar seberapa "
            "jauh indikasi di atas bisa meleset dari harga sebenarnya."
        )
        st.caption(
            f"Fitur jarak jaringan jalan dipinjam dari titik referensi grid terdekat "
            f"(~{jarak_ke_titik_m:,.0f} meter dari lokasi yang ditandai), bukan dihitung ulang presisi "
            "untuk lokasi persis ini."
        )

    if pred_padat_per_m2 is not None:
        pred_padat_total = pred_padat_per_m2 * luas
        batas_bawah_padat_m2 = pred_padat_per_m2 * (1 - MAPE_SPATIAL)
        batas_atas_padat_m2 = pred_padat_per_m2 * (1 + MAPE_SPATIAL)
        batas_bawah_padat_total = batas_bawah_padat_m2 * luas
        batas_atas_padat_total = batas_atas_padat_m2 * luas

        with st.container(border=True, key="kartu_hasil_padat"):
            st.markdown('<div class="label-kecil">Hasil (Grid 100m)</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.metric("Indikasi awal nilai per m²", f"Rp{pred_padat_per_m2:,.0f}")
            c2.metric("Indikasi awal total bidang", f"Rp{pred_padat_total:,.0f}")
            st.markdown(
                f'<div class="hasil-sub" style="margin-top:8px;">Rentang per m²: '
                f"Rp{batas_bawah_padat_m2:,.0f} sampai Rp{batas_atas_padat_m2:,.0f}</div>"
                f'<div class="hasil-sub">Rentang total bidang: '
                f"Rp{batas_bawah_padat_total:,.0f} sampai Rp{batas_atas_padat_total:,.0f}</div>",
                unsafe_allow_html=True,
            )
            st.caption(
                "Rentang ini dari MAPE hasil spatial block cross-validation (49,19%), bukan "
                "selang kepercayaan statistik formal. Anggap sebagai perkiraan kasar seberapa "
                "jauh indikasi di atas bisa meleset dari harga sebenarnya."
            )
            st.caption(
                f"Fitur jarak jaringan jalan dipinjam dari titik referensi grid terdekat "
                f"(~{jarak_ke_titik_padat_m:,.0f} meter dari lokasi yang ditandai), bukan dihitung ulang "
                "presisi untuk lokasi persis ini."
            )

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
            "Menunjukkan enam faktor dengan pengaruh terbesar terhadap indikasi nilai per m² di atas "
            "dalam perkiraan rupiah. Hijau *menaikkan* nilai, merah *menurunkan* nilai."
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
            "di atas (jumlah totalnya tidak dijamin pas sama dengan indikasi nilai akhir karena model "
            "dilatih pada skala logaritmik)."
        )

    # --- Rujukan data pembanding kecamatan ---
    kecamatan_lokasi = titik["kecamatan"]
    baris_kec = kec_nir[kec_nir["kecamatan"] == kecamatan_lokasi]
    if len(baris_kec):
        b = baris_kec.iloc[0]
        n_tx = int(b["n_tx"])
        ada_data = n_tx > 0
        kelas_kartu = "kartu_rujukan_kecamatan" if ada_data else "kartu_rujukan_kecamatan_bahaya"
        with st.container(border=True, key=kelas_kartu):
            st.markdown(
                f'<div class="rujukan-baris">Kecamatan: <strong>{kecamatan_lokasi}</strong></div>'
                f'<div class="rujukan-baris">Data pembanding: <strong>{n_tx}</strong></div>',
                unsafe_allow_html=True,
            )
            if not ada_data:
                st.markdown(
                    '<div class="peringatan-disclaimer">PERHATIAN: Tidak ada data transaksi pembanding '
                    "di kecamatan ini, indikasi nilai bidang sepenuhnya berasal dari model, gunakan "
                    "dengan hati-hati.</div>",
                    unsafe_allow_html=True,
                )

st.write("")
with st.expander("Keterbatasan yang perlu diketahui sebelum memakai angka ini"):
    st.markdown(
        """
**Apa arti R², RMSE, dan MAPE:**
- R² mengukur seberapa representatif model menjelaskan variasi harga tanah, dari 0
  sampai 1. Makin dekat ke 1, makin banyak variasi harga yang berhasil dijelaskan model.
- RMSE (Root Mean Square Error) adalah rata-rata simpangan prediksi terhadap harga
  sebenarnya, dalam rupiah per m², dengan bobot lebih berat untuk simpangan yang besar.
- MAPE (Mean Absolute Percentage Error) adalah rata-rata simpangan prediksi terhadap
  harga sebenarnya, dalam persen, tanpa bobot ekstra untuk simpangan besar.

**Hasil 5-fold cross-validation (interpolasi):**
- R² skala ln **0,5114**, skala rupiah **0,4161**
- RMSE **Rp563.931/m²**
- MAPE **43,07%**

**Hasil spatial block cross-validation per kecamatan (ekstrapolasi):**
- R² skala ln **0,3659**, skala rupiah **0,1364**
- RMSE **Rp691.171/m²**
- MAPE **49,19%**

**R² in-sample (model diuji pada data yang sama dipakai melatihnya):**
- R² skala ln **0,9246**, skala rupiah **0,8486**
- RMSE **Rp287.175/m²**
- MAPE **15,63%**

**Uji IAAO, 5-fold CV (interpolasi):**
- COD **34,38** (ambang 5-20)
- PRD **1,2068** (ambang 0,98-1,03)
- PRB **-0,1813** (ambang -0,05 s.d. 0,05)
- Ketiganya gagal ambang.

**Uji IAAO, spatial block CV per kecamatan (ekstrapolasi):**
- COD **39,00** (ambang 5-20)
- PRD **1,3383** (ambang 0,98-1,03)
- PRB **-0,4448** (ambang -0,05 s.d. 0,05)
- Ketiganya gagal ambang.

**Keterbatasan lain:**
- Fitur jarak jaringan jalan pada purwarupa ini dipinjam dari titik grid prediksi
  terdekat (grid 500 meter), bukan dihitung ulang presisi untuk lokasi persis yang
  ditandai.
- Random Forest tidak bisa diandalkan untuk memprediksi kombinasi input yang jauh di
  luar rentang data 196 bidang yang dipakai melatihnya.
- Faktor penentu nilai di atas adalah aproksimasi SHAP yang dikonversi dari skala
  logaritmik ke rupiah untuk kemudahan baca, bukan dekomposisi rupiah yang presisi.
        """
    )
