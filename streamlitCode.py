import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def create_daily_rentals_df(df):
    daily_rentals_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum"
    })
    daily_rentals_df = daily_rentals_df.reset_index()
    daily_rentals_df.rename(columns={
        "cnt": "rental_count"
    }, inplace=True)
    
    return daily_rentals_df

def create_daily_casual_rentals_df(df):
    daily_casual_rentals_df = df.resample(rule='D', on='dteday').agg({
        "casual": "sum"
    })
    daily_casual_rentals_df = daily_casual_rentals_df.reset_index()
    daily_casual_rentals_df.rename(columns={
        "casual": "casual_count"
    }, inplace=True)
    
    return daily_casual_rentals_df

def create_daily_registered_rentals_df(df):
    daily_registered_rentals_df = df.resample(rule='D', on='dteday').agg({
        "registered": "sum"
    })
    daily_registered_rentals_df = daily_registered_rentals_df.reset_index()
    daily_registered_rentals_df.rename(columns={
        "registered": "registered_count"
    }, inplace=True)
    
    return daily_registered_rentals_df


def create_byweather_df(df):
    byweather_df = df.groupby("weathersit").cnt.sum().reset_index()
    byweather_df.rename(columns={
        "cnt": "rental_count"
    }, inplace=True)
    
    return byweather_df


def create_average_rentals_by_holiday(df):
    avg_rentals_by_holiday = df.groupby('holiday')['cnt'].mean().reset_index()
    avg_rentals_by_holiday.rename(columns={"cnt": "average_rental_count"}, inplace=True)
    
    return avg_rentals_by_holiday


all_df = pd.read_csv("data_1.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(drop=True, inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    st.image("https://static.vecteezy.com/system/resources/previews/019/030/974/original/bike-rental-logo-with-a-bicycle-and-label-combination-for-any-business-vector.jpg")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                  (all_df["dteday"] <= str(end_date))]

daily_rentals_df = create_daily_rentals_df(main_df)
daily_casual = create_daily_casual_rentals_df(main_df)
daily_registered = create_daily_registered_rentals_df(main_df)
byweather_df = create_byweather_df(main_df)
average_rentals_df = create_average_rentals_by_holiday(main_df)

st.header('Bike Rental Dashboard :sparkles:')

st.subheader('Daily Rentals')
 
col1, col2, col3 = st.columns(3)
 
with col1:
    total_rentals = daily_rentals_df.rental_count.sum()
    st.metric("Total Rentals", value=total_rentals)
 
with col2:
    total_casual = daily_casual.casual_count.sum()
    st.metric("Total Casual", value=total_casual)

with col3:
    total_registered = daily_registered.registered_count.sum()
    st.metric("Total Registered", value=total_registered)


fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rentals_df["dteday"],
    daily_rentals_df["rental_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader("Rental by Weather Situation")
 
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x="weathersit", 
    y="rental_count", 
    data=byweather_df, 
    palette="viridis", 
    ax=ax
)

ax.set_ylabel("Total Rentals", fontsize=15)
plt.tick_params(axis='x', labelsize=12)
plt.xticks(ticks=[0, 1, 2], labels=["Cerah", "Kabut", "Salju Ringan"]) 
st.pyplot(fig)

st.subheader('Average Rental Holiday or Not')

fig, ax = plt.subplots(figsize=(7, 5))
colors = ["#72BCD4", "#D3D3D3"]

sns.barplot(
    y="average_rental_count", 
    x="holiday",
    data=average_rentals_df.sort_values(by="average_rental_count", ascending=False),
    palette=colors,
    ax=ax
)

ax.tick_params(axis='x', labelsize=12)
ax.set_xticklabels(["Hari Kerja", "Hari Libur"]) 

st.pyplot(fig)

st.caption('Copyright (c) Dicoding 2024')