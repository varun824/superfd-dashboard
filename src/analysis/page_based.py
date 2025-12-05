import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


def clean_url_path(url):
    if url.startswith('/'):
        return url[1:]
    return url


def get_first_directory(url):
    parts = url.split('/')
    return parts[0]


def pageAnalysis(df):
    df['url_path'] = df['url_path'].apply(clean_url_path)
    df['first_directory'] = df['url_path'].apply(get_first_directory)
    
    st.header("Page-Based Analysis")
    st.write("### Activity by First Directory in URL Paths")
    activityByDirectory(df)
    st.write("### Page Activity by User Type")
    pageActivityByUsers(df)
    st.write("### Most Visited Bank Pages")
    bankPagesActivity(df)
    st.write("### Bank Pages Activity by User Type")
    bankPagesActivityByUser(df)


def activityByDirectory(df):
    first_directory_counts = df['first_directory'].value_counts()
    labels = first_directory_counts.index
    sizes = first_directory_counts.values

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of First Directories in URL Paths')
    plt.axis('equal')
    
    st.pyplot(plt)
    
    
def pageActivityByUsers(df):
    null_users_df = df[df['user_id'].str.contains('null', na=False)]
    non_null_users_df = df[~df['user_id'].str.contains('null', na=False)]
    
    null_users_df['first_directory'] = null_users_df['url_path'].apply(get_first_directory)
    non_null_users_df['first_directory'] = non_null_users_df['url_path'].apply(get_first_directory)

    null_users_directory_counts = null_users_df['first_directory'].value_counts()
    non_null_users_directory_counts = non_null_users_df['first_directory'].value_counts()
    
    st.write("### Distribution of First Directories for public Users:")
    labels_null = null_users_directory_counts.index
    sizes_null = null_users_directory_counts.values

    plt.figure(figsize=(8, 8))
    plt.pie(sizes_null, labels=labels_null, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of First Directories for Public Users')
    plt.axis('equal')
    st.pyplot(plt)

    st.write("### Distribution of First Directories for signed-in Users:")
    labels_non_null = non_null_users_directory_counts.index
    sizes_non_null = non_null_users_directory_counts.values

    plt.figure(figsize=(8, 8))
    plt.pie(sizes_non_null, labels=labels_non_null, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of First Directories for Signed-in Users')
    plt.axis('equal')
    st.pyplot(plt)
    
    
def bankPagesActivity(df):
    df_banks = df[df['url_path'].str.startswith('banks/')]
    df_banks['bank_name'] = df_banks['url_path'].str.extract(r'banks/(.*?)-bank-fd-rates')
    
    bank_counts = df_banks.groupby('bank_name').size()
    bank_counts = bank_counts.sort_values(ascending=False)
    
    plt.figure(figsize=(10, 6))
    bars = bank_counts.plot(kind='bar')
    plt.title("Most Visited Bank Pages")
    plt.xlabel("Bank Name")
    plt.ylabel("Number of Visits")
    plt.xticks(rotation=45, ha='right')

    total = bank_counts.sum()
    for bar in bars.patches:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 5, int(yval), ha='center', va='bottom')
        plt.text(bar.get_x() + bar.get_width()/2.0, yval/2.0, '{:.1f}%'.format(yval/total*100), ha='center', va='center')

    plt.tight_layout()
    st.pyplot(plt)
    
    
def bankPagesActivityByUser(df):
    df_banks = df[df['url_path'].str.startswith('banks/')]
    df_banks['bank_name'] = df_banks['url_path'].str.extract(r'banks/(.*?)-bank-fd-rates')
    
    null_banks_df = df_banks[df_banks['user_id'].str.contains('null', na=False)]
    non_null_banks_df = df_banks[~df_banks['user_id'].str.contains('null', na=False)]

    null_banks_counts = null_banks_df['bank_name'].value_counts()
    non_null_banks_counts = non_null_banks_df['bank_name'].value_counts()

    with st.container():
        left,right= st.columns(2)
        with left:
            st.write("### Bank Name Counts for Public Users:")
            st.write(null_banks_counts)
        with right:
            st.write("### Bank Name Counts for Signed-in Users:")
            st.write(non_null_banks_counts)