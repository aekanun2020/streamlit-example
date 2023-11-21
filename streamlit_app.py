import streamlit as st
import urllib.request
import json
import ssl
import os

def allowSelfSignedHttps(allowed):
    # Bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

def call_api(text):
    allowSelfSignedHttps(True)

    # สร้างข้อมูลที่จะส่งไปยัง API
    data = {"question": text}
    body = str.encode(json.dumps(data))

    url = 'https://aekanun-deploy-21dec2023.eastus.inference.ml.azure.com/score'
    api_key = '0QuDIDpd0MmgJuPSbsyAQz2vV4RwvivB'
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + api_key}
    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        # แปลงผลลัพธ์จาก bytes เป็น string
        result = response.read().decode('utf-8')
        return result
    except urllib.error.HTTPError as error:
        return f"Error: {error}"

# Streamlit UI
st.title('สวัสดีครับ ผมครูเอ้เองครับ มาในเวอร์ชั่นของ Generative AI')

# รับข้อมูลเป็นข้อความธรรมดา
text_input = st.text_area("ท่านอยากรู้อะไรในเรื่องที่ครูได้บรรยายไปบ้างครับ")
if st.button('สอบถามครู'):
    try:
        # ส่งข้อความไปยัง API
        result = call_api(text_input)

        # แสดงผลลัพธ์โดยตรง
        st.json(json.loads(result))  # แสดงผลลัพธ์ในรูปแบบ JSON
    except Exception as e:
        st.error(f"An error occurred: {e}")
