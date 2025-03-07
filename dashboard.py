# Memanggil module yang dibutuhkan 
import pandas as pd 
import streamlit as st 
import plotly.express as px 

# Membaca Dataset
all_df = pd.read_csv("airdata.csv") 

# Membuat judul dashboard
st.title("📊 Dashboard Air Quality Control By Station") 

# Menambahkan Gambar yang diinginkan
st.image( 
    "https://klikhijau.com/wp-content/uploads/2019/08/Polusi-Udara-Tingkatkan-Risiko-Dimensia-Begini-Penjelasannya.jpg", 
    caption="Ilustrasi Polusi Udara", 
    use_container_width=True
)

# Menampilkan 5 data pertama untuk memastikan dataset terbaca dengan benar
st.write("📌 **Data yang tersedia:**")  
st.dataframe(all_df.head())  # Menggunakan dataframe agar lebih interaktif 

# List polutan yang tersedia
list_polusi = ["PM2.5", "PM10", "SO2", "NO2", "CO"]  

## 🔹 **Grafik Tren Polutan Berdasarkan Stasiun** 
st.subheader("📈 Tren Polutan Berdasarkan Stasiun") 
selected_polusi = st.selectbox("🔎 Pilih jenis polutan:", list_polusi, key="tren_polutan") 

# Cek apakah kolom yang dibutuhkan ada 
if {"year", "station", selected_polusi}.issubset(all_df.columns): 
    fig = px.line(
        all_df, 
        x="year", 
        y=selected_polusi, 
        color="station", 
        title=f"Tren {selected_polusi} Berdasarkan Stasiun",
        labels={"year": "Tahun", selected_polusi: f"Konsentrasi {selected_polusi}"},
        template="plotly_dark"
    )
    st.plotly_chart(fig)  # Menampilkan grafik interaktif 
else: 
    st.error(f"⚠️ Data tidak tersedia untuk 'year', 'station', atau '{selected_polusi}'!") 

## 🔹 **Scatter Plot: Hubungan Kecepatan Angin dan Polutan** 
st.subheader("💨 Hubungan Kecepatan Angin dengan Konsentrasi Polutan") 
selected_scatter_polusi = st.selectbox("🔎 Pilih polutan yang ingin dianalisis:", list_polusi, key="scatter_polutan") 

# Cek apakah kolom yang dibutuhkan ada 
if {"WSPM", selected_scatter_polusi, "wd"}.issubset(all_df.columns): 
    fig_scatter = px.scatter(
        all_df, 
        x="WSPM", 
        y=selected_scatter_polusi, 
        color="wd",
        title=f"Hubungan Kecepatan Angin dengan Konsentrasi {selected_scatter_polusi}",
        labels={"WSPM": "Kecepatan Angin (m/s)", selected_scatter_polusi: f"Konsentrasi {selected_scatter_polusi} (µg/m³)", "wd": "Arah Angin"},
        template="plotly_dark"
    )
    st.plotly_chart(fig_scatter)  # Menampilkan scatter plot interaktif 
else:
    st.error(f"⚠️ Data tidak tersedia untuk 'WSPM', 'wd', atau '{selected_scatter_polusi}'!")   
