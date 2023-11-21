import streamlit as st
import urllib.request
import json
import ssl
import os

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

def call_api(data):
    allowSelfSignedHttps(True)
    body = str.encode(json.dumps(data))
    url = 'https://aekanun-deploy-21dec2023.eastus.inference.ml.azure.com/score'
    api_key = '0QuDIDpd0MmgJuPSbsyAQz2vV4RwvivB'
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        return result
    except urllib.error.HTTPError as error:
        return "Error: " + str(error)

# Streamlit UI
st.title('API Call Interface')

data_input = st.text_area("Enter your data here")
if st.button('Call API'):
    result = call_api(json.loads(data_input))
    st.text("API Response:")
    st.write(result)
