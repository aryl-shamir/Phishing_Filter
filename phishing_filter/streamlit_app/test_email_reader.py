import streamlit as st
import email
from email import policy

def load_email(uploaded_file):
    uploaded_file.seek(0)
    raw_bytes = uploaded_file.read()
    return email.parser.BytesParser(policy=policy.default).parsebytes(raw_bytes)

st.title("Test EML Reader")

uploaded = st.file_uploader("Upload .eml", type=["eml"])

if uploaded:
    st.write("UploadedFile type:", type(uploaded))
    try:
        msg = load_email(uploaded)
        st.success("Parsed successfully!")
        st.write(msg.keys())
    except Exception as e:
        st.error(str(e))
