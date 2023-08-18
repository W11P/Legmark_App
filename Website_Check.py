import re
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import time
from PIL import Image
image = Image.open('./legmark_logo.png')
#image = Image.open('C:\\Users\\wil\\PycharmProjects\\pythonProject1\\pythonProject\\Legmark_app\\venv\\legmark_logo.png')
st.image(image)


internal_urls = set()
external_urls = set()
title_urls = set()
url_crawled = []  # page crawled
titles = []  # title text for each page
title_length = []  # lenght of the title (characters)
page_status = []
meta_desc = []  # meta description text
meta_desc_words = []  # meta description number of words
meta_desc_length = []  # meta description number of characters
number_words_on_page = []
numb_internal_links = []
numb_external_links = []
internal_link_list_for_each_page = []
external_link_list_for_each_page = []
none_webpage_links = []
error_links = []
h1_1 = []
h1_2 = []
h1_3 = []
h1_1_letters = []
h1_1_word = []
h1_2_letters = []
h1_2_word = []
h1_3_letters = []
h1_3_word = []


global initial_url
#initial_url = "https://legmark.com"
#st.text("You must own the website you are investigating")
initial_url = st.text_input("Enter Website?")
if initial_url=='':
    st.write('Input website')
    exit()

match = re.search(r'^https?://', initial_url)
if not match:
    initial_url = "https://" + initial_url

st.write(initial_url)

#start of wordcloud
st.set_option('deprecation.showPyplotGlobalUse', False)

soup = BeautifulSoup(requests.get(initial_url, headers={'User-Agent': 'Mozilla/5.0'}).content, "html.parser")
text = soup.get_text()
#print(text)

cleaned_text = re.sub('\t', "", text)
cleaned_texts = re.split('\n', cleaned_text)
cleaned_textss = "".join(cleaned_texts)
#st.write("Word Cloud Plot")
# using stopwords to remove extra words
stopwords = set(STOPWORDS)
wordcloud = WordCloud(background_color="white", max_words=
100, stopwords=stopwords).generate(cleaned_textss)
plt.imshow(wordcloud, interpolation = 'bilinear')
plt.axis("off")
plt.show()
st.pyplot()



def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url):

    urls = set()
    #domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    match = re.search(r'^www\.', domain_name)
    if match:
        domain_name=domain_name[match.end():]

    soup = BeautifulSoup(requests.get(url,headers={'User-Agent': 'Mozilla/5.0'}).content, "html.parser")
    number_ext_lx = 0
    number_int_lx = 0
    title_check = soup.find_all('title')
    if title_check != " " or title_check != None:
        get_title(soup)
        status_code_response = requests.get(url)
        page_status.append(status_code_response.status_code)
        get_heading_tags(soup)
        get_word_count(soup)
        get_meta_description(soup)
    for a_tag in soup.findAll("a"):
       # is_internal_link = False
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            number_int_lx += 1
            continue
        if domain_name not in href:
            # external link
            number_ext_lx += 1
            if href not in external_urls:

                external_urls.add(href)
                number_ext_lx +=1
            continue

        urls.add(href)
        internal_urls.add(href)
        number_int_lx += 1

    numb_internal_links.append(number_int_lx)
    numb_external_links.append(number_ext_lx)
    return urls



# number of urls visited so far will be stored here
total_urls_visited = 0


def get_title(soup):   # domain name of the URL without the protocol
    """
    word count needs to be between 50-60 characters long. use target key work and brand name if space
    """
    count_title = 0
    for title in soup.find_all('title'):
        if count_title ==0:
            count_title +=1
            if title == "" and title == None:
                #titles.append('no title')
                continue
            title_text = title.get_text()
            title_urls.add(title_text)
            #print(f'Tile -> {title_text}')
            titles.append(title_text)
            letters_in_title = len(title_text)#-title_text.count(" ")
            title_length.append(letters_in_title)


def get_heading_tags(soup):
    heading_tags = ['h1' ]#, 'h2', 'h3']
    i = 0
    heading_word_count = 0
    h1_1_check = True
    h1_2_check = True
    h1_3_check = True
    for tags in soup.find_all(heading_tags):
        if i == 3:
            break
        tags_text = tags.get_text()
        words_tags = len(tags_text.split())
        letters_in_tags = len(tags_text) #- tags_text.count(" ")
        heading_word_count = heading_word_count + letters_in_tags
        if i == 0:
            h1_1.append(tags_text)
            h1_1_letters.append(letters_in_tags)
            h1_1_word.append(words_tags)
            h1_1_check = False
        if i == 1:
            h1_2.append(tags_text)
            h1_2_letters.append(letters_in_tags)
            h1_2_word.append(words_tags)
            h1_2_check = False
        if i == 2:
            h1_3.append(tags_text)
            h1_3_letters.append(letters_in_tags)
            h1_3_word.append(words_tags)
            h1_3_check = False
        i += 1

    if h1_1_check:
        h1_1.append("No H1 Tag")
        h1_1_letters.append(0)
        h1_1_word.append(0)
    if h1_2_check:
        h1_2.append("No H1-2 Tag")
        h1_2_letters.append(0)
        h1_2_word.append(0)
    if h1_3_check:
        h1_3.append("No H1-3 Tag")
        h1_3_letters.append(0)
        h1_3_word.append(0)


def get_meta_description(soup):
    """
       word count needs to be between 100-160. This should be written in a way to encourage clikc throughs to the site.
    """

    meta_text_letters = 0
    meta_word = 0
    meta_description = soup.find('meta', attrs={'name': 'description'})
    try:
        meta_text =meta_description['content'] if meta_description else "No meta description"
        meta_desc.append(meta_text)
        if meta_text == "No meta description":
            meta_text=""
        meta_text_letters = len(meta_text)# - meta_text.count(" ")
        meta_word = len(meta_text.split())

        meta_desc_words.append(meta_word)
        meta_desc_length.append(meta_text_letters)
        #else:
        #    meta_desc.append('0')
        #    meta_desc_length.append('0')
    except(AttributeError, KeyError) as er:
        meta_desc.append('No Meta description')
        meta_desc_words.append('0')
        meta_desc_length.append('0')


def get_word_count(soup):
    """
    word count needs to be less than ???
    """
    number_of_word = 0
    for script in soup(["script", "style"]):
        script.clear()
    text = soup.get_text()
    word_list = text.split()
    number_of_word = len(word_list)
    number_words_on_page.append(number_of_word)
    ## use to find words
    # We get the words within paragrphs
#    text_p = (''.join(s.findAll(text=True)) for s in soup.findAll('p'))
#    c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))

    # We get the words within divs
#    text_div = (''.join(s.findAll(text=True)) for s in soup.findAll('div'))
#    c_div = Counter((x.rstrip(punctuation).lower() for y in text_div for x in y.split()))

    # We sum the two countesr and get a list with words count from most to less common
#    total = c_div + c_p
#    list_most_common_words = total.most_common()


def crawl(url, max_urls=100):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """

    global total_urls_visited
    total_urls_visited += 1

    url_crawled.append(url)
    links = get_all_website_links(url)

    for link in links:
        if not link.startswith('mailto:'):
            if total_urls_visited > max_urls:
                break
            crawl(link, max_urls=max_urls)

#tl - title needs to be within 50 to 60 if not turns red
def highlight_cells_tl(val, color_if_true, color_if_false):
    color = color_if_true if val <= 50 or val >= 60 else color_if_false
    return 'background-color: {}'.format(color)
#md - meta discription lenght
def highlight_cells_md(val, color_if_true, color_if_false):
    color = color_if_true if val <= 100 or val >= 160 else color_if_false
    return 'background-color: {}'.format(color)
def highlight_cells_st(val, color_if_true, color_if_false):
    color = color_if_true if val != 200 else color_if_false
    return 'background-color: {}'.format(color)

if __name__ == "__main__":


    crawl(initial_url)


    # progress
    latest_iteration = st.empty()
    bar = st.progress(0)
    for i in range(100):
        #latest_iteration.text(f'progess {i + 1}')
        bar.progress(i + 1)
        time.sleep(0.1)
    bar.empty()
    print(len(url_crawled),len(titles),len(title_length),len(page_status),len(meta_desc),len(meta_desc_words),len(meta_desc_length),len(number_words_on_page),len(h1_1))
    print(len(h1_1_letters),len(h1_1_word),len(numb_external_links),len(numb_internal_links))
    print(url_crawled)
    print(titles)

    scrape_table = pd.DataFrame({
        'Page': url_crawled,
        'Title': titles,
        'Title Length': title_length,
        'Page Status': page_status,
        'Meta Description': meta_desc,
        'Meta Word Count': meta_desc_words,
        'Meta Length': meta_desc_length,
        'Page Word Count': number_words_on_page,
        'H1-1': h1_1,
        'H1-1 Lenght': h1_1_letters,
        'H1-1 Words': h1_1_word,
#        'H1-2': h1_2,
#        'H1-2 Lenght': h1_2_letters,
#        'H1-2 Words': h1_2_word,
#        'H1-3': h1_3,
#        'H1-3 Lenght': h1_3_letters,
#        'H1-3 Words': h1_3_word,
        'Number Of Exernal Links': numb_external_links,
        'Number Of Internal Links': numb_internal_links,


        # 'External Links': external_link_list_for_each_page,
        # 'Internal Links': internal_link_list_for_each_page,
#        'Error Links on Page': error_links,
#        'None Scrapable links': none_webpage_links,
    })
    try:
        st.dataframe(scrape_table.style.applymap(highlight_cells_tl, color_if_true='red', color_if_false='',subset=['Title Length'])\
                 .applymap(highlight_cells_md, color_if_true='red', color_if_false='',subset=['Meta Length']) \
                     .applymap(highlight_cells_st, color_if_true='red', color_if_false='#90EE90'
                                                                                       '', subset=['Page Status']) )


    #st.dataframe(scrape_table)

        st.write("Total Links Followed:", (total_urls_visited))
        st.write("Total Internal links:", len(internal_urls))
        st.write("Total External links:", len(external_urls))
        st.write("Total URLs:", len(external_urls) + len(internal_urls))
    except(AttributeError, KeyError) as er:
        st.write("Sorry Error")
