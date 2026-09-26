import streamlit as st
import random
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(page_title="Smart Parking System - Pro Edition", page_icon="🚗", layout="centered")

# Custom CSS Premium (Biar Tampilannya Jauh Lebih Estetik & Gak Kaku)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    .stApp {
        background-color: #0b0f19;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f1f5f9;
    }
    
    /* Header Modern Card */
    .hero-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        margin-bottom: 25px;
    }
    
    /* Container Kotak Informasi & Struk */
    .custom-box {
        background: #1e293b;
        border: 1px solid #334155;
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    /* Desain Slot Parkir */
    .slot-grid-kosong {
        background: linear-gradient(135deg, #064e3b 0%, #022c22 100%);
        border: 1px solid #059669;
        padding: 16px;
        border-radius: 14px;
        text-align: center;
        color: #34d399;
        font-weight: 700;
        box-shadow: 0 4px 10px rgba(5, 150, 105, 0.15);
    }
    .slot-grid-penuh {
        background: linear-gradient(135deg, #7f1d1d 0%, #450a0a 100%);
        border: 1px solid #dc2626;
        padding: 16px;
        border-radius: 14px;
        text-align: center;
        color: #f87171;
        font-weight: 700;
        box-shadow: 0 4px 10px rgba(220, 38, 38, 0.15);
    }
    
    /* Tombol Kustom */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 6px 15px rgba(37, 99, 235, 0.5);
        transform: translateY(-1px);
    }
    
    /* Styling Radio Menu */
    .stRadio > div {
        background: #1e293b;
        padding: 10px;
        border-radius: 14px;
        border: 1px solid #334155;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ESTETIK ---
st.markdown("""
    <div class="hero-card">
        <span style="font-size: 40px;">🚗⚡</span>
        <h1 style="color: #38bdf8; margin: 10px 0 5px 0; font-size: 26px;">Smart Parking Management</h1>
        <p style="color: #94a3b8; margin: 0; font-size: 14px;">Sistem Otomasi Tarif LKPD & Visualisasi Slot Real-Time</p>
    </div>
""", unsafe_allow_html=True)

# Inisialisasi State Slot Parkir
if 'slot_status' not in st.session_state:
    st.session_state.slot_status = {
        "A1": 0, "A2": 1, "A3": 0, "A4": 0,
        "B1": 1, "B2": 1, "B3": 0, "B4": 1,
        "VIP 1": 0, "VIP 2": 1
    }

# Navigasi Tab Menu yang Lebih Clean
menu_pilihan = st.radio("Navigasi Menu:", [
    "📝 Pintu Masuk", 
    "💳 Pintu Keluar & Pembayaran", 
    "🗺️ Denah Slot Parkir", 
    "📊 Dashboard Admin"
], horizontal=True, label_visibility="collapsed")

st.write("")

# --- MENU 1: ENTRY GATE ---
if menu_pilihan == "📝 Pintu Masuk":
    st.markdown("### 📥 Pendaftaran Kendaraan Masuk")
    
    with st.container():
        st.markdown('<div class="custom-box">', unsafe_allow_html=True)
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
            
            st.write("")
            submit_entry = st.form_submit_button("Cetak Karcis & Masukkan Kendaraan 🚀")
            
            if submit_entry and slot_tersedia:
                st.session_state.slot_status[pilih_slot] = 1
                waktu_masuk = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                st.success(f"✅ Kendaraan Berhasil Masuk ke Slot **{pilih_slot}**!")
                st.info(f"**Waktu Masuk:** {waktu_masuk} | **Driver:** {nama_driver} ({plat_nomor})")
            elif submit_entry:
                st.error("Maaf, seluruh slot parkir sedang penuh!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- MENU 2: EXIT GATE & PEMBAYARAN ---
elif menu_pilihan == "💳 Pintu Keluar & Pembayaran":
    st.markdown("### 📤 Kalkulator Tarif & Pembayaran")
    
    with st.container():
        st.markdown('<div class="custom-box">', unsafe_allow_html=True)
        plat_keluar = st.text_input("Nomor Plat Kendaraan Keluar:", "B 1234 XYZ")
        jam_parkir = st.slider("Durasi Waktu Parkir (Jam):", min_value=1, max_value=24, value=6)
        
        metode_bayar = st.selectbox("Metode Pembayaran:", [
            "📱 QRIS (GoPay / OVO / Dana / BCA)", 
            "💳 Kartu E-Money (Flazz / Mandiri)", 
            "💵 Tunai (Cash)"
        ])
        
        slot_terisi = [k for k, v in st.session_state.slot_status.items() if v == 1]
        slot_to_free = st.selectbox("Kosongkan Slot Parkir:", slot_terisi if slot_terisi else ["Tidak ada kendaraan di dalam"])

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
            if slot_terisi:
                st.session_state.slot_status[slot_to_free] = 0 
                
            waktu_keluar = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            token_transaksi = f"PARK-{random.randint(10000, 99999)}"
            
            st.divider()
            col_struk1, col_struk2 = st.columns([1.3, 1])
            
            with col_struk1:
                st.markdown(f"""
                    <div style="background: #f8fafc; color: #0f172a; padding: 20px; border-radius: 12px; border-left: 5px solid #3b82f6; font-family: monospace;">
                        <h4 style="text-align: center; margin-top: 0; color: #1e293b;">STRUK PEMBAYARAN</h4>
                        <hr style="border: 1px dashed #cbd5e1;">
                        <p style="margin: 4px 0;"><b>Token:</b> {token_transaksi}</p>
                        <p style="margin: 4px 0;"><b>Waktu:</b> {waktu_keluar}</p>
                        <p style="margin: 4px 0;"><b>Plat:</b> {plat_keluar}</p>
                        <p style="margin: 4px 0;"><b>Durasi:</b> {jam_parkir} Jam (Slot: {slot_to_free})</p>
                        <p style="margin: 4px 0;"><b>Diskon LKPD:</b> Rp {diskon_didapat:,}</p>
                        <p style="margin: 4px 0;"><b>Metode:</b> {metode_bayar}</p>
                        <hr style="border: 1px dashed #cbd5e1;">
                        <h3 style="color: #16a34a; text-align: center; margin: 5px 0;">TOTAL: Rp {total_biaya:,}</h3>
                    </div>
                """, unsafe_allow_html=True)
                
            with col_struk2:
                qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=Paid-{token_transaksi}-{plat_keluar}"
                st.image(qr_url, caption="Scan QR Validasi Keluar", width=140)
        st.markdown('</div>', unsafe_allow_html=True)

# --- MENU 3: DENAH SLOT PARKIR ---
elif menu_pilihan == "🗺️ Denah Slot Parkir":
    st.markdown("### 🗺️ Real-Time Slot Ketersediaan Parkir")
    st.markdown('<div class="custom-box">', unsafe_allow_html=True)
    
    cols = st.columns(4)
    idx = 0
    for slot, status in st.session_state.slot_status.items():
        with cols[idx % 4]:
            if status == 0:
                st.markdown(f"""
                    <div class="slot-grid-kosong">
                        <div style="font-size: 18px;">{slot}</div>
                        <div style="font-size: 11px; margin-top: 4px;">🟢 TERSEDIA</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="slot-grid-penuh">
                        <div style="font-size: 18px;">{slot}</div>
                        <div style="font-size: 11px; margin-top: 4px;">🔴 TERISI</div>
                    </div>
                """, unsafe_allow_html=True)
        idx += 1
    st.markdown('</div>', unsafe_allow_html=True)

# --- MENU 4: DASHBOARD ADMIN ---
else:
    st.markdown("### 📊 Ringkasan Statistik Parkir")
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
    st.markdown('<div class="custom-box">', unsafe_allow_html=True)
    st.markdown("<b>Grafik Kunjungan Kendaraan Harian</b>", unsafe_allow_html=True)
    st.bar_chart({"Mobil Standar": 85, "SUV / Besar": 32, "Mobil Listrik": 25})
    st.markdown('</div>', unsafe_allow_html=True)
