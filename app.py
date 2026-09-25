import streamlit as st

# Konfigurasi Halaman Web
st.set_page_config(page_title="Smart Parking Calculator", page_icon="🅿️", layout="centered")


st.title("iezzipark")
st.write("Aplikasi penghitung tarif parkir otomatis berdasarkan durasi waktu.")
st.divider()


nama = st.text_input("Nama Pengemudi", "Nafes")
plat = st.text_input("Nomor Kendaraan (Plat)", "B 1234 XYZ")


jam_parkir = st.slider("Pilih Durasi Waktu Parkir (Jam)", min_value=1, max_value=24, value=6)


if jam_parkir <= 1:
    total_biaya = 5000
else:
    total_biaya = 5000 + (jam_parkir - 1) * 3000
  
diskon = 0
if jam_parkir > 5:
    diskon = 2000
    total_biaya -= diskon

if st.button("Hitung Tarif Parkir"):
    st.success("Perhitungan Berhasil!")
    
    # Menampilkan hasil
    st.write(f"**Nama Pengemudi:** {nama} ({plat})")
    st.write(f"**Durasi Parkir:** {jam_parkir} Jam")
    
    if jam_parkir > 5:
        st.info(f"🎉 Selamat! Anda mendapatkan potongan diskon sebesar Rp {diskon:,}")
    
    st.markdown(f"### **Total Biaya Akhir: Rp {total_biaya:,}**")
