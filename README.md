# 📧 Phishing Email Classifier using sapcy as natural language preprocessing 

This project is a machine-learning application that detects whether an email is **phishing** or **ham (safe)**.  
It uses two trained models:

- **Logistic Regression**
- **Support Vector Machine (SVM)**

The app is built with **Streamlit** for easy interaction and visualization.


This work was inspired by a research article on arXiv ([link](https://arxiv.org/abs/2303.08792)), and the project reproduces and adapts some of the methods proposed in that paper for email phishing detection.
## 🚀App Features

- Upload any `.eml` email file  
- Automatic text extraction and preprocessing  
- Multi-language support using **spaCy**  
- Classification using **Logistic Regression** or **SVM**  
- Visual prediction indicator (0 = ham, 1 = phishing)  
- Phishing Indicator

- ## 📊 Evaluation Results

Below are the key evaluation visuals generated during model training.

### 🔹 Confusion Matrix
This matrix shows how well the model distinguishes between phishing and ham emails:

![logistic Confusion Matrix]
<img width="507" height="432" alt="1c6a7ebd-06f9-44f3-be45-841b369b2014" src="https://github.com/user-attachments/assets/ff44eba3-2254-4a31-858b-083f398e78f6" />

![SVM_Confusion Matrix](../reports/figures/logistic_confusion_matrix.png)


### 🔹 Logistic Regression vs SVM — Precision & Recall Comparison
This plot compares the precision and recall of both models:

![Evaluation Comparison](../reports/figures/evaluation_comparison.png)

🙌 Contributions

Feel free to clone and improve the preprocessing, add new models, or optimize the Streamlit UI. 

