import email 
import email.policy
from collections import Counter
from bs4 import BeautifulSoup
from html import unescape
from langdetect import detect
from deep_translator import GoogleTranslator
from typing import Union, IO
from pathlib import Path

#----------------------------------------------------------------------------------------------------------

def load_email(email_file: Union[str, Path, IO, object]):
    raw_bytes = email_file.read()
    return email.parser.BytesParser(policy=email.policy.default).parsebytes(raw_bytes)
    
    #Read all the data from the binary file-like object fp, parse the resulting bytes,
    # and return the message object.fp must support both the readline() and the read() methods.
    
# ------------------------------------------------------------------------------------------------------   
def get_email_structure(email):
    if isinstance(email, str):
        return email
    payload = email.get_payload()
    if isinstance(payload, list):
        multipart = ','.join([get_email_structure(subemail) for subemail in payload])
        return f'multipart({multipart})' # In case an email has multipart ( html, images)
    else:
        return email.get_content_type()
    
# ------------------------------------------------------------------------------------------------------

def structure_counter(emails):
    structures = Counter()
    for email in emails:
        structure = get_email_structure(email)
        structures[structure] += 1 # Increament by one each time it sees thesame structure of an email
    return structures
        
 # ------------------------------------------------------------------------------------------------------
        
def html_to_plain_text(html_email):
    # sample = email.get_content(), source of big errors, becasue html is already a string, so html_email.get_content gives an error because it is not an email 
    soup = BeautifulSoup(html_email, 'html.parser')
    
    # Remove the <head> section
    if soup.head:
        soup.head.decompose()
        
    #Replace the <a> tag by HYPERLINK
    for link in soup.find_all('a'):
        link.replace_with('HYPERLINK')
        
    #Get only the text form the email 
    text = soup.get_text()
    
    # clean up extra lines and spaces 
    cleaned_text = '\n'.join([line.strip() for line in text.splitlines() if line.strip()])
    return unescape(cleaned_text)

# ------------------------------------------------------------------------------------------------------

  
def email_to_text(email):
    html = None
    
     # Gives the format 
    for part in email.walk():
        ctype = part.get_content_type()
        
        # Skip subpart of multiparts not in ('text/html', 'text/plain'), so we'll not have to dealwith them becasue they don't have the get_content() method. 
        if ctype not in ('text/html', 'text/plain'):
            continue 
    
        try:
            content = part.get_content()
        except: # We 
            content = str(part.get_payload(decode=True))# This retrieves the raw payload bytes, and decode=True tries to: base64 decode
            # if isinstance(content, bytes):
            #     content = content.decode(errors="ignore") # convert bytes into string
                  
        if ctype == 'text/plain':
            return content
        else:
            html = content 
            
    if html:
        return html_to_plain_text(html)
    return ""  # fallback in case nothing is found

# ------------------------------------------------------------------------------------------------------


def email_language(email):
    email_text = email_to_text(email)
    
    # If no text was extracted, use empty string instead of None
    if not email_text:
        return "unknown"
    
    try:
        return detect(email_text)
    except:
        return "unknown"
#--------------------------------------------------------------------------------------------------------

def translate_into_english(email):
    text = email_to_text(email)
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text
    
# --------------------------------------------------------------------------------------------------------
