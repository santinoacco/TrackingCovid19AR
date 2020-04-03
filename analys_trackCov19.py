import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import PyPDF2
import re
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

#test = pdfDict['24-03-2020_1']
#print(type(test))
#test = pdfDict[].replace('\n', ' ')
#test = test.split('. ')

sentence_dict={}
for k, text in pdfDict.items():
    # --Replace newlines for nothing.
    text = text.replace('\n', '')
    # --Split sentences
    text = text.split('. ')
    
    key_sentences = []
    #key_sentences = ""
    for sentence in text:
        # --Find keywords in text
        cases_confirmed = sentence.find('caso' and 'confirmado')
        # --Check that there are some digits at least
        has_digits = re.compile(r'\d+')
        match = has_digits.search(sentence)
        cond = (cases_confirmed != -1) and match != None
        if cond:
            key_sentences.append(sentence)
            #key_sentences += sentence + '\n'

    
    sentence_dict[k]= key_sentences


#print(sentence_dict)
print(sentence_dict['08-03-2020_1'])
print(sentence_dict['15-03-2020_1'])

country_data_kwords = [r'confirmado \d+ ']
state_data_kwords = ['provincia ']
death_rate_kwords = ['fallecido', 'muerto']

time_ref_w = ['hoy','ayer']

has_digits = re.compile(r'\d+')

#pattern = re.compile(r'confirmados?( \w+)+(\d+)')

states =['Ciudad Autónoma de Buenos Aires', 'Buenos Aires', 'Chaco', 'Formosa', 'Salta', 'Jujuy', 'Mendoza']


#matches = pattern.finditer(sentence_dict['24-03-2020_1'][0])
#for sent in sentence_dict['24-03-2020_1']:
#    matches = pattern.finditer(sent)
#    for match in matches:
#        print(match)
#
#pattern = re.compile(r'(nuevos)? ( \w+)+ confirmados?( \w+)+ (\d{1,5}) (nuevos)?')
#pattern = re.compile(r'confirmados?( \w+)* (\d{1,5})( nuevos casos)?')
#pattern = re.compile(r'confirmados? (\d{1,5}) (nuevos casos)?')
#pattern = re.compile(r'total(e|es)?( \w+)? casos confirmados?( \w+)+ (\d{1,5})( total(e|es)?)?')

# --Make a dictionary to store all paterns to extract,
#   and the position of the digit
pattern_dict = {
        'new_confirmed_AR':
        [re.compile(r'confirmados?( \w+)? \(?(\d{1,5})\)?( nuevos casos)?'),2],
        'tot_confirmed_AR':
        [re.compile(r'total(e|es)?( \w+)? casos confirmados?( \w+)+ (\d{1,5})( total(e|es)?)?'),4],
        }


data_dict={}
not_data=[]
for date, sent_list in sentence_dict.items():
    #print(sent)
    data_dict[date]={}
    #print(f'========= {date} =========')
    for pattern_name, pattern_list in pattern_dict.items():
        pattern = pattern_list[0]
        digit_place_in_group = pattern_list[1]
        for sent in sent_list:
            matches = pattern.finditer(sent)
            for match in matches:
                #print(match)
                data = match.group(digit_place_in_group)
                #print(data)
                data_dict[date][pattern_name] = int(data)
    if data_dict[date] == {}:
        not_data.append(date)
    #print()
#print(data_dict.items())

df=pd.DataFrame.from_dict(
        data_dict,
        orient='index',
        columns=['new_confirmed_AR','tot_confirmed_AR'],
        #dtype=pd.StringDtype()
        )

df.sort_index(inplace=True)
#print(df.index)
#print(len(df['full_text'].str.split('\n')))
#print(df.loc[:,'full_text'].str.split('\n'))
#df['num_sentences'] = len(df.loc[:,'full_text'].str.split('\n'))
#df['confirmed_cases'] = df[df.loc[:,'full_text'].str.contains('casos \d+' or '\d+ casos')]
print(not_data)

print(df.head())

# TODO: store data in file
# TODO: improve the format of the plots
plt.plot(
        df.index,
        df['new_confirmed_AR'],
        'bo--',
        label='new cases',
        )
plt.plot(
        df.index,
        df['tot_confirmed_AR'],
        'k+--',
        label='total cases',
        )
plt.xlabel('date')
plt.legend()
plt.show()
#print(df.tail())

'''
sns.lineplot(
        df.index,
        df['new_confirmed_AR'],
        palette="tab10",
        linewidth=2.5)
'''
plt.show()
'''
#test = df[df['full_text'].str.contains('casos')]

#print(test.head())
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
