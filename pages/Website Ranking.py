
import requests
import streamlit as st
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd
import re
def remove_www(text):
  return re.sub(r"www\.(\w+)", r"\1", text)

site_position=[]
lenth =[]
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36','referer':'https://www.google.co.uk'}

search_for_domain = st.text_input('Website name: (e.g. Legmark.com)') #"legmark.com"
search_for_domain = remove_www(search_for_domain)
key_words= st.text_input('Keyword Search:')
if key_words != "":

    new_key_word=""
    for space in key_words:
        if space == " ":
            new_key_word +="+"
        else:
            new_key_word += space

    target_url='https://www.google.co.uk/search?q='+new_key_word+'&num=20'
    st.write(target_url)

    response = requests.get(target_url, headers=headers)

    # Parse response into Beautiful Soup
    soup = BeautifulSoup(response.text,'html.parser')
  
    st.write(soup.prettify())
    # Extract all search results by looking up the first class
    results = soup.find_all("div", class_="MjjYud")
    #st.write(results)
   
    position = 0
    for result in range(0,len(results)):

        # Parse each url and look for the class yuRUbf to make get the correct URL
        try:

            web_site = results[result].find(class_='VuuXrf').text
            st.write(web_site)
        except:

            pass

        try:
            link= urlparse(results[result].find('a').get('href')).netloc
            if len(link)==0:
                pass
            else:
             
                link = remove_www(link)
                
                site_position.append(link)
                lenth.append(len(link))
           
                if(link == search_for_domain):
                    found = True
                    position = result

                    break;
                else:
                    found = False
        except:
            pass
    
    if(found == True):
        st.write("Found at position", position)

   
    else:
        st.write("Not found in top", len(results))

    df=pd.DataFrame({'Website Ranking':site_position})
    st.dataframe(df)
