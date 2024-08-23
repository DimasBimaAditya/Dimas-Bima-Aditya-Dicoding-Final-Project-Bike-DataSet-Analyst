import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

sns.set(style='dark')

st.title('PUBLIC BIKE RENTAL')
st.text('Hi, My Name is Dimas Bima Aditya')
st.text('This is my first Streamlit app')
st.text('Hope You Liked It :)')


#IMPORT DATA SET
day_df = pd.read_csv("D:/Submission/Dashboard/day.csv")
hour_df = pd.read_csv("D:/Submission/Dashboard/hour.csv")
 
with st.sidebar:
        st.image('D:/Submission/Dashboard/Masdim.png')
        st.title('YOUR TRUSTED RENTS PLACE')

#REPLACING THE WRONG DATA TYPE OF A DATASET COMPONENT
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df['dteday'] = pd.to_datetime(hour_df['dteday'])

#CLEAN THE OUTLIER ON THE HOUR DATASET AND REPLACE IT WITH ITS MEDIAN VALUE
Q1 = hour_df['cnt'].quantile(0.25)
Q3 = hour_df['cnt'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1 * IQR
upper_bound = Q3 + 1 * IQR

median_cnt = hour_df['cnt'].median()
hour_df['cnt'] = np.where((hour_df['cnt'] < lower_bound) | (hour_df['cnt'] > upper_bound), median_cnt, hour_df['cnt'])

#CREATE A BOXPLOT TO CHECK ITS OUTLIER
fig, ax = plt.subplots()
sns.boxplot(x=hour_df['cnt'], ax=ax)  # Specify 'cnt' column for boxplot
plt.xlabel('Count')
plt.title('Boxplot after Outlier Handling on DataSet Hour')

#CREATING COLUMNS FOR DAYS OF THE WEEK
day_df['hari_dalam_seminggu'] = day_df['dteday'].dt.day_name()
day_df['kategori_hari'] = day_df['hari_dalam_seminggu'].apply(lambda x: 'weekday' if x in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] else 'weekend')

#MAKING THE TOTAL NUMBER OF RENTERS OF THE BIKE
col1, col2, col3, col4 = st.columns(4)

#TOTAL RENTERS
with col1:
    st.write("TOTAL RENTERS")
    total=day_df['cnt'].sum()
    st.write('TOTAL =',total)

#TOTAL WEEKDAY BIKE RENTAL
with col2:
    st.write("WEEKDAYS")
    weekdayy=day_df[day_df['kategori_hari'] == 'weekday']['cnt'].sum()
    st.write("TOTAL = ",weekdayy)

#TOTAL WEEKEND BIKE RENTAL
with col3:
    st.write("WEEKEND")
    weekendd=day_df[day_df['kategori_hari'] == 'weekend']['cnt'].sum()
    st.write("TOTAL = ",weekendd)

#DIFFERENCE IN BIKE RENTERS BETWEEN WEEKDAYS AND WEEKENDS
with col4:
    st.write("DIFFERENCE BETWEEN WEEKDAYS & WEEKENDS")
    selisih = day_df[day_df['kategori_hari'] == 'weekday']['cnt'].sum() - day_df[day_df['kategori_hari'] == 'weekend']['cnt'].sum()
    st.write("DIFF = ",selisih)

st.header('WEEKDAY & WEEKEND RENTAL')

#VISUALIZATION
#QUESTION 1
#BOXPLOT
fig, ax = plt.subplots(figsize=(8, 6))
sns.boxplot(x='cnt', y='kategori_hari', data=day_df, ax=ax)
plt.title('Comparison of the Number of Rents between Weekdays and Weekends')
plt.ylabel('Day')
plt.xlabel('Rents')
st.pyplot(fig)

#BAR CHART
weekday_cnt = day_df[day_df['kategori_hari'] == 'weekday']['cnt'].sum()
weekend_cnt = day_df[day_df['kategori_hari'] == 'weekend']['cnt'].sum()
fig, ax = plt.subplots(figsize=(8, 6))
plt.bar(['Weekday'], [weekday_cnt], color='blue', label='Weekday')
plt.bar(['Weekend'], [weekend_cnt], color='orange', label='Weekend')
plt.title('Comparison of the Number of Rents between Weekdays and Weekends')
plt.xlabel('Day')
plt.ylabel('Rents')
st.pyplot(fig)

#DAILY BIKE RENTAL
st.header('DAILY BIKE RENTAL')
jumlah_harian = day_df.groupby('hari_dalam_seminggu')['cnt'].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 6))
jumlah_harian.plot(kind='bar', ax=ax)
plt.title('Number of Rents per Day (MOST)')
plt.xlabel('Day')
plt.ylabel('Rents')
plt.xticks(rotation=45)
st.pyplot(fig)

#QUESTION 2
st.header('BIKE RENTAL BY WEATHER')

cuaca = day_df.groupby('weathersit')['cnt'].describe(include='all')
rata_rata_pengguna_per_cuaca = day_df.groupby('weathersit')['cnt'].mean()

# Calculate and display average usage per day and weather in Streamlit
day_df['dayofweek'] = day_df['dteday'].dt.dayofweek
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
average_usage = day_df.groupby(['dayofweek', 'weathersit'])['cnt'].mean().reset_index()

#BAR CHART
st.subheader('BAR CHART')
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='dayofweek', y='cnt', hue='weathersit', data=average_usage, order=range(7), ax=ax)
plt.xticks(range(7), day_order)
plt.title('Comparison of Rents per Day with Weather Conditions')
plt.xlabel('Weather(1.Sunny , 2.Cloudy , 3.Rainy)')
plt.ylabel('Rents')
plt.legend(title='Weather')
st.pyplot(fig)

#LINE CHART
st.subheader('LINE CHART')
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='dayofweek', y='cnt', hue='weathersit', data=average_usage, marker='o', ax=ax)
plt.xticks(range(7), day_order)
plt.title('Comparison of Rents per Day with Weather Conditions')
plt.xlabel('Day (Weather : 1.Sunny , 2.Cloudy , 3.Rainy)')
plt.ylabel('Rents')
plt.legend(title='Weather')
st.pyplot(fig)

#QUESTION 3

#PROCESSING DATA TO FIND OUT THE MOST BIKE RENTALS BY HOUR
hourly_usage = hour_df.groupby('hr')['cnt'].mean().reset_index()
jam = hour_df.groupby('hr')['cnt'].describe(include='all')

hourly_usage = hour_df.groupby('hr')['cnt'].mean().reset_index()
hourly_usage_sorted = hourly_usage.sort_values('cnt', ascending=False)

hourly_usage_sorted = hour_df[hour_df['hr'] == 16]
hour16 = hourly_usage_sorted.groupby('dteday')['cnt'].sum().reset_index()
max_usage_date = hour16[hour16['cnt'] == hour16['cnt'].max()]['dteday'].iloc[0]

st.header('BIKE RENTAL BY HOUR')
#LINE CHART
st.subheader('LINE CHART')
fig, ax = plt.subplots(figsize=(10, 6))
plt.plot(hourly_usage['hr'], hourly_usage['cnt'])
plt.xlabel('Hour')
plt.ylabel('Rents')
plt.title('Rentals by Hour')
plt.xticks(range(24))
plt.grid(True)
st.pyplot(fig)

#BAR CHART
st.subheader('BAR CHART')
fig, ax = plt.subplots(figsize=(10, 6))
plt.bar(hourly_usage['hr'], hourly_usage['cnt'])
plt.xlabel('Hour')
plt.ylabel('Rents')
plt.title('Rentals by Hour')
plt.xticks(range(24))
st.pyplot(fig)

st.caption('Copyright (C) Dimas Bima Aditya 2024')
