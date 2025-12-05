import streamlit as st
from src.analysis.page_based import pageAnalysis
from src.analysis.time_based import timeAnalysis
from src.file_handler import handleFileUpload
from src.page_config import setConfig
from src.preprocessing import preprocessor
from src.analysis.user_based import userAnalysis
from src.analysis.fd_based import FDAnalysis

setConfig()
st.title("Super FD Analytics Dashboard")


df = handleFileUpload()

if df is not None:
    df = preprocessor(df)
    st.write(df.head())
    timeAnalysis(df)
    userAnalysis(df)
    pageAnalysis(df)
    FDAnalysis(df)  