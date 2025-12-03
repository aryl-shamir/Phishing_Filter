from sklearn.base import BaseEstimator, TransformerMixin
import re 
import spacy
from .email_structure import email_to_text, email_language, translate_into_english
MAX_CHARS = 5000


# # from phishing_filter.email_structure import (load_email, get_email_structure,
#                                              structure_counter, html_to_plain_text,
#                                              email_to_text, email_language,
#                                              translate_into_english
#                                              )
# -----------------------------------------------------------------------------------------------------
spacy_models = {
    'en': 'en_core_web_sm',
    'fr': 'fr_core_news_sm',
    'de': 'de_core_news_sm',
    'pt': "pt_core_news_sm",
    'nl': "nl_core_news_sm",
    'es': "es_core_news_sm",
} # we don't use the vi because spacy has ot yet created a pipeline for that.

_cached_models = {} # Private cached models

def get_spacy_model(lang):
    if lang not in _cached_models:
        if lang not in spacy_models:
            raise ValueError(f"Unsupported language: {lang}")
        _cached_models[lang] = spacy.load(spacy_models[lang])
    return _cached_models[lang]

# -----------------------------------------------------------------------------------------------------


def clean_text(text):
    # creating a sanitizer for each emails.
    """ sanitize the email text.
    encode: convert the python string into bytes. if there is a word that can't be encode it is been replace by (?)
    decode: convert the bytes back to string 
    """
    return text.encode("utf-8", "replace").decode("utf-8", "replace")

# -----------------------------------------------------------------------------------------------------

# it is a function that return exactly what it takes.
def identity(tokens):
    return(tokens)

# -----------------------------------------------------------------------------------------------------

class EmailToTokens (BaseEstimator, TransformerMixin):
    # creating a transformer capable of preprocessing or parsing an email 
    def __init__(self, tokenization=True, strip_header=True, lower_case=True):
        self.strip_header = strip_header
        self.lower_case = lower_case
        self.tokenization = tokenization

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        all_tokens = []

        for email in X:
            tokens = []
            
            text = email_to_text(email) or ""
            
            # Clean unicode 
            text = clean_text(text)
            
            # Truncate long text
            if len(text) > MAX_CHARS:
                text = text[:MAX_CHARS]
            
            lang = email_language(email) or "en"
            
            try:
                nlp =  get_spacy_model(lang)
            except ValueError:
                # unsupported language → translate to English
                email = translate_into_english(email)
                lang = 'en'
                nlp = get_spacy_model('en')

            if self.lower_case:
                text = text.lower()

            doc = nlp(text)

            for token in doc:
                # Replace URLs
                if token.like_url:
                    tokens.append("URL")
                    continue

                # Skip pure numbers
                if token.like_num or token.text.isdigit():
                    continue

                # Mixed alphanumeric: keep only letters
                if re.search(r"[A-Za-z]", token.text) and re.search(r"\d", token.text):
                    cleaned = re.sub(r"\d", "", token.text)
                    tokens.append(cleaned.lower())
                    continue

                # Skip punctuation, symbols, stop words
                if token.is_punct or token.is_stop or not token.is_alpha:
                    continue
                
                # Lemma
                lemma = token.lemma_.strip()
                if lemma:
                    tokens.append(lemma)

            all_tokens.append(tokens)

        return all_tokens    