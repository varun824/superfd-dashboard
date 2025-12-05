import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def FDAnalysis(df):
    st.header("FD-Based Analysis")
    
    df_deposit = mapBankFromHash(df)
    
    st.write("### Most Visited FD Pages")
    FDPagesActivity(df_deposit)
    
    st.write("### FD Pages Activity by User Type")
    FDPageActivityByUser(df_deposit)
    
    
    
    
def mapBankFromHash(df):
    df_deposit = df[df['url_path'].str.startswith('fd/')]
    df_deposit['deposit_hash'] = df_deposit['url_path'].str.replace('fd/', '')
    
    fdMap = {
        "cmc8t2dur0015c8w0mfg0trca" : "suryoday",
        "cmc8w1is3001lc8w0uqrdu542" : "unity",
        "cmc8ytv5l001w10ffo5j0zvd9" : "shriram",
        "cmc90hhex002qc8w0u0ws85fc" : "bajaj",
        "cm1tail900007d32xj5mfwcxb" : "suryoday",
        "clwrt7yf300041iueibdcw7yf" : "unity",
        "clwj02goo000b888hne8uurmr" : "mahindra",
        "clwizrefx0001888h3f4n3lvx" : "shriram",
        "cmc9208ou003c10fftt0v3vjw" : "mahindra",
        "cmdrih74z0002kk055813y9nu" : "utkarsh",
        "clwrwgvbn000drzvhgch76n32" : "bajaj",
        "cm9skljiv002cykrejmzbvsm4" : "shriram",
        "cm9sh373q001gykreu78fznee" : "shriram",
        "cm98obfwd0006m9hjl0ltm5gk" : "shriram",
        "cm9sk5vg1001zykreluejeyf2" : "shriram",
        "cm9s6dxep000jykrephpuqayt" : "shriram",
        "cm19nfma0000hnpz22zezt2cl" : "shriram"
    }
    
    df_deposit['deposit_name'] = df_deposit['deposit_hash'].map(fdMap)
    
    return df_deposit


def FDPagesActivity(df_deposit):    
    deposit_name_counts = df_deposit['deposit_name'].value_counts()
    
    plt.figure(figsize=(10, 6))
    bars = deposit_name_counts.plot(kind='bar')
    plt.title("Most Visited FD Pages")
    plt.xlabel("Name of FD")
    plt.ylabel("Number of Visits")
    plt.xticks(rotation=45, ha='right')


    total = deposit_name_counts.sum()
    for bar in bars.patches:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 5, int(yval), ha='center', va='bottom')
        plt.text(bar.get_x() + bar.get_width()/2.0, yval/2.0, '{:.1f}%'.format(yval/total*100), ha='center', va='center')

    plt.tight_layout()
    st.pyplot(plt)
    
    
def FDPageActivityByUser(df_deposit):
    null_deposit_df = df_deposit[df_deposit['user_id'].str.contains('null', na=False)]
    non_null_deposit_df = df_deposit[~df_deposit['user_id'].str.contains('null', na=False)]

    null_deposit_counts = null_deposit_df['deposit_name'].value_counts()
    non_null_deposit_counts = non_null_deposit_df['deposit_name'].value_counts()
    
    combined_deposit_counts = pd.DataFrame({
        'Public Users': null_deposit_counts,
        'Signed-in Users': non_null_deposit_counts
    }).fillna(0)

    ax = combined_deposit_counts.plot(kind='bar', figsize=(12, 7), color=['red', 'blue'])

    plt.title('Deposit pages visited by Public vs. Signed-in Users')
    plt.xlabel('Deposit Name')
    plt.ylabel('Number of Visits')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='User Type')

    for container in ax.containers:
        ax.bar_label(container, fmt='%d', label_type='edge')

    plt.tight_layout()
    st.pyplot(plt)