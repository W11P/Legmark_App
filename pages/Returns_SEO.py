import pandas as pd
import streamlit as st
import requests
from pathlib import Path
from PIL import Image
import pytrends
from pytrends.request import TrendReq
import streamlit as st
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

def formula_lg(CTR,b,c,d):
    y = float(CTR)*float(b)*float(c)*int(d)
    return y

def remove_www(text):
  return re.sub(r"www\.(\w+)", r"\1", text)
#streamlit run C:/Users/wil/PycharmProjects/pythonProject1/pythonProject/Legmark_app/venv/SEO_Info.py [ARGUMENTS]
def website_keyword(key_word):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'referer': 'https://www.google.co.uk'}

    if key_word == '':
        st.write('Input Keyword:')
        exit()
    else:
        new_key_word = ""
        for space in key_word:
            if space == " ":
                new_key_word += "+"
            else:
                new_key_word += space
        target_url='https://www.google.co.uk/search?q='+new_key_word+'&num=100'
        #st.write(target_url)
        response = requests.get(target_url, headers=headers)
        soup = BeautifulSoup(response.text,'html.parser')
        results = soup.find_all("div", class_="MjjYud")
        position = 0
        for result in range(0, len(results)):

            try:
                link= urlparse(results[result].find('a').get('href')).netloc
            except:
                pass
            if len(link)!=0:
                link = remove_www(link)
                print(link)
                site_position.append(link)
                lenth.append(len(link))
                if(link == search_for_domain):
                    found = True
                    position = result

                    break;
                else:
                    found = False
        if(found == True):
            pass
            #st.write("Found at position", position)
        else:
            st.write("Not found in top", len(results))

        df=pd.DataFrame({'Website Ranking':site_position})
        return position
def keyword_ranking(keyword):
    requests_args = {
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
    }
    #headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36','referer':'https://www.google.co.uk'}

    pytrends = TrendReq(requests_args=requests_args)

    pytrends.build_payload(kw_list=[key_word], timeframe='today 1-m')
    iot =pytrends.interest_over_time()
    if iot.empty:
        st.write('No Search volume found')
        exit()

    iot_total_sum = 0
    for value in iot[key_word]:
        iot_total_sum += value

    st.write('The number of times the keyword {} has been searched each month is:'.format(key_word),iot_total_sum)
    return iot_total_sum
image = Image.open('./legmark_logo.png')

st.image(image)

search_for_domain = st.text_input('Website name: (e.g. Legmark.com)') #"legmark.com"
search_for_domain = remove_www(search_for_domain)
key_word =st.text_input('Keyword:')
site_position=[]
lenth =[]

if st.button('Website Ranking'):
   st.session_state.site_ranking = website_keyword(key_word)

if "site_ranking" in st.session_state and st.session_state.site_ranking != 0:
    st.write('Found At Position:', st.session_state.site_ranking)
    position = st.slider('Site Ranking',value =st.session_state.site_ranking,min_value=0,max_value=10,step=1)

if st.button('Key Word Searches'):
    iot_total_sum = keyword_ranking(key_word)
    st.session_state.iot_tot = iot_total_sum
if "iot_tot" in st.session_state and st.session_state.iot_tot != 0:
    pass
    #st.write('The number of times the keyword {} has been searched each month is:'.format(key_word), st.session_state.iot_tot )

#click_rate = st.slider('Click Through Rate',value =50,min_value=0,max_value= st.session_state.iot_tot,step=1)


web_rate =st.number_input('Website Conversation % Rate?',min_value=0, max_value=100,value = 5, step=1)
int_rate =st.slider('Internal Conversation % Rate?',value=10,min_value=0,max_value=100,step=1)
ave_cost_rate =st.number_input('Average Cost of Case',min_value=0,value = 1000,step=100)

if st.button('Calculate Returns'):
    if position <= 10 and position !=0:
        CTR_P = (0.398, 0.187, 0.102, 0.074, 0.051, 0.045, 0.034, 0.026, 0.024, 0.022)
        for i, value in enumerate(CTR_P):
            if i == position-1:
                CTR = value* st.session_state.iot_tot
                CTR_potential = 0.389*st.session_state.iot_tot
    else:
        st.write(f'Ranking not in the top 10')
        exit()
        
    b=web_rate/100
    c=int_rate/100
    d=ave_cost_rate
    st.write(f'Current Income=£{int(formula_lg(CTR,b,c,d))} per month')
    st.write(f'Potential Income=£ {int(formula_lg(CTR_potential,b,c,d))} per month if ranking at number 1')





if st.button("reset"):
    for key in session_state.keys():
        del st.session_state[key]

