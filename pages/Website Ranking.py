
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
    #st.write(new_key_word)

    #key_words = "SEO"
    target_url='https://www.google.co.uk/search?q='+new_key_word+'&num=100'
    st.write(target_url)

    response = requests.get(target_url, headers=headers)

    # Response status code from Google
    #print(response.status_code)

    # Parse response into Beautiful Soup
    soup = BeautifulSoup(response.text,'html.parser')

    # Extract all search results by looking up the first class
    results = soup.find_all("div", class_="MjjYud")

    #st.write(results)
    position = 0
    for result in range(0,len(results)):

        #st.write(results[result].prettify())
        # Parse each url and look for the class yuRUbf to make get the correct URL
        try:
            web_site=results[result].find(class_='qLRx3b tjvcx GvPZzd cHaqb').text
        #    st.write(result, web_site)
        except:
        #    st.title(result,"not here")
            pass

        try:
            link= urlparse(results[result].find('a').get('href')).netloc
            #st.write(link)
            #st.write(len(link))
            if len(link)==0:
               # st.write('pick it up')
                pass
        #except:
        #    pass
        #if link is not None or link != " " or link != "" or len(link)==0:
            else:# len(link)!=0 or link is not None or link !="" or link !=" ":
                st.write(len(link))
                link = remove_www(link)
                #print(link)
                site_position.append(link)
                lenth.append(len(link))
                #st.write(link)
                if(link == search_for_domain):
                    found = True
                    position = result

                    break;
                else:
                    found = False
        except:
            pass
    # We found the domain we are looking for
    if(found == True):
        st.write("Found at position", position)

    # We did not find the domain we are looking for
    else:
        st.write("Not found in top", len(results))

    df=pd.DataFrame({'Website Ranking':site_position})
    st.dataframe(df)
