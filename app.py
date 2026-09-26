import streamlit as st
import random
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(page_title="Smart Parking System - QR & Barcode", page_icon="🅿️", layout="centered")

# Custom CSS untuk Tampilan Modern & Grid Slot Parkir
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
    .slot-box-kosong {
        background-color: #064e3b;
        border: 1px solid #10b981;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        color: #6ee7b7;
        font-weight: bold;
    }
    .slot-box-penuh {
        background-color: #7f1d1d;
        border: 1px solid #ef4444;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        color: #fca5a5;
        font-weight: bold;
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

# --- HEADER UTAMA ---
st.markdown("""
    <div class="header-container">
        <h1 style="font-size: 45px; margin: 0;">🚗🅿️</h1>
        <p class="main-title">Smart Parking Management System</p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# Inisialisasi State untuk Status Slot Parkir
if 'slot_status' not in st.session_state:
    st.session_state.slot_status = {
        "A1": 0, "A2": 1, "A3": 0, "A4": 0,
        "B1": 1, "B2": 1, "B3": 0, "B4": 1,
        "VIP 1": 0, "VIP 2": 1
    }

# Navigasi Menu Atas
menu_pilihan = st.radio("Pilih Menu Sistem:", ["📝 Pintu Masuk", "💳 Pintu Keluar & Pembayaran", "🗺️ Denah Status Slot Parkir", "📊 Dashboard Admin"], horizontal=True)

st.write("")

# --- MENU 1: ENTRY GATE ---
if menu_pilihan == "📝 Pintu Masuk":
    st.subheader("📥 Pendaftaran & Masuk Kendaraan")
    
    with st.form("entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            nama_driver = st.text_input("Nama Pengemudi:", "Nafes")
            plat_nomor = st.text_input("Nomor Plat Kendaraan:", "B 1234 XYZ")
        with col2:
            tipe_kendaraan = st.selectbox("Jenis Kendaraan:", [
                "🚗 Mobil Standar", 
                "⚡ Mobil Listrik (EV)", 
                "🚙 SUV / Besar"
            ])
            slot_tersedia = [k for k, v in st.session_state.slot_status.items() if v == 0]
            pilih_slot = st.selectbox("Alokasi Slot Otomatis:", slot_tersedia if slot_tersedia else ["Semua Penuh!"])
        
        submit_entry = st.form_submit_button("Cetak Karcis & Update Slot 🚀")
        
        if submit_entry and slot_tersedia:
            st.session_state.slot_status[pilih_slot] = 1
            waktu_masuk = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            st.success(f"✅ Kendaraan Berhasil Masuk ke Slot **{pilih_slot}**!")
            st.markdown(f"""
                <div class="dashboard-card">
                    <h4 style="color: #38bdf8; margin-top: 0;">🎟️ Karcis Masuk Digital</h4>
                    <p><b>Waktu:</b> {waktu_masuk}</p>
                    <p><b>Driver:</b> {nama_driver} ({plat_nomor})</p>
                    <p><b>Slot Parkir:</b> {pilih_slot}</p>
                </div>
            """, unsafe_allow_html=True)
        elif submit_entry:
            st.error("Maaf, seluruh slot parkir sedang penuh!")

# --- MENU 2: EXIT GATE & PEMBAYARAN DENGAN BARCODE ---
elif menu_pilihan == "💳 Pintu Keluar & Pembayaran":
    st.subheader("📤 Kalkulator Tarif & Pembayaran Parkir")
    
    plat_keluar = st.text_input("Nomor Plat Kendaraan Keluar:", "B 1234 XYZ")
    jam_parkir = st.slider("Durasi Waktu Parkir (Jam):", min_value=1, max_value=24, value=6)
    
    metode_bayar = st.selectbox("Pilih Metode Pembayaran Non-Tunai / Tunai:", [
        "📱 QRIS (GoPay / OVO / Dana / BCA)", 
        "💳 Kartu Member / E-Money (Flazz / Mandiri e-Money)", 
        "💵 Tunai (Cash)"
    ])
    
    slot_terisi = [k for k, v in st.session_state.slot_status.items() if v == 1]
    slot_to_free = st.selectbox("Pilih Slot yang Dikosongkan:", slot_terisi if slot_terisi else ["Tidak ada kendaraan di dalam"])

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

    if st.button("Bayar & Cetak Struk Berbarcode 🖨️"):
        total_biaya, diskon_didapat = hitung_tarif(jam_parkir)
        if slot_terisi:
            st.session_state.slot_status[slot_to_free] = 0 
            
        waktu_keluar = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        token_transaksi = f"PARK-{random.randint(10000, 99999)}"
        
        # Layout Struk dan Barcode
        col_struk1, col_struk2 = st.columns([1.5, 1])
        
        with col_struk1:
            st.markdown(f"""
                <div class="receipt-box">
                    <h3 style="text-align: center; margin-top: 0; color: #0284c7;">STRUK RESMI PARKIR</h3>
                    <hr style="border: 1px dashed #cbd5e1;">
                    <p><b>Token:</b> {token_transaksi}</p>
                    <p><b>Waktu Keluar:</b> {waktu_keluar}</p>
                    <p><b>Plat Nomor:</b> {plat_keluar}</p>
                    <p><b>Durasi:</b> {jam_parkir} Jam | <b>Slot Bebas:</b> {slot_to_free}</p>
                    <p><b>Potongan Diskon:</b> Rp {diskon_didapat:,}</p>
                    <p><b>Metode Pembayaran:</b> {metode_bayar}</p>
                    <hr style="border: 1px dashed #cbd5e1;">
                    <h3 style="color: #16a34a; text-align: center;">TOTAL BAYAR: Rp {total_biaya:,}</h3>
                    <p style="text-align: center; font-size: 0.85rem; color: #64748b;">Status: LUNAS ✅</p>
                </div>
            """, unsafe_allow_html=True)
            
        with col_struk2:
            st.markdown("### **📱 Barcode / QR Valet**")
            # Menampilkan QR Code digital otomatis menggunakan API publik gratis
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=Paid-{token_transaksi}-{plat_keluar}"
            st.image(qr_url, caption="Scan QR untuk Buka Gerbang Keluar", width=160)

# --- MENU 3: DENAH VISUAL SLOT PARKIR ---
elif menu_pilihan == "🗺️ Denah Status Slot Parkir":
    st.subheader("🗺️ Visualisasi Real-Time Ketersediaan Slot Parkir")
    st.info("🟩 Hijau = Kosong (Tersedia) | 🟥 Merah = Penuh (Terisi)")
    
    st.write("")
    
    cols = st.columns(4)
    idx = 0
    for slot, status in st.session_state.slot_status.items():
        with cols[idx % 4]:
            if status == 0:
                st.markdown(f"""
                    <div class="slot-box-kosong">
                        <h4>{slot}</h4>
                        <p style="margin:0; font-size: 12px;">🟢 KOSONG</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="slot-box-penuh">
                        <h4>{slot}</h4>
                        <p style="margin:0; font-size: 12px;">🔴 PENUH</p>
                    </div>
                """, unsafe_allow_html=True)
        idx += 1

# --- MENU 4: DASHBOARD ADMIN ---
else:
    st.subheader("📊 Dashboard Admin & Statistik")
    
    total_kosong = list(st.session_state.slot_status.values()).count(0)
    total_penuh = list(st.session_state.slot_status.values()).count(1)
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric(label="Slot Terisi", value=f"{total_penuh} Unit")
    with col_m2:
        st.metric(label="Slot Kosong", value=f"{total_kosong} Slot")
    with col_m3:
        st.metric(label="Estimasi Pendapatan", value="Rp 2.850.000")
        
    st.divider()
    st.bar_chart({"Mobil Standar": 85, "SUV / Besar": 32, "Mobil Listrik": 25})
