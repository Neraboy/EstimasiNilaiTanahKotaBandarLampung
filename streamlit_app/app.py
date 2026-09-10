"""
Kalkulator Indikasi Awal Nilai Tanah -- Kota Bandar Lampung
Purwarupa skripsi, BUKAN alat penetapan NJOP/ZNT/NIR resmi.
"""
import json
import os

import folium
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "data")

st.set_page_config(page_title="Kalkulator Indikasi Nilai Tanah - Bandar Lampung", layout="wide")


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


model, info = load_model()
grid = load_grid()
kec_nir = load_kecamatan_nir()
zona_geojson = load_zona_geojson()

FITUR = info["FITUR"]
JARAK_COLS = [
    "jarak_ke_transportasi", "jarak_ke_pendidikan", "jarak_ke_pemerintahan",
    "jarak_ke_kolektor_sekunder", "jarak_ke_kolektor_primer", "jarak_ke_kesehatan",
    "jarak_ke_CBD", "jarak_ke_arteri_sekunder", "jarak_ke_arteri_primer",
]

# Rentang data latih, untuk peringatan ekstrapolasi (lihat catatan di bagian bawah halaman)
RENTANG_LATIH = {
    "luas": (56, 10000),
    "latitude": (-5.47485144929159, -5.34246958998922),
    "longitude": (105.190345574862, 105.333857363892),
}

st.title("Kalkulator Indikasi Awal Nilai Tanah")
st.caption("Purwarupa skripsi | Kota Bandar Lampung | Model Random Forest")

st.warning(
    "**Ini BUKAN alat penetapan NJOP, ZNT, atau NIR resmi.** Angka yang keluar dari "
    "kalkulator ini adalah indikasi awal untuk satu bidang berdasarkan model machine "
    "learning skripsi. Menurunkan indikasi ini menjadi ZNT dan NIR resmi adalah proses "
    "dan kewenangan BPPRD sendiri, bukan keluaran otomatis dari alat ini."
)

col_form, col_map = st.columns([1, 1.3])

with col_form:
    st.subheader("1. Data bidang")
    luas = st.number_input(
        "Luas tanah (m²)", min_value=1, max_value=100000, value=170, step=1,
        help=f"Rentang data latih model: {RENTANG_LATIH['luas'][0]:,} - {RENTANG_LATIH['luas'][1]:,} m². "
             "Di luar rentang ini, model melakukan ekstrapolasi dan hasilnya kurang bisa diandalkan.",
    )
    jenis_hak = st.selectbox("Jenis hak", ["SHM", "SHGB"])
    zonasi = st.selectbox("Zonasi (RTRW)", ["Permukiman", "NonPermukiman"])
    banjir = st.radio("Riwayat rawan banjir di lokasi ini?", ["Tidak", "Ya"], horizontal=True)
    longsor = st.radio("Riwayat rawan longsor di lokasi ini?", ["Tidak", "Ya"], horizontal=True)

    st.subheader("2. Lokasi bidang")
    st.caption("Klik peta di sebelah kanan untuk menandai lokasi, atau isi koordinat manual di bawah.")
    lat_manual = st.number_input("Lintang (latitude)", value=-5.4295, format="%.6f")
    lon_manual = st.number_input("Bujur (longitude)", value=105.2625, format="%.6f")

with col_map:
    st.subheader("Peta referensi kecamatan")
    try:
        CARTO_KEY = st.secrets.get("CARTO_API_KEY", "")
    except Exception:
        CARTO_KEY = ""
    tile_url = "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
    if CARTO_KEY:
        tile_url += f"?key={CARTO_KEY}"
    else:
        st.caption(
            "Peta dasar belum diberi API key CARTO, jadi bisa muncul watermark "
            "\"API KEY REQUIRED\". Tambahkan CARTO_API_KEY di Settings > Secrets "
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
    map_state = st_folium(m, height=480, width=None, key="peta_lokasi")

    if map_state and map_state.get("last_clicked"):
        lat_manual = map_state["last_clicked"]["lat"]
        lon_manual = map_state["last_clicked"]["lng"]
        st.info(f"Lokasi dari klik peta: {lat_manual:.6f}, {lon_manual:.6f}")

st.divider()

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

    st.subheader("Hasil")
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
        st.error(p)

    # --- Rujukan nilai tengah kecamatan ---
    kecamatan_lokasi = titik["kecamatan"]
    baris_kec = kec_nir[kec_nir["kecamatan"] == kecamatan_lokasi]
    if len(baris_kec):
        b = baris_kec.iloc[0]
        st.subheader(f"Rujukan: kecamatan {kecamatan_lokasi}")
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

st.divider()
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
        """
    )
