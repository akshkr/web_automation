import bs4 as bs
import urllib.request
from urllib.parse import *

"""The following method is depricated for the application. It works when a website is specified."""

def get_content(web_url, topic_str):
    #u = 'http://www.digit.in/'
    sauce = urllib.request.urlopen(web_url).read()

    soup = bs.BeautifulSoup(sauce, 'lxml')

    body = soup.body
    #for para in body.find_all('p'):
    #    print(para.text)

    #strin = input('Hello akash! Please enter the title of the post : \n')
    strin = topic_str
    str_a = strin.split()
    #print(str_a)
    tex = []

    p = ''
    q = ''

    for url in body.find_all('a'):
    #    print(url.text)
    #    print(url.get('href'))

        counter = 0
        for str in str_a:
            if str in url.text.lower():
                counter = counter + 1
        comp = len(str_a)
        if counter >= comp:
            present_url = url.get('href')
    #        print(type(present_url))		for viewing the datatype of url
            try:
                present_page = urllib.request.urlopen(present_url).read()
            except ValueError as e:
    #            continue
                p_parsed = urlparse(web_url)
                parsed = urlparse(present_url)
                mod_parsed = parsed._replace(scheme=p_parsed.scheme, netloc=p_parsed.netloc)
                present_url = urlunparse(mod_parsed)
                present_page = urllib.request.urlopen(present_url).read()
            present_soup = bs.BeautifulSoup(present_page, 'lxml')
            present_body = present_soup.body
            for para in present_body.find_all('p'):
                #print(type(para))
                #print(para.text)
                q = para.text
                if find_i(q) is True:
                    continue
                if len(q) > 200:
                    #print ('a')
                    #p = p + para.text
                    #p = p + '\n\n\n'
                    tex.append(para.text)
    return tex

def find_i(text):
    s_text = text.split()
    for wrds in s_text:
        if wrds == "I":
            return True
    return False
