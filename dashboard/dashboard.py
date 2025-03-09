import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

df = pd.read_csv("all_data.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

season_labels = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df['season_label'] = df['season'].map(season_labels)

dominant_color, secondary_color = '#0b3d91', '#62a8e5'

# Sidebar
min_date, max_date = df["dteday"].min(), df["dteday"].max()

with st.sidebar:
    st.image("bike logo.png")

    start_date, end_date = st.date_input("Pilih Rentang Tanggal", [min_date, max_date], min_value=min_date, max_value=max_date)

    season_options = df["season_label"].unique()
    selected_season = st.selectbox("Pilih Musim", ["Semua"] + list(season_options))

main_df = df[(df["dteday"] >= pd.to_datetime(start_date)) & (df["dteday"] <= pd.to_datetime(end_date))]

if selected_season != "Semua":
    main_df = main_df[main_df["season_label"] == selected_season]

st.header('Dashboard Analisis Bike Sharing :sparkles:')

# **0. Penggunaan Sepeda Harian**
st.subheader("📅 Jumlah Penggunaan Sepeda per Hari")

col1, col2 = st.columns(2)

with col1:
    total_usage = main_df["cnt"].sum()
    st.metric("Total Penggunaan Sepeda", value=total_usage)

with col2:
    avg_usage = round(main_df["cnt"].mean(), 2)
    st.metric("Rata-rata Penggunaan Harian", value=avg_usage)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    main_df["dteday"],
    main_df["cnt"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)

ax.set_xlabel("Tanggal", fontsize=14)
ax.set_ylabel("Jumlah Penggunaan Sepeda", fontsize=14)
ax.set_title("Jumlah Penggunaan Sepeda Per Hari", fontsize=16, fontweight="bold")
ax.tick_params(axis='x', rotation=45, labelsize=12)  # Rotasi label tanggal agar lebih rapi
ax.tick_params(axis='y', labelsize=12)

st.pyplot(fig)


# **1. Rata-rata Penggunaan Sepeda Harian Berdasarkan Musim**
st.subheader("🚴‍♂️ Rata-rata Penggunaan Sepeda Harian Berdasarkan Musim")

season_usage = df.groupby('season_label')['cnt'].mean().reset_index()
max_value = season_usage['cnt'].max()
colors = [dominant_color if val == max_value else secondary_color for val in season_usage['cnt']]

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=season_usage, x='season_label', y='cnt', palette=colors)
ax.set_xlabel('Musim')
ax.set_ylabel('Rata-rata Jumlah Penggunaan Sepeda')

st.pyplot(fig)

# **2. Korelasi antara Suhu dan Jumlah Sepeda yang Disewa**
st.subheader("🌡️ Hubungan antara Suhu dan Jumlah Sepeda yang Dipinjam")
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=df, x='temp', y='cnt', alpha=0.6, color='blue', ax=ax)
ax.set_xlabel('Suhu Udara (Normalized)')
ax.set_ylabel('Jumlah Sepeda yang Dipinjam')
st.pyplot(fig)

correlation = df['temp'].corr(df['cnt'])
st.write(f"**Koefisien Korelasi: {correlation:.2f}**")

# **3. Korelasi Sepeda yang Disewa dengan Suhu berdasarkan Musim**
st.subheader("🌍 Korelasi antara Suhu dan Jumlah Sepeda berdasarkan Musim")
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 10))
axes = axes.flatten()

for i, season in enumerate(df['season_label'].unique()):
    season_data = df[df['season_label'] == season]
    sns.scatterplot(x='temp', y='cnt', data=season_data, alpha=0.6, color='b', ax=axes[i])
    axes[i].set_title(f'{season}')
    axes[i].set_xlabel('Suhu (Normalized)')
    axes[i].set_ylabel('Jumlah Sepeda')

plt.tight_layout()
st.pyplot(fig)
