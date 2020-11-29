# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 18:39:52 2020

@author: dilip
"""
import pandas as pd
import os
from dash.dependencies import Input, Output
import dash_html_components as html
import dash
from app import app
import dash_core_components as dcc

file_path = os.getcwd()
df = pd.read_csv(file_path+os.sep+'output_df.csv', index_col=0, parse_dates=True)

#pandas dataframe to html table
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

def get_about_info():
    return dcc.Markdown('''
#### Overview

This dashboard uses the information retrieved from different movie portals like IMDB, Rotten Tomatoes, Metacritic. The information was retrieved from release year 2011 for movie category.

#### Background

The data retrieval process for the dashboard is as follows:

* Step 1: Retrieve information from [IMDB Dataset](https://datasets.imdbws.com/title.basics.tsv.gz)
* Step 2: Select only movies greater than start year 2010
* Step 3: For each movie, retrieve the ratings information from the following sites if available:
    * [IMDB](https://www.imdb.com/find?q=%s&s=tt&ttype=ft&ref_=fn_ftl)
    * [Rotten Tomatoes](https://www.rottentomatoes.com/napi/search/?query=%s)
    * [Metacritic](http://www.metacritic.com/search/movie/%s/results)
* Step 4: All the results are combined to form one data frame and saved as commma separated file
* Step 5: This data file is used as input for this dashboard

#### Dashboard features
Based on the selection and input provided using release year, genres and ratings:
    
* Top 20 movies tab displays the top 20 movies 
* User score vs critic score tab displays the scatter plot with trend line
* Plot of 20 movies tab displays the bar plot based on number of user votes
* Results tab displays all results

''',
            style={"textAlign": "left", 'color':'white',},)
  
# Update the table
@app.callback(
    Output(component_id='movie-output', component_property='children'),
    [Input(component_id='all-tabs-inline', component_property='value'),
     Input(component_id='year-slider', component_property='value'),
     Input(component_id='genres', component_property='value'),
     Input(component_id='ratings', component_property='value')]
)
def update_tab(tab, years, genres, ratings):
    if tab == "about-tab":
        return get_about_info()
    elif tab == "top20-tab":  
        return generate_table(df)
    elif tab == "uservscritic-tab":
        return generate_table(df)
    elif tab == "plot-tab": 
        return generate_table(df)
    elif tab == "results-tab":  
        return generate_table(df)
