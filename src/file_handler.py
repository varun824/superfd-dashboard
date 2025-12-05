import streamlit as st
import pandas as pd
import json

def handleFileUpload():
    file = st.file_uploader("Upload logs file (in JSON format)", type=["json"])

    submit_button = st.button("Submit File", key="submit_file", on_click=lambda: st.session_state.update({"file_uploaded": True}) if file else None)

    if submit_button and file:
        st.success("File submitted successfully!")
    elif submit_button and not file:
        st.error("Please upload a file before submitting.")
        
    if 'file_uploaded' in st.session_state and st.session_state.file_uploaded:
        data = json.load(file)
        
        logs= []
        for log in data:
            value = log['line']
            timestamp = int(log['timestamp'])
            logs.append({'line': value, 'timestamp': timestamp})

        df = pd.DataFrame(logs)

        st.write("Preview:")
        st.write(df.head())
        
        return df