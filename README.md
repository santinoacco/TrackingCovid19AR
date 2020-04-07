# Tracking the evolution of Covid-19 in Argentina using data from the Health-ministry and other sources like Google News

## Required packages

>-  pandas
>-  numpy
>-  matplotlib and seaborn :: for plotting
>-  os
>-  requests :: to get url data
>-  bs4 :: to work with json files
>-  PyPDF2 :: to read PDFs
>-  re :: for regular expressions
>-  news-api, install like: sudo pip3 install newsapi-python
>-  my personal library which you can find: https://github.com/santinoacco/MySetup/tree/master/Python 

## Workflow

### 'scrapperCov19.py'

    This is a web scrapper that gets the PDF files from the official
    Health-ministry.

### 'extract_patterns.py'
    
    This is a data analysis script to read the pdfs and extract relevant information.
    In addition it plots the data.

## Run
    First run  'scrapperCov19.py' to get the updated data:
    >- $ python3 scrapperCov19.py
    
    Sencond run 'extract_patterns.py' to get info from data:
    >- $ python3 extract_patterns.py -I '<input_folder>' -O '<output_folder>'
    
    example:
    >- $ python3  extract_patterns.py -I 'Data_Covid19_Ar_pdf' -O 'Output_Covid19'

## Pre results
![](src/images/new_and_tot.png)
![](src/images/new_vs_tot.png)    
