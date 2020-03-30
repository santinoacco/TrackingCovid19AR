#!/usr/bin/env python3
'''
Script for web scrapping to get official articles
of COVID-19 situation in AR.
'''
import requests
from bs4 import BeautifulSoup 
from os import mkdir
from os.path import join

#TODO: add timer to download files 

# --Set url to web page
url_MSAR='https://www.argentina.gob.ar/coronavirus/informe-diario'
source = requests.get(url_MSAR).text
# --get json with bs4
soup = BeautifulSoup(source, 'lxml')
# --Get the articles we are interested in
articles = soup.find_all('div', class_='col-md-12 col-xs-12 col-sm-6')
print(len(articles))
#print(articles.prettify())

pdfDict={}
for article in articles:
    for date, link in zip(article.p, article.find_all('a')):
        # --Get date and link to pdf.
        pdf_date = date.split('/')[1].split(' ')[1]
        pdf_link = link.get('href')
        try: pdfDict[pdf_date].append(pdf_link)
        except KeyError: pdfDict[pdf_date]=[pdf_link]

print(pdfDict)

# --Build dir to store pdfs
Ar_Data_dir = 'Data_Covid19_Ar_pdf'
try: mkdir(Ar_Data_dir)
except: pass


for date, v_link in pdfDict.items():
    # --When we have to files with the same date,
    # --link will have a lenght > 1.
    num_link=0
    for l in v_link:
        # --download and save pdf in dir
        print(l)
        response = requests.get(l)
        #print(response.status_code)
        num_link+=1
    
        out_pdf_filename = join(
                Ar_Data_dir,
                f'RDV_{num_link}_{date}.pdf'
                )
        #TODO: check if file exist before creating a new one
        with open(out_pdf_filename, 'wb') as f:
            f.write(response.content)

