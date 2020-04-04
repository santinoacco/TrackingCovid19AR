import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup 

url_GoogleNews='https://news.google.com/stories/CAAqOQgKIjNDQklTSURvSmMzUnZjbmt0TXpZd1NoTUtFUWkzNzVhWms0QU1FVlRrNTdKN1BfNmFLQUFQAQ?hl=es-419&gl=AR&ceid=AR%3Aes-419&so=1'
source = requests.get(url_GoogleNews).text

soup = BeautifulSoup(source, 'lxml')

#article = soup.find('div',class_='IlBwEZb.BL5WZbRr.xP6mwf')
#article = soup.find('a')
#article = soup.find_all('a',class_='VDXfz')
article = soup.find('article')
print(len(article))
#print(article.prettify())
#
#print(article[1].prettify())
#print()
#print(article[1]['href'])
href_prefix ='https://news.google.com'
for link in soup.find_all('a'):
    print(link.get('href'))
    sufix = link.get('href')
    print(sufix)
    full_link = href_prefix + sufix
    print(full_link)
