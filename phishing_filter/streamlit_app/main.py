import streamlit as st 
import sys 
from pathlib import Path
import joblib

# Path to phishing_filter/
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

sys.path.insert(0, Path(__file__).resolve().parent.parent)
from get_email import email_parser

from phishing_filter.tokens_class import (MAX_CHARS, clean_text,
                                          EmailToTokens, identity, get_spacy_model
                                          )
from phishing_filter.email_structure import load_email

log_model_path = MODEL_DIR/'logistic_regression_classifier.pkl'
svm_model_path = MODEL_DIR/'support_vector_classifier.pkl'
log_classifier, svm_classifier = joblib.load(log_model_path), joblib.load(svm_model_path)


def main():
    
    if 'loaded_email' not in st.session_state:
        st.session_state.loaded_email = None
    
    st.logo(image='static/image.png', size='large')
    st.subheader('Phishing email classifier')
    st.caption('This phishing app uses two models, logistic regression model and the support vector machine model'
               ' having the highest precision of 99%. Check if the email you received is a phishing one ')
    
    with st.sidebar.header('1. Upload your emails'):
        uploaded_file = st.file_uploader('Upload your email file(s) here', type=['eml'])
        
    
    if uploaded_file is not None:
        st.session_state.loaded_email = load_email(uploaded_file)
        email_parser(st.session_state.loaded_email)
    else:
        st.info("Awaiting for the email file(s)")
    
    st.divider()
    chosen_model = st.selectbox('Choose the model you wish to use', ['logistic Classifier', 'Support Vector machine'])
    st.divider()
    
    if st.session_state.loaded_email:
        if chosen_model == 'logistic Classifier':
            phishing_prediction = log_classifier.predict([st.session_state.loaded_email])
        elif chosen_model == 'Support Vector machine':
            phishing_prediction = svm_classifier.predict([st.session_state.loaded_email])
            
        # Progress Bar Indicator (0–1)
     
        prediction = int(phishing_prediction[0])

        st.markdown("Prediction Indicator")

        progress_value = 1.0 if prediction == 1 else 0.0

        st.progress(progress_value)

        if prediction == 1:
            st.error("⚠️ This email is likely a **Phishing Email**.")
        else:
            st.success("✔️ This email looks like **Ham (Safe)**.")
        
    
if __name__ == "__main__":
    main()
        