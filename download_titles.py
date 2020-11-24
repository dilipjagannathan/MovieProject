# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 19:42:48 2020

@author: dilip
"""

import requests
import gzip
import os
import shutil
from find_movie_info import movie_data
from http_session import requests_retry_session
import pandas as pd
import concurrent.futures
    
file_path = os.getcwd()  
url = "https://datasets.imdbws.com/title.basics.tsv.gz"
headers = {'User-Agent': 'Safari'}
filename = url.split("/")[-1]

print ("Starting download..")
if not os.path.exists(file_path + os.sep + filename):
    print ("file does not exist:", filename)
    with open(filename, "wb") as f:
        session = requests.Session()
        r = requests_retry_session(session = session).get(url, headers=headers,
        timeout=300)
        r.raise_for_status()
        f.write(r.content)
        
if not os.path.exists(file_path + os.sep + 'title.basics.tsv'):   
    with gzip.open(filename, 'rb') as f_in:
        with open('title.basics.tsv', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        
       
output = pd.DataFrame()

output_file = 'output_df.csv'
if not os.path.exists(file_path + os.sep + output_file):
    data = []
    NUM_WORKERS = 4

    df = pd.read_csv('title.basics.tsv', sep='\t', low_memory=False)
    df.startYear = pd.to_numeric(df.startYear, errors='coerce')
    # filtering results to have only movies
    titleTypeFilter = ['movie']
    # filtering results for only categories that started after 2011 as the dataset is so huge
    # Considering only last 10 years
    filtered_df = df[df.startYear > 2010]
    filtered_df = filtered_df[filtered_df.titleType.isin(titleTypeFilter)]
    futures = []
    final_df = filtered_df
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        for index, row in final_df.iterrows():    
            movie_link = "https://www.imdb.com/title/" + row[0]
            session = requests.Session()
            futures.append(executor.submit(movie_data, movie_on_imdb=movie_link, session=session))

        for future in concurrent.futures.as_completed(futures):
            try :
                data.append(future.result())     
            except Exception as x:
                print('It failed :(', x.__class__.__name__)

                
    result = []
    for dataRow in data:
        if dataRow != None :
            result.append(dataRow)  
    output = output.append(result, True)      
    new_columns = output.IMDB_link.str.rsplit('/', 1, expand=True)
    new_output = pd.DataFrame()
    new_output = new_columns
    output['titleId'] = new_output[1]
    
    final_df = output.merge(filtered_df[['tconst','titleType','genres', 'runtimeMinutes']], how='left',
                     left_on=['titleId'], right_on=['tconst'])
    final_df.to_csv(file_path + os.sep + 'output_df.csv')    

print ("Download complete...")