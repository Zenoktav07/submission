import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# load data
data = pd.read_csv('dashboard/main_data.csv')

st.title("Dashboard Analisis Data")

# Filter data
st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox("Pilih Tahun", data['year'].unique())
season_options = ["Semua Musim"] + list(data['season'].unique())
selected_season = st.sidebar.selectbox("Pilih Musim", season_options)

if selected_season == "Semua Musim":
    filtered_data = data[data['year'] == selected_year]
else:
    filtered_data = data[(data['year'] == selected_year) & (data['season'] == selected_season)]

st.subheader("Data yang Difilter")
st.dataframe(filtered_data)


# Tren pengguna per bulan
st.subheader("Tren Pengguna per Bulan")
monthly_data = filtered_data.groupby('mnth')['cnt'].sum().reset_index()
plt.figure(figsize=(10, 5))
sns.barplot(x=monthly_data['mnth'], y=monthly_data['cnt'], palette='viridis')
plt.xlabel("Bulan")
plt.ylabel("Total Pengguna")
plt.title("Total Pengguna per Bulan")
st.pyplot(plt)


# Perbandingan penggunaan sepeda (hari kerja vs akhir pekan)
st.subheader("Perbandingan Penggunaan Sepeda")

is_weekend_options = ["Semua", "Weekday", "Weekend"]
selected_weekend = st.sidebar.selectbox("Pilih Kategori Hari", is_weekend_options)

if selected_weekend != "Semua":
    filtered_viz4_data = filtered_data[filtered_data['is_weekend'] == selected_weekend]
else:
    filtered_viz4_data = filtered_data

total_cnt_perweekend = filtered_viz4_data.groupby(by=["is_weekend"]).agg({
    "cnt": "sum"
}).sort_values(by="cnt", ascending=False).reset_index()

labels = total_cnt_perweekend["is_weekend"]
plt.figure(figsize=(5, 5))
explode = (0, 0.1) if len(labels) == 2 else (0,)
palette_color = sns.color_palette('pastel')

plt.pie(total_cnt_perweekend["cnt"],
        labels=labels,
        autopct='%1.f%%',
        startangle=90,
        pctdistance=0.6,
        explode=explode,
        colors=palette_color
        )

plt.title("Penggunaan Sepeda (Weekend vs Weekday)")
st.pyplot(plt)


# Distribusi suhu
st.subheader("Distribusi Suhu")
plt.figure(figsize=(8, 5))
sns.histplot(filtered_data['temp'], kde=True, bins=20, color='blue')
plt.xlabel("Suhu")
plt.ylabel("Frekuensi")
plt.title("Distribusi Suhu")
st.pyplot(plt)


# Pengaruh cuaca terhadap jumlah pengguna
st.subheader("Pengaruh Cuaca terhadap Pengguna")
weather_data = filtered_data.groupby('weathersit')['cnt'].mean().reset_index()
plt.figure(figsize=(8, 5))
sns.barplot(x=weather_data['weathersit'], y=weather_data['cnt'], palette='coolwarm')
plt.xlabel("Kondisi Cuaca")
plt.ylabel("Rata-rata Pengguna")
plt.title("Rata-rata Pengguna berdasarkan Kondisi Cuaca")
st.pyplot(plt)
