import os
os.environ["STREAMLIT_WATCH_USE_POLLING"] = "true"

import streamlit as st
import requests
from pdf_extraction import extract_biological_data

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

try:
    from streamlit_lottie import st_lottie   #animation part
    upload_animation = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_puciaact.json")
except:
    upload_animation = None

st.set_page_config(page_title="CBC Bot - Upload", layout="centered")
st.markdown("<h1 style='text-align: center;'>🩸 CBC Report Analyzer & Diet Assistant</h1>", unsafe_allow_html=True)

if upload_animation:
    st_lottie(upload_animation, height=250, key="upload_anim")
#create upload button only for pdf
uploaded_file = st.file_uploader("📤 Upload your CBC Report (PDF)", type=["pdf"])

#save the text of pdf in temp file and passing the file to call function 
if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    extracted = extract_biological_data("temp.pdf")
    st.session_state["patient_data"] = extracted # storing the data 
    st.success("✅ CBC data extracted!")
    st.json(extracted)

    if st.button("💬 Chat Now"):
        st.switch_page("pages/Chatbot.py")
