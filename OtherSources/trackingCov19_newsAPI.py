import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import json


#install like: sudo pip3 install newsapi-python
from newsapi import NewsApiClient
# Init
newsapi = NewsApiClient(api_key='9ea9bd56b9394a138eb85071e3db7629')

# Get data from news
Covid_data = newsapi.get_everything(
        q='Covid-19, corona, virus',
        sources='lanacion,infobae,lmcipolletti,eldestapeweb,perfil',
        domains='lanacion.com.ar,infobae.com,lmcipolletti.com,eldestapeweb.com,perfil.com',
        from_param='2020-03-01',
        to='2020-03-25',
        language='es',
        sort_by='publishedAt',
        )
#print(type(all_articles))
#print(all_articles.keys())
#print(all_articles['totalResults'])

print(Covid_data['totalResults'])
#print(Covid_data.keys())
#print(type(Covid_data['articles']))
df = pd.DataFrame(Covid_data['articles'])
#print(df['source'].array)
#df['source'] = df['source'].array
#print(df['source']['name'])
df.set_index('publishedAt', inplace=True)

#print(df['urlToImage'][0])
#print(df['title'][1])
df.drop(columns=['urlToImage','description'],inplace=True)
#print(df.head())
# --The issue is that content is truncated at 260 char
content = df['content']
#print(content[0][:])

#print(df)
#print(df.columns)

keywords1='caso'
keywords2='confimado'
keywords3=['covid-19','corona virus', 'coronavirus']

#print(content.array)
#print(type(content))
#print(type(content.str))
#print(any(keywords1))


first_trim = df[content.str.contains(keywords3[0] or keywords3[1] or keywords3[2],case=False)]
#print(first_trim.size)
#print(first_trim.columns)
#content = first_trim['content']
#print(content)
second_trim = first_trim[content.str.contains(keywords1[1],case=False)]
#first_trim = df[content.str.contains(any(keywords1) and keywords2 and any(keywords3))]
#first_trim = df[content.array.contains(any(keywords1) and keywords2 and any(keywords3))]

print(len(second_trim))
print(second_trim['content'])



