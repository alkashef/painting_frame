import frame
import extract_colors
import streamlit as st

PAGES = {"Frame"          : frame,
         "Extract Colors" : extract_colors}

st.set_page_config(layout="wide")

selection = st.selectbox("", list(PAGES.keys()))
page = PAGES[selection]
page.app()
