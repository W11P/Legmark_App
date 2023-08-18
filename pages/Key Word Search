import time

import streamlit as st
import requests
import pandas as pd
from pytrends.request import TrendReq

#   pytrends = TrendReq(hl='en-US', tz=360)

requests_args = {
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
}

# Only need to run this once, the rest of requests will use the same session.
pytrends = TrendReq(requests_args=requests_args)


key_word =st.text_input('Keyword:')
if key_word == '':
    st.write('Input Keyword:')
    exit()
time.sleep(1)
pytrends.build_payload(kw_list=[key_word], timeframe='today 1-m')
iot =pytrends.interest_over_time()
if iot.empty:
    st.write('No Search volume found')
    exit()

iot_total_sum = 0
for value in iot[key_word]:
    iot_total_sum += value

st.write('The number of times the keyword {} has been searched each month is:'.format(key_word),iot_total_sum)

