import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import PyPDF2
from os import listdir
from os.path import join, splitext

pdfDir_path = '/home/santi_noacco/Desktop/Covid_19/TrackCovid19Ar/Data_Covid19_Ar_pdf'

pdfDict={}
for filename in listdir(pdfDir_path): 
    # --Open pdfs and get relevant data
    pdfFObj = open(join(pdfDir_path,filename),'rb')
    
    filename, ext = splitext(filename)
    numfile, date_file = filename.split('_')[1:]
    pdfKey=f'{date_file}_{numfile}'
    
    pdfReader = PyPDF2.PdfFileReader(pdfFObj)
    num_pages = pdfReader.numPages
    #print(f'pdf file has {num_pages} pages')
    full_text=""
    for page in range(num_pages):
        pageObj=pdfReader.getPage(page)
        full_text+= pageObj.extractText()
        

    pdfDict[pdfKey] = full_text

#test = pdfDict['24-03-2020_1'].splitlines()
#test = pdfDict[].replace('\n', ' ')
#test = test.split('. ')

sentence_dict={}
for k, text in pdfDict.items():
    text = text.replace('\n', ' ')
    text = text.split('. ')
    #print(text)
    
    key_sentences = []
    for sentence in text:
        # --Find keywords in text
        cases_confirmed = sentence.find('caso' and 'confirmado')
        if cases_confirmed != -1:
            key_sentences.append(sentence)

            print(sentence + '\n\n')
    
    sentence_dict[k]=key_sentences


print(sentence_dict)
#print(sentence_dict['24-03-2020_1'])

'''
df=pd.DataFrame.from_dict(
        pdfDict,
        orient='index',
        columns=['full_text'],
        dtype=pd.StringDtype()
        )

print(df.index)
#print(df.index[0])

test = df[df['full_text'].str.contains('casos')]

print(test.head())
##test = df['full_text'][0].replace('\n','None')
#test = df['full_text'].str.replace('\n', '  ')
##print(test[0])
#test = test.str.split('\. ')
#print(test[0])

#sentences = test.str.contains('casos')
#print(sentences)

#test = test.dropna()
#test = test.str.split('. ')
#test = df['full_text'].str.split('. ')
## --how many confirmed cases in a given day

#print(test.contains('casos'))
#cases = test.find('casos')
#print(cases)
#print(test.pop(cases))

#cases = df[df['full_text'].str.contains('casos')]
#print(cases)

#print(test.dropna(inplace=True))int(test[0])
'''
