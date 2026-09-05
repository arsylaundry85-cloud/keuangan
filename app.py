import os
import pandas as pd
import streamlit as st

# Nama file database CSV
CSV_FILE = "data_keuangan_online.csv"

# Otomatis buat file CSV jika belum ada agar tidak error/layar putih
if not os.path.exists(CSV_FILE):
  df_init = pd.DataFrame(columns=["Tanggal", "Kategori", "Jumlah", "Catatan"])
  df_init.to_csv(CSV_FILE, index=False)


# Fungsi muat data
def load_data():
  return pd.read_csv(CSV_FILE)


# Konfigurasi Tampilan Utama (Diperbaiki)
st.set_page_config(page_title="Aplikasi Keuangan Online", page_icon="💰")
st.title("Aplikasi Keuangan Harian 📊")
st.write(
    "Kelola keuangan dengan kategori Harian, Lain-lain, Laundry, dan Tabungan."
)

# Form Input Transaksi
st.subheader("➕ Tambah Transaksi Baru")
with st.form("form_transaksi"):
  tanggal = st.date_input("Tanggal")
  kategori = st.selectbox(
      "Kategori", ["Harian", "Lain-lain", "Laundry", "Tabungan"]
  )
  jumlah = st.number_input("Jumlah (Rp)", min_value=0, step=1000)
  catatan = st.text_input("Catatan (Opsional)")
  submit = st.form_submit_button("Simpan")

  if submit:
    df = load_data()
    new_data = pd.DataFrame({
        "Tanggal": [str(tanggal)],
        "Kategori": [kategori],
        "Jumlah": [jumlah],
        "Catatan": [catatan],
    })
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    st.success("Transaksi berhasil disimpan!")

# Tampilkan Data & Ringkasan
st.markdown("---")
st.subheader("📋 Riwayat Transaksi")
df_current = load_data()

if not df_current.empty:
  st.dataframe(df_current, use_container_width=True)

  # Ringkasan Total per Kategori
  st.subheader("📌 Ringkasan per Kategori")
  summary = df_current.groupby("Kategori")["Jumlah"].sum().reset_index()
  st.dataframe(summary, use_container_width=True)
else:
  st.info("Belum ada data transaksi. Yuk, mulai isi dari form di atas!")
  
