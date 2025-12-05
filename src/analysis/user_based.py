import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def userAnalysis(df):
    st.header("User-Based Analysis")
    
    st.write("### Activity segregation by users")
    userActivitySegregation(df)
    
    st.write("### User activity segregation by day of the week")
    userActivitySegregationByDay(df)
    
    uniqueUsers(df)
    
    
def userActivitySegregation(df):
    null_mask = df['user_id'].isnull() | df['user_id'].astype(str).str.lower().str.contains('null', na=False)
    null_count = int(null_mask.sum())
    non_null_count = int(len(df) - null_count)

    labels = ['Public Users', 'Signed-in Users']
    sizes = [null_count, non_null_count]

    plt.figure(figsize=(8, 8))
    plt.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=140,
        textprops={'color': 'black'}
    )
    plt.axis('equal') 
    plt.title('User Activity Segregation: Public vs Signed-in')

    st.pyplot(plt)
    
    
def userActivitySegregationByDay(df):
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['date'].dt.day_name()

    df_all_days = df.copy()

    df_all_days['user_type'] = df_all_days['user_id'].apply(lambda x: 'Public Users' if 'null' in x else 'Signed-in Users')

    all_day_logs_by_user_type = df_all_days.groupby(['day_of_week', 'user_type']).size().unstack(fill_value=0)
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    all_day_logs_by_user_type = all_day_logs_by_user_type.reindex(days_order)
    ax = all_day_logs_by_user_type.plot(kind='bar', figsize=(12, 7), color=['red', 'blue'])

    plt.title('Daily Log Counts by User Type')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Logs')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='User Type')

    for container in ax.containers:
        ax.bar_label(container, fmt='%d', label_type='edge')

    plt.tight_layout()
    st.pyplot(plt)
    

def uniqueUsers(df):
    total_unique_users = df['user_id'].nunique()
    st.write(f"Total unique users in the dataset: {total_unique_users}")
    
    null_users_df = df[df['user_id'].str.contains('null', na=False)]
    null_unique_users = null_users_df['user_id'].nunique()
    st.write(f"Total unique public users in the dataset: {null_unique_users}")
    
    auth_users_df = df[df['url_path'] == '/auth']
    unique_auth_users = auth_users_df['user_id'].nunique()
    st.write(f"Unique number of users visiting /auth: {unique_auth_users}")

    