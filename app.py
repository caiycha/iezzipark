
import streamlit as st
import random
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(page_title="Smart Parking System - Ultimate Dashboard", page_icon="🅿️", layout="centered")

# Custom CSS untuk Tampilan Dashboard Profesional
st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .header-container {
        text-align: center;
        padding: 15px 0;
    }
    .main-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #38bdf8;
        margin-top: 5px;
    }
    .dashboard-card {
        background: #1e293b;
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
    }
    .receipt-box {
        background: #f8fafc;
        color: #0f172a;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #0284c7;
        font-family: monospace;
    }
    .stButton>button {
        width: 100%;
        background: #0284c7;
        color: white;
        border: none;
        padding: 12px;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background: #0369a1;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER / MENU UTAMA ---
st.markdown("""
    <div class="header-container">
        <h1 style="font-size: 45px; margin: 0;">🚗🔍</h1>
        <p class="main-title">Smart Parking Management System</p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# Navigasi Menu Atas (Simulasi Dashboard)
menu_pilihan = st.radio("Pilih Menu Sistem:", ["📝 Pintu Masuk (Entry Gate)", "💳 Pembayaran & Keluar (Exit Gate)", "📊 Dashboard Admin"], horizontal=True)

st.write("")

# --- MENU 1: ENTRY GATE ---
if menu_pilihan == "📝 Pintu Masuk (Entry Gate)":
    st.subheader("📥 Pendaftaran & Masuk Kendaraan")
    
    with st.form("entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            nama_driver = st.text_input("Nama Pengemudi:", "Nafes")
            plat_nomor = st.text_input("Nomor Plat Kendaraan:", "B 1234 XYZ")
        with col2:
            tipe_kendaraan = st.selectbox("Jenis Kendaraan:", [
                "🚗 Mobil Standar (Bensin/Diesel)", 
                "⚡ Mobil Listrik (EV Charging)", 
                "🚙 SUV / Kendaraan Besar"
            ])
            lantai_tujuan = st.selectbox("Zona Parkir:", ["Lantai P1 - Zona A (Regular)", "Lantai P2 - Zona B (VIP)", "Lantai P3 - Zona EV Charging"])
        
        submit_entry = st.form_submit_button("Cetak Karcis & Alokasikan Slot 🚀")
        
        if submit_entry:
            waktu_masuk = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            nomor_slot_parkir = random.randint(10, 99)
            
            st.success("✅ Kendaraan Berhasil Terdaftar!")
            st.markdown(f"""
                <div class="dashboard-card">
                    <h4 style="color: #38bdf8; margin-top: 0;">🎟️ Karcis Masuk Digital</h4>
                    <p><b>Waktu Masuk:</b> {waktu_masuk}</p>
                    <p><b>Pengemudi:</b> {nama_driver} ({plat_nomor})</p>
                    <p><b>Kendaraan:</b> {tipe_kendaraan}</p>
                    <p><b>Lokasi Slot:</b> {lantai_tujuan} (Slot No. #{nomor_slot_parkir})</p>
                </div>
            """, unsafe_allow_html=True)

# --- MENU 2: EXIT GATE & KALKULATOR LKPD ---
elif menu_pilihan == "💳 Pembayaran & Keluar (Exit Gate)":
    st.subheader("📤 Kalkulator Tarif & Pembayaran Parkir")
    
    plat_keluar = st.text_input("Masukkan Nomor Plat Kendaraan Saat Keluar:", "B 1234 XYZ")
    jam_parkir = st.slider("Pilih Durasi Waktu Parkir (Jam):", min_value=1, max_value=24, value=6)
    
    metode_bayar = st.selectbox("Pilih Metode Pembayaran Non-Tunai:", [
        "📱 QRIS (GoPay/OVO/Dana)", 
        "💳 Kartu Member / E-Money", 
        "💵 Tunai (Cash)"
    ])

    # Logika Tarif LKPD
    def hitung_tarif(jam):
        if jam <= 1:
            biaya = 5000
        else:
            biaya = 5000 + (jam - 1) * 3000
        
        diskon = 0
        if jam > 5:
            diskon = 2000
            biaya -= diskon
            
        return biaya, diskon

    if st.button("Proses Pembayaran & Cetak Struk 🖨️"):
        total_biaya, diskon_didapat = hitung_tarif(jam_parkir)
        waktu_keluar = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        st.write("")
        st.markdown(f"""
            <div class="receipt-box">
                <h3 style="text-align: center; margin-top: 0; color: #0284c7;">STRUK RESMI PARKIR</h3>
                <hr style="border: 1px dashed #cbd5e1;">
                <p><b>Waktu Keluar:</b> {waktu_keluar}</p>
                <p><b>Plat Nomor:</b> {plat_keluar}</p>
                <p><b>Durasi Parkir:</b> {jam_parkir} Jam</p>
                <p><b>Potongan Diskon:</b> Rp {diskon_didapat:,}</p>
                <hr style="border: 1px dashed #cbd5e1;">
                <h3 style="color: #16a34a; text-align: center;">TOTAL BAYAR: Rp {total_biaya:,}</h3>
                <p style="text-align: center; font-size: 0.85rem; color: #64748b;">Metode: {metode_bayar} - LUNAS</p>
            </div>
        """, unsafe_allow_html=True)
        
        if jam_parkir > 5:
            st.info("💡 Selamat! Anda mendapatkan potongan diskon Rp 2.000 karena durasi parkir lebih dari 5 jam.")

# --- MENU 3: DASHBOARD ADMIN ---
else:
    st.subheader("📊 Dashboard Admin & Rekapitulasi")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric(label="Total Kendaraan Masuk Hari Ini", value="142 Unit", delta="+12%")
    with col_m2:
        st.metric(label="Slot Parkir Kosong", value="58 Slot", delta="-5%")
    with col_m3:
        st.metric(label="Estimasi Pendapatan Harian", value="Rp 2.850.000", delta="+18%")
        
    st.divider()
    st.subheader("📈 Statistik Penggunaan Kendaraan")
    
    # Grafik dummy sederhana menggunakan chart bawaan Streamlit
    chart_data = {"Mobil Standar": 85, "SUV / Besar": 32, "Mobil Listrik (EV)": 25}
    st.bar_chart(chart_data)
