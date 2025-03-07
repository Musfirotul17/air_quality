# Memanggil module yang dibutuhkan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.cluster import KMeans

# Mengatur style seaborn
sns.set(style='dark')

# Membaca Dataset (pastikan file berada pada folder yang sama)
all_df = pd.read_csv("airdata.csv")

# Membuat judul dashboard
st.title("Dashboard Air Quality Control By Station")

#Menambahkan Gambar
st.image("https://klikhijau.com/wp-content/uploads/2019/08/Polusi-Udara-Tingkatkan-Risiko-Dimensia-Begini-Penjelasannya.jpg", caption="Ilustrasi Polusi Udara", use_container_width=True)


# Menampilkan 5 data pertama untuk memastikan dataset terbaca dengan benar
st.write("Data yang ada:") 
st.write(all_df.head()) 

# Menuliskan list polutan yang ada di dataset
list_polusi = ["PM2.5", "PM10", "SO2", "NO2", "CO"] 

# Membuat pilihan polutan yang ingin dicari
selected_polusi = st.selectbox("Pilih jenis polutan:", list_polusi) 

# Cek apakah kolom yang dibutuhkan ada
required_columns = {"year", "station", selected_polusi} 
if required_columns.issubset(all_df.columns):
# Membuat grafik tren kualitas udara berdasarkan polutan yang dipilih 
    fig, ax = plt.subplots(figsize=(10, 5)) 

# Membuat grafik garis interaktif sesuai polutan yang diinginkan
    sns.lineplot(x='year', y=selected_polusi, data=all_df, hue='station', ax=ax) 

    # Pemberian label dan judul 
    ax.set_title(f'Tren {selected_polusi} Berdasarkan Stasiun')  #Menuliskan stasiun aapa yang di dataset
    ax.set_xlabel('Tahun')  #Memberi label x yaitu untuk tahun
    ax.set_ylabel(f'Konsentrasi {selected_polusi}') #Memberi Label y untuk polutan yang dipilih
    ax.legend(title="Stasiun", loc='upper right') #Memberikan keterang untuk warna stasiun pemantauan

# Menampilkan Grafik ke dashboard streamlit
    st.pyplot(fig) 
else: 
    st.error(f"Kolom 'year', 'station', atau '{selected_polusi}' tidak ditemukan dalam dataset!") 

# Widget pemilihan polutan untuk scatter plot
selected_scatter_polusi = st.selectbox("Pilih polutan untuk analisis kecepatan angin:", list_polusi)

# Cek apakah kolom yang dibutuhkan ada
scatter_columns = {"WSPM", selected_scatter_polusi, "wd"}
if scatter_columns.issubset(all_df.columns):
    # Membuat scatter plot interaktif
    fig, ax = plt.subplots(figsize=(8, 5))

    sns.scatterplot(x='WSPM', y=selected_scatter_polusi, hue='wd', data=all_df, ax=ax)

    # Pemberian label dan judul
    ax.set_title(f'Hubungan Kecepatan Angin dan {selected_scatter_polusi}')
    ax.set_xlabel('Kecepatan Angin (WSPM)')
    ax.set_ylabel(f'Konsentrasi {selected_scatter_polusi}')

    # Menampilkan scatter plot di Streamlit
    st.pyplot(fig)
else:
    st.error(f"Kolom 'WSPM', 'wd', atau '{selected_scatter_polusi}' tidak ditemukan dalam dataset!")

# Membuat data clustering menggunakan K-Means
@st.cache_data 
def load_data(): 
    return pd.read_csv("airdata.csv")  #Panggil dataset

airdata = load_data() #Load dataset airdata

# Hitung rata-rata polusi per stasiun menggunakan mean
station_avg = airdata.groupby('station').agg({
    "PM2.5": "mean",
    "PM10": "mean",
    "NO2": "mean",
    "CO": "mean",
    "O3": "mean"
}).reset_index()

#Menerapkan  K-Means dengan 3 cluster yaitu 0,1,2 beradasrkan stasiun
kmeans = KMeans(n_clusters=3, random_state=42) 
station_avg['cluster'] = kmeans.fit_predict(station_avg.iloc[:, 1:]) 

# Menampilkan hasil dalam tabel di Streamlit supaya lebih interaktif dengan memilih cluster 

st.subheader("📍 Stasiun Berdasarkan Cluster") 
selected_cluster = st.selectbox("Pilih Cluster:", [0, 1, 2]) 

st.dataframe(station_avg[station_avg['cluster'] == selected_cluster]) 

# Menampilkan visualisasi hasil clustering 

st.subheader("📊 Visualisasi Clustering Stasiun") 

fig, ax = plt.subplots(figsize=(10, 5)) 
sns.scatterplot(x="PM2.5", y="PM10", hue=station_avg['cluster'], data=station_avg, palette="deep", ax=ax) 
ax.set_title("Clustering Stasiun Pemantauan berdasarkan Konsentrasi Polutan") 
ax.set_xlabel("Rata-rata PM2.5") 
ax.set_ylabel("Rata-rata PM10") 
st.pyplot(fig) 

# Menampilkan jumlah stasiun per cluster  
st.subheader("📈 Jumlah Stasiun perCluster")  
st.bar_chart(station_avg['cluster'].value_counts())  
