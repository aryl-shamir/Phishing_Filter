import streamlit as st 
import sys 
from pathlib import Path

# sys.path.insert(0, Path(__file__).resolve().parent.parent)

from phishing_filter.email_structure import (load_email, get_email_structure,
                                             structure_counter, html_to_plain_text,
                                             email_to_text, email_language,
                                             translate_into_english
                                             )
    
# def email_parser(email_file):
#     with st.expander("Here is the email content"):
#         email_msg = load_email(email_file)
#         email_text = email_to_text(email_msg)
#         return email_msg, st.write(email_text)

def email_parser(loaded_email):
    with st.expander("Here is the email content"):
        email_text = email_to_text(loaded_email)
        st.write(email_text)
            
        
        
        
        
        
        
        
        
        
        



# def email_parser(email_file):

# def email_parser(uploaded_file):
#     if uploaded_file is None:
#         st.info("Awaiting email file(s)")
#         return

#     with st.expander("Here is the email content"):
#         # load_email will handle UploadedFile correctly
#         try:
#             email_msg = load_email(uploaded_file)
#         except Exception as e:
#             st.error(f"Failed to parse uploaded file: {e}")
#             return

#         st.session_state['email_msg'] = email_msg  # optional
#         email_text = email_to_text(email_msg)
#         st.write(email_text)