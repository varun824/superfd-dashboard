import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks

def timeAnalysis(df):
    st.header("Time-Based Analysis")
    
    st.write("### Logs per Day")
    logsPerDay(df)
    st.write("### Logs by Day of the Week")
    logsByDayOfWeek(df)
    st.write("### Logs by Hour of the Day")
    logsByHour(df)
    
    
def logsPerDay(df):
    df['date'] = pd.to_datetime(df['date'])
    logs_by_date = df['date'].value_counts().sort_index()
    
    plt.figure(figsize=(12, 6))
    plt.plot(logs_by_date.index, logs_by_date.values)
    plt.xlim([logs_by_date.index.min(), logs_by_date.index.max()])
    plt.title('Number of Logs per Day')
    plt.xlabel('Date')
    plt.ylabel('Number of Logs')
    plt.xticks(rotation=45)
    plt.tight_layout()

    peaks, _ = find_peaks(logs_by_date.values)

    for peak_index in peaks:
        date = logs_by_date.index[peak_index]
        count = logs_by_date.values[peak_index]
        plt.text(date, count, str(count), ha='center', va='bottom')
        
    st.pyplot(plt)
    
    
def logsByDayOfWeek(df):
    df['day_of_week'] = df['date'].dt.day_name()

    logs_by_day_of_week = df['day_of_week'].value_counts()
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    logs_by_day_of_week = logs_by_day_of_week.reindex(days_order)

    plt.figure(figsize=(10, 6))
    bars = logs_by_day_of_week.plot(kind='bar')
    plt.title('Number of Logs per Day of the Week')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Logs')
    plt.xticks(rotation=45, ha='right')

    for bar in bars.patches:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 5, int(yval), ha='center', va='bottom')

    plt.tight_layout()
    st.pyplot(plt)
    
    
def logsByHour(df):
    df['hour'] = pd.to_datetime(df['time']).dt.hour

    logs_by_hour = df['hour'].value_counts().sort_index()
    plt.figure(figsize=(12, 6))
    plt.plot(logs_by_hour.index, logs_by_hour.values)

    plt.title('Number of Logs per Hour of Day')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Logs')
    plt.xticks(range(24))
    plt.tight_layout()

    peaks, _ = find_peaks(logs_by_hour.values)

    for peak_index in peaks:
        hour = logs_by_hour.index[peak_index]
        count = logs_by_hour.values[peak_index]
        plt.text(hour, count, str(count), ha='center', va='bottom')
    
    st.pyplot(plt)