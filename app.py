import streamlit as st

# Konfigurasi Halaman & Tema Minimalis Elegan
st.set_page_config(page_title="Velora // Smart Parking", page_icon="🅿️", layout="centered")

# Custom CSS untuk Tampilan Clean, Modern, & Chill (Dark/Light Balance)
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 0.95rem;
        margin-bottom: 30px;
    }
    .card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(51, 65, 85, 0.6);
        padding: 20px;
        border-radius: 16px;
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #0284c7 0%, #6366f1 100%);
        color: white;
        border: none;
        padding: 12px;
        border-radius: 10px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Header Halaman
st.markdown('<p class="main-title">Velora Parking Space</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Sistem kalkulasi tarif otomatis dengan presisi tinggi.</p>', unsafe_allow_html=True)

# Container Input Data
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📋 Informasi Kendaraan")
    
    col1, col2 = st.columns(2)
    with col1:
        nama = st.text_input("Nama Pengemudi", "Nafes")
    with col2:
        plat = st.text_input("Nomor Kendaraan", "B 1234 XYZ")
        
    tipe_kendaraan = st.selectbox("Jenis Kendaraan", [
        "🚗 Mobil Standar", 
        "⚡ Mobil Listrik (EV)", 
        "🚙 SUV / Medium Vehicle"
    ])
    st.markdown('</div>', unsafe_allow_html=True)

# Container Kalkulator Durasi
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("⏱️ Durasi Parkir")
    jam_parkir = st.slider("Pilih Lama Waktu Parkir (Jam)", min_value=1, max_value=24, value=3)
    st.markdown('</div>', unsafe_allow_html=True)

# Logika Perhitungan Tarif Sesuai LKPD
if jam_parkir <= 1:
    total_biaya = 5000
else:
    total_biaya = 5000 + (jam_parkir - 1) * 3000

diskon = 0
if jam_parkir > 5:
    diskon = 2000
    total_biaya -= diskon

# Tombol Eksekusi & Hasil Interaktif
if st.button("Kalkulasi Tarif Sekarang 🚀"):
    st.divider()
    
    # Tampilan Metrik Estetik
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="Pengemudi", value=nama)
    with m2:
        st.metric(label="Durasi", value=f"{jam_parkir} Jam")
    with m3:
        st.metric(label="Diskon", value=f"Rp {diskon:,}")
        
    # Kotak Total Biaya Menarik
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #065f46 0%, #047857 100%); padding: 22px; border-radius: 14px; text-align: center; margin-top: 20px; box-shadow: 0 8px 25px rgba(5, 150, 105, 0.2);">
            <p style="margin: 0; color: #a7f3d0; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Total Biaya Akhir</p>
            <h1 style="margin: 5px 0 0 0; color: #ffffff; font-size: 2.5rem;">Rp {total_biaya:,}</h1>
        </div>
    """, unsafe_allow_html=True)
    
    if jam_parkir > 5:
        st.success("✨ Selamat! Anda mendapatkan potongan diskon sebesar Rp 2.000 karena durasi parkir lebih dari 5 jam.")
