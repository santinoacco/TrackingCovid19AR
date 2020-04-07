import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import PyPDF2
import re
import sys
from os import listdir
from os.path import join, splitext
from datetime import datetime
import NoaccoLibrary as Nlib
import argparse


def config_Parse():
    """
    Set all the configuration to your parser object.

    # Args::None

    # Returns::parser object.
    """
    parser = argparse.ArgumentParser('Covid_19')
    parser.add_argument('-I', '--Input', required=True, help='<Input folder or file/s>' )
    parser.add_argument('-O', '--Output', required=True, help='<Output folder or files/s>')
    parser.add_argument('-D','--Debug', required=False, help='Debug flag', action='store_true')
    parser.add_argument('-M','--MaxEvents', required=False, help='Set maximum of events. Default -1 == all', type=int, default=-1)
    return parser 

def get_pdf_content(path):
    """
    Get the content of the pdfs files store in path.     

    # Args::
        path: to dir of pdfs

    # Returns::
        pdf_dict: a dictionary keeping the full text of each pdf file.
    """  
    pdf_dict={}
    for filename in listdir(path): 
        # --Open pdfs and get relevant data
        pdfFObj = open(join(path,filename),'rb')
        
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
            
        pdf_dict[pdfKey] = full_text
    return pdf_dict

def presampler_pdf(pdf_dict):
    sentence_dict={}
    for k, text in pdf_dict.items():
        # --Replace newlines for nothing.
        text = text.replace('\n', '')
        # --Split sentences
        text = text.split('. ')
        
        key_sentences = []
        for sentence in text:
            # --Find keywords in text
            cases_confirmed = sentence.find('caso' and 'confirmado')
            # --Check that there are some digits at least
            has_digits = re.compile(r'\d+')
            match = has_digits.search(sentence)
            cond = (cases_confirmed != -1) and match != None
            if cond:
                key_sentences.append(sentence)
        
        sentence_dict[k] = key_sentences
    
    return sentence_dict

def look_for_patterns(sentence_dict, pattern_dict):
    data_dict={}
    not_data=[]
    for date, sent_list in sentence_dict.items():
        # --Delete empty lists
        if sent_list==[]: continue
        # --Setting keys to dictionary
        date_str, num_file = date.split('_')
        #date = datetime.strptime(date_str, '%d-%m-%Y').date()
        date = datetime.strptime(date_str, '%d-%m-%Y')
        data_dict[(date,num_file)]={}
        #print(f'========= {date} =========')
        for pattern_name, pattern_list in pattern_dict.items():
            pattern = pattern_list[0]
            digit_place_in_group = pattern_list[1]
            # --Find patterns in each sentence
            for sent in sent_list:
                matches = pattern.finditer(sent)
                for match in matches:
                    #print(match)
                    data = match.group(digit_place_in_group)
                    data_dict[(date,num_file)][pattern_name] = int(data)

        if data_dict[(date,num_file)] == {}:
            not_data.append((date,num_file))
            # --Transforming datetime to date
            date = date.date()
            print('===> unrecognized data:')
            print(sentence_dict[f'{date:%d-%m-%Y}_{num_file}'])
            #break

    return data_dict, not_data 

def main(argv):
    parser = config_Parse()
    args = parser.parse_args()    
    
    output_dir = args.Output
    
    # --Get raw data
    pdfDict = get_pdf_content(args.Input)
    # --Get a dictionary with relevant sentences
    sentence_dict = presampler_pdf(pdfDict)
    #print(type(sentence_dict.keys()))
    #print(  )

    # --Make a dictionary to store all paterns to extract,
    #   and the position of the digit
    pattern_dict = {
            'new_confirmed_AR':
            [re.compile(r'confirmados?(\s+\w+)? \(?(\d{1,5})\)?( nuevos casos)?'),2],
            'tot_confirmed_AR':
            [re.compile(r'total(e|es)?( \w+)? casos confirmados?( \w+)+ (\d{1,5})( total(e|es)?)?'),4],
            }


    data_dict, not_data = look_for_patterns(sentence_dict, pattern_dict)

    
    # --Create a pd.DataFrame
    df=pd.DataFrame.from_dict(
            data_dict,
            orient='index',
            columns=[
                'new_confirmed_AR',
                'tot_confirmed_AR'
                ],
            )

    df.sort_index(inplace=True)
    # --Store df in csv file.
    out_csv = Nlib.build_dir(output_dir,'Covid19_AR_data','.csv')
    df.to_csv(out_csv)
    print(f'* DataFrame saved to {out_csv}')

    #TODO: same date files add news together 
    NaN_val = df['tot_confirmed_AR'].isna() 
    NaN_val = df[NaN_val]
    # --Replace NaN values in tot_confirmed by summing up to date the new cases
    for index, row in df[NaN_val].iterrows():
        new_tot_val = df.loc[:index,'new_confirmed_AR'].sum()
        print(new_tot_val)
        df.loc[index,'tot_confirmed_AR'] = int(new_tot_val)



    #TODO: add update on provinces
    df['new/tot'] = np.round(df['new_confirmed_AR']/df['tot_confirmed_AR'], 2)
    #print(df['new/tot'].head())

    
    #print(df.index)
    #print(df.loc[('2020-03-16','1'):('2020-03-24','1'),'tot_confirmed_AR'].sum())
    print()
    
    #df = df[NaN_val].loc[:NaN_val.index,'new_confirmed_AR'].sum()

   # print(df)

    # TODO: improve the format of the plots
    m_outfile = Nlib.build_dir('images','new_and_tot','.png')
    m_fig, ax = plt.subplots()
    ax.axis(option='tight')
    m1_param = {
            'marker':'o',
            'color':'grey',
            'linestyle':'--',
            'label':'new cases',
            }
    m2_param = {
            'marker':'o',
            'color':'green',
            'linestyle':'--',
            'label':'total cases',
            }
    dates = df.index.get_level_values(0)
    #print(dates.dtype)
    plt.plot_date(
            dates,
            df['new_confirmed_AR'],
            **m1_param
            )
    plt.plot_date(
            dates,
            df['tot_confirmed_AR'],
            **m2_param
            )
    
    plt.xlabel('date')
    plt.legend()
    plt.savefig(m_outfile)

    m2_outfile = Nlib.build_dir('images','new_vs_tot','.png')
    m2_fig, ax2 =plt.subplots()
    ax2.axis(option='tight')
    m3_param = {
            'marker':'3',
            'color':'red',
            'linestyle':'--',
            'label':f'new/tot cases',
            }
    plt.plot_date(
            dates,
            df['new/tot'],
            **m3_param
            )
    plt.xlabel('date')
    plt.legend()
    plt.savefig(m2_outfile)
    #plt.show()

    
    return

if __name__ == '__main__':
     main(sys.argv[1:])


states =[
        'Jujuy',
        'Salta',
        'Chaco',
        'Formosa',
        'Misiones',
        'Catamarca',
        'La Rioja',
        'Tucumán',
        'Entre Ríos',
        'Santiago del Estero',
        'Santa Fe',
        'Ciudad Autónoma de Buenos Aires',
        'Buenos Aires',
        'Córdoba',
        'La Pampa',
        'Mendoza',
        'San Luís',
        'San Juan',
        'Neuquén',
        'Río Negro',
        'Chubut',
        'Santa Cruz',
        'Tierra del Fuego'
        ]

#print(sentence_dict['08-03-2020_1'])
#print(sentence_dict['15-03-2020_1'])

country_data_kwords = [r'confirmado \d+ ']
state_data_kwords = ['provincia ']
death_rate_kwords = ['fallecido', 'muerto']

time_ref_w = ['hoy','ayer']

has_digits = re.compile(r'\d+')

#pattern = re.compile(r'confirmados?( \w+)+(\d+)')



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

#Nlib.my_plotter_2D(
#        ax,
#        df.index,
#        df['new_confirmed_AR'],
#        m_param
#        )

'''
sns.lineplot(
        df.index,
        df['new_confirmed_AR'],
        palette="tab10",
        linewidth=2.5)
'''
#plt.show()
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
