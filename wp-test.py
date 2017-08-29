from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
import bs4 as bs
import urllib.request
from urllib.parse import *

"""The following files is under development. You can work and solve this issue"""

"""The wordpress_xmlrpc is not allowed to access the wordpress site"""

wp = Client('http://example.com/dir/xmlrpc.php', 'username', 'password')

sauce = urllib.request.urlopen('http://www.trustedreviews.com/').read()

soup = bs.BeautifulSoup(sauce, 'lxml')

body = soup.body
#for para in body.find_all('p'):
#    print(para.text)

strin = input('Hello akash! Please enter the title of the post : \n')
str_a = strin.split()
#print(str_a)

post = WordPressPost()
post.title = 'Samsung Galaxy S8'
p = ''
q = ''
for url in body.find_all('a'):
#    print(url.text)
#    print(url.get('href'))

    counter = 0
    for str in str_a:
        if str in url.text.lower():
            counter = counter + 1
    comp = len(str_a)*2/3
    if counter >= comp:
        present_url = url.get('href')
#        print(type(present_url))		for viewing the datatype of url
        try:
            present_page = urllib.request.urlopen(present_url).read()
        except ValueError as e:
#            continue
            parsed = urlparse(present_url)
            mod_parsed = parsed._replace(scheme='http', netloc='www.trustedreviews.com')
            present_url = urlunparse(mod_parsed)
            present_page = urllib.request.urlopen(present_url).read()
        present_soup = bs.BeautifulSoup(present_page, 'lxml')
        present_body = present_soup.body
        for para in present_body.find_all('p'):
            #print(type(para))
            #print(para.text)
            p = p + '\n' + para.text
        post.content = p
        wp.call(NewPost(post))
