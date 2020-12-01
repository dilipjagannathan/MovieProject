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
import dash_table
from app import app
import dash_core_components as dcc
import plotly.express as px

file_path = os.getcwd()
df = pd.read_csv(file_path+os.sep+'output_df.csv', index_col=0, parse_dates=True)

def generate_data_table (dataframe):
    return dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in dataframe.columns],
    data=dataframe.to_dict('records'),
    style_cell={'textAlign': 'left', 'font-size': '14px',},
    style_data_conditional=[
        {
            'if': {'row_index':'odd'},
            'backgroundColor': 'lightgrey',
            'color': 'black'
        },
        {
            "if": {"state": "selected"},
            "backgroundColor": "inherit !important",
            "border": "inherit !important",
        } 
    ],
    style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white',
        'fontWeight': 'bold',
        'font-size': '26px',
    },
    style_table={'overflowX': 'scroll'}, 
    sort_action="native",
    sort_mode="multi",
    )

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
def clean_integer(x):
    """ If the value is a string, then remove currency symbol and delimiters
    otherwise, the value is numeric and can be converted
    """
    if isinstance(x, str):
        return(x.replace(',', ''))
    return(x)

def get_about_info():
    
    return dcc.Markdown('''
#### Overview

This dashboard uses the information retrieved from different movie portals like IMDB, Rotten Tomatoes, Metacritic. The information was retrieved from release year 2011 for movie category.

#### Background

The data retrieval process for the dashboard (download_titles.py) is as follows:

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
* Plot of 20 movies by user ratings tab displays the bar plot based on user ratings
* Plot of 20 movies by user count tab displays the bar plot based on number of user votes
* Results tab displays all results

''',
            style={"textAlign": "left", 'color':'white',},)

def get_top20_data_table(df, years, genres, ratings):
    if (ratings == "IMDB"):
        filtered_df = df[["name", "year", "IMDB_rating", "IMDB_votes", "runtimeMinutes", "genres", "titleId"]]  
        filtered_df['runtimeMinutes'] = filtered_df['runtimeMinutes'].replace('\\N','')
        filtered_df = filtered_df.rename(columns={'IMDB_rating': 'Ratings', 'IMDB_votes': 'Votes'})    
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        filtered_df = filtered_df.sort_values('Ratings', ascending = False).head(20)
        return generate_data_table(filtered_df)
    elif (ratings == "RT"):
        filtered_df = df[["name", "year", "RT_users_rating", "RT_users_count", "RT_critics_rating", "RT_critics_count", "runtimeMinutes", "genres", "titleId"]]   
        filtered_df['runtimeMinutes'] = filtered_df['runtimeMinutes'].replace('\\N','')
        filtered_df = filtered_df.rename(columns={'RT_users_rating': 'User Ratings', 'RT_users_count': 'User Votes', 'RT_critics_rating': 'Critics Ratings', 'RT_critics_count': 'Critics Votes'})     
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        filtered_df = filtered_df.sort_values('User Ratings', ascending = False).head(20)
        return generate_data_table(filtered_df)
    elif (ratings == "MC"):
        filtered_df = df[["name", "year", "MC_users_rating", "MC_users_count", "MC_critics_rating", "MC_critics_count", "runtimeMinutes", "genres", "titleId"]]   
        filtered_df['runtimeMinutes'] = filtered_df['runtimeMinutes'].replace('\\N','')        
        filtered_df = filtered_df.rename(columns={'MC_users_rating': 'User Ratings', 'MC_users_count': 'User Votes', 'MC_critics_rating': 'Critics Ratings', 'MC_critics_count': 'Critics Votes'})     
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        filtered_df = filtered_df[~filtered_df['User Ratings'].isin(['tbd'])]
        filtered_df = filtered_df.sort_values('User Ratings', ascending = False).head(20)
        return generate_data_table(filtered_df)    
    
def get_results_data_table(df, years, genres, ratings):
    if (ratings == "IMDB"):
        filtered_df = df[["name", "year", "IMDB_rating", "IMDB_votes", "runtimeMinutes", "genres", "titleId"]]  
        filtered_df['runtimeMinutes'] = filtered_df['runtimeMinutes'].replace('\\N','')        
        filtered_df = filtered_df.rename(columns={'IMDB_rating': 'Ratings', 'IMDB_votes': 'Votes'})    
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        return generate_data_table(filtered_df)
    elif (ratings == "RT"):
        filtered_df = df[["name", "year", "RT_users_rating", "RT_users_count", "RT_critics_rating", "RT_critics_count", "runtimeMinutes", "genres", "titleId"]]   
        filtered_df['runtimeMinutes'] = filtered_df['runtimeMinutes'].replace('\\N','')        
        filtered_df = filtered_df.rename(columns={'RT_users_rating': 'User Ratings', 'RT_users_count': 'User Votes', 'RT_critics_rating': 'Critics Ratings', 'RT_critics_count': 'Critics Votes'})     
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        return generate_data_table(filtered_df)
    elif (ratings == "MC"):
        filtered_df = df[["name", "year", "MC_users_rating", "MC_users_count", "MC_critics_rating", "MC_critics_count",  "runtimeMinutes", "genres", "titleId"]]   
        filtered_df['runtimeMinutes'] = filtered_df['runtimeMinutes'].replace('\\N','')        
        filtered_df = filtered_df.rename(columns={'MC_users_rating': 'User Ratings', 'MC_users_count': 'User Votes', 'MC_critics_rating': 'Critics Ratings', 'MC_critics_count': 'Critics Votes'})     
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        return generate_data_table(filtered_df)        
    
# Update the table
@app.callback(
    Output(component_id='movie-output', component_property='children'),
    [Input(component_id='all-tabs-inline', component_property='value'),
     Input(component_id='year-slider', component_property='value'),
     Input(component_id='genres', component_property='value'),
     Input(component_id='ratings', component_property='value')]
)
def update_tab(tab, years, genres, ratings):
    years = range (years[0], years[1], 1)
    if tab == "about-tab":
        return get_about_info()
    elif tab == "top20-tab": 
        return get_top20_data_table(df, years, genres, ratings)
    elif tab == "plotratings-tab":
        return get_top_20_plot_based_on_user_ratings(df, years, genres, ratings)
    elif tab == "plot-tab": 
        return get_top_20_plot_based_on_user_count(df, years, genres, ratings)
    elif tab == "results-tab":  
        return get_results_data_table(df, years, genres, ratings)

def get_top_20_plot_based_on_user_count(df, years, genres, ratings):
    if (ratings == "IMDB"):
        filtered_df = df[["name", "year", "IMDB_rating", "IMDB_votes", "genres"]]   
        filtered_df = filtered_df.rename(columns={'IMDB_rating': 'Ratings', 'IMDB_votes': 'Votes'})    
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        filtered_df['user_count'] = filtered_df['Votes'].apply(clean_integer).astype(float)
        filtered_df = filtered_df[~pd.isnull(filtered_df.user_count)]
        filtered_df = filtered_df.sort_values('user_count', ascending = False).head(20)
        fig = px.bar(filtered_df, x='name', y='user_count')    
        return dcc.Graph(figure=fig,style={'width': '90vw', 'height': '70vh'}) 
        # fig = px.bar(x=filtered_df.name, y=filtered_df["user_count"])
      
        # return dcc.Graph(figure=fig)
    elif (ratings == "RT"):
        filtered_df = df[["name", "year", "RT_users_rating", "RT_users_count", "genres"]]   
        filtered_df = filtered_df.rename(columns={'RT_users_rating': 'User Ratings', 'RT_users_count': 'User Votes'})     
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        filtered_df['user_count'] = filtered_df['User Votes'].apply(clean_integer).astype(float)
        filtered_df = filtered_df[~pd.isnull(filtered_df.user_count)]
        filtered_df = filtered_df.sort_values('user_count', ascending = False).head(20)
        fig = px.bar(filtered_df, x='name', y='user_count')
        return dcc.Graph(figure=fig,style={'width': '90vw', 'height': '70vh'}) 
    elif (ratings == "MC"):
        filtered_df = df[["name", "year", "MC_users_rating", "MC_users_count", "genres"]]   
        filtered_df = filtered_df.rename(columns={'MC_users_rating': 'User Ratings', 'MC_users_count': 'User Votes'})     
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        filtered_df['user_count'] = filtered_df['User Votes'].apply(clean_integer).astype(float)
        filtered_df = filtered_df[~pd.isnull(filtered_df.user_count)]
        filtered_df = filtered_df.sort_values('user_count', ascending = False).head(20)
        fig = px.bar(filtered_df, x='name', y='user_count')
        return dcc.Graph(figure=fig,style={'width': '90vw', 'height': '70vh'}) 
    
def get_top_20_plot_based_on_user_ratings(df, years, genres, ratings):
    if (ratings == "IMDB"):
        filtered_df = df[["name", "year", "IMDB_rating", "IMDB_votes", "genres"]]   
        filtered_df = filtered_df.rename(columns={'IMDB_rating': 'Ratings', 'IMDB_votes': 'Votes'})    
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        filtered_df['user_ratings'] = filtered_df['Ratings'].apply(clean_integer).astype(float)
        filtered_df = filtered_df[~pd.isnull(filtered_df.user_ratings)]
        filtered_df = filtered_df.sort_values('user_ratings', ascending = False).head(20)
        fig = px.bar(filtered_df, x='name', y='user_ratings')    
        return dcc.Graph(figure=fig,style={'width': '90vw', 'height': '70vh'}) 
    elif (ratings == "RT"):
        filtered_df = df[["name", "year", "RT_users_rating", "RT_users_count", "genres"]]   
        filtered_df = filtered_df.rename(columns={'RT_users_rating': 'User Ratings', 'RT_users_count': 'User Votes'})     
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        filtered_df['user_ratings'] = filtered_df['User Ratings'].apply(clean_integer).astype(float)
        filtered_df = filtered_df[~pd.isnull(filtered_df.user_ratings)]
        filtered_df = filtered_df.sort_values('user_ratings', ascending = False).head(20)
        fig = px.bar(filtered_df, x='name', y='user_ratings')
        return dcc.Graph(figure=fig,style={'width': '90vw', 'height': '70vh'}) 
    elif (ratings == "MC"):
        filtered_df = df[["name", "year", "MC_users_rating", "MC_users_count", "genres"]]   
        filtered_df = filtered_df.rename(columns={'MC_users_rating': 'User Ratings', 'MC_users_count': 'User Votes'})     
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        filtered_df = filtered_df[~filtered_df['User Ratings'].isin(['tbd'])]
        filtered_df['user_ratings'] = filtered_df['User Ratings'].apply(clean_integer).astype(float)
        
        filtered_df = filtered_df[~pd.isnull(filtered_df.user_ratings)]
        filtered_df = filtered_df.sort_values('user_ratings', ascending = False).head(20)
        fig = px.bar(filtered_df, x='name', y='user_ratings')
        return dcc.Graph(figure=fig,style={'width': '90vw', 'height': '70vh'})     

