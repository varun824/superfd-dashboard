import pandas as pd
import streamlit as st
def preprocessor(df):
    # Handle timestamp conversion and sorting
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ns')
    df = df.sort_values(by='timestamp')
    df = df.reset_index(drop=True)
    df['ist_timestamp'] = pd.to_datetime(df['timestamp'], unit='ns', utc=True).dt.tz_convert('Asia/Kolkata')
    
    #Unpack line into url_path and user_id
    df[['url_path', 'user_id']] = df['line'].str.split(',', expand=True)
    df['user_id'] = df['user_id'].str.replace('user/', '', regex=False)
    df = df.drop('line', axis=1)
    
    # Extract date and time from ist_timestamp
    df['date'] = df['ist_timestamp'].dt.date
    df['time'] = df['ist_timestamp'].dt.strftime('%H:%M')
    df = df[['timestamp', 'date', 'time', 'url_path', 'user_id']]
    
    return df