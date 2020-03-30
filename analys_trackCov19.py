import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import PyPDF2

# --Open pdfs and get relevant data
pdfFObj = open(out_pdf_filename,'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFObj)
num_pages = pdfReader.numPages
print(f'pdf file has {num_pages} pages')

textObjList=[]
#files_text = {filename:''}
for page in range(num_pages):
    pageObj=pdfReader.getPage(page)
    textObjList.append(pageObj.extractText())
    
    #paragraphs = textObjList[page].split('. ')
    #for pgh in paragraphs:
    #    sentence = pgh.split('.')
    #    for line in sentence:
    #        line.replace('\n','')
    #        
    #        print(line.find('confirmado'))
                 

        
    #print(paragraphs)
#df = pd.DataFrame(
#        textObjList,
#        columns=['paragraphs'],
#        dtype=pd.StringDtype())
#
#print(df.size)
#print(df.head())
#df['paragraphs'].replace('\n','')

# --how many confirmed cases in a given day
