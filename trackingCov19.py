import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup 
import PyPDF2
from os import mkdir
from os.path import join

# --Set url to web page
url_MSAR='https://www.argentina.gob.ar/coronavirus/informe-diario'
source = requests.get(url_MSAR).text
# --get json with bs4
soup = BeautifulSoup(source, 'lxml')
# --Get the article we are interested in
article = soup.find('div', class_='col-md-12 col-xs-12 col-sm-6')
print(len(article))
#print(article.prettify())

#
pdfDict={}
for date, link in zip(article.p, article.find_all('a')):
    # --Get date and link to pdf.
    pdf_date = date.split(' ')[4]
    pdf_link = link.get('href')
    pdfDict.update({pdf_date:pdf_link})

print(pdfDict)
t_pdf = pdfDict['29-03-2020']

# --Build dir to store pdfs
Ar_Data_dir = 'Data_Covid19_Ar_pdf'
try: mkdir(Ar_Data_dir)
except: pass

# --download and save pdf in dir
response = requests.get(t_pdf)
#print(response.status_code)

out_pdf_filename = join(Ar_Data_dir,'29-03-2020'+'.pdf')
with open(out_pdf_filename, 'wb') as f:
    f.write(response.content)


# --Open pdfs and get relevant data
pdfFObj = open(out_pdf_filename,'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFObj)
num_pages = pdfReader.numPages
print(f'pdf file has {num_pages} pages')

textObjList=[]
for page in range(num_pages):
    pageObj=pdfReader.getPage(page)
    textObjList.append(pageObj.extractText())

print(textObjList)

