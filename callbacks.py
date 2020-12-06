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
import logging

logger = logging.getLogger(__name__)
# Create handlers
c_handler = logging.StreamHandler('sys.stdout')
f_handler = logging.FileHandler('app.log')
c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

def clean_integer(x):
    """ If the value is a string, then remove currency symbol and delimiters
    otherwise, the value is numeric and can be converted
    """
    if isinstance(x, str):
        return(x.replace(',', ''))
    return(x)

file_path = os.getcwd()
df = pd.read_csv(file_path+os.sep+'output_df.csv', index_col=0, parse_dates=True)
df['runtimeMinutes'] = df['runtimeMinutes'].replace('\\N','')
df['IMDB_votes'] = df['IMDB_votes'].apply(clean_integer).astype(float)
df['MC_users_count'] = df['MC_users_count'].apply(clean_integer).astype(float)
df['MC_critics_count'] = df['MC_critics_count'].apply(clean_integer).astype(float)
df['RT_users_count'] = df['RT_users_count'].apply(clean_integer).astype(float)
df['RT_critics_count'] = df['RT_critics_count'].apply(clean_integer).astype(float)

def generate_data_table (dataframe, id_name):
    return dash_table.DataTable(
    id=id_name,
    columns=[{"name": i, "id": i} for i in dataframe.columns],
    data=[],
    style_cell={'textAlign': 'left', 'fontSize': '14px',},
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
        'fontSize': '26px',
    },
    style_table={'overflowX': 'scroll'}, 
    sort_action="native",
    sort_mode="single",
    )

# pandas dataframe to html table
def generate_table(dataframe, max_rows=100):
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
    logger.info(years)
    logger.info(genres)
    logger.info(ratings)
    if (ratings == "IMDB"):
        filtered_df = df[["name", "year", "IMDB_rating", "IMDB_votes", "runtimeMinutes", "genres", "titleId"]]  
        filtered_df = filtered_df.rename(columns={'IMDB_rating': 'Ratings', 'IMDB_votes': 'Votes'})    
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        filtered_df['user_ratings'] = filtered_df['Ratings'].apply(clean_integer).astype(float)
        filtered_df = filtered_df[~pd.isnull(filtered_df.user_ratings)]
        filtered_df = filtered_df.sort_values('user_ratings', ascending = False).head(20)
        return generate_data_table(filtered_df, 'top_20_table')
    elif (ratings == "RT"):
        filtered_df = df[["name", "year", "RT_users_rating", "RT_users_count", "RT_critics_rating", "RT_critics_count", "runtimeMinutes", "genres", "titleId"]]   
        filtered_df = filtered_df.rename(columns={'RT_users_rating': 'User Ratings', 'RT_users_count': 'User Votes', 'RT_critics_rating': 'Critics Ratings', 'RT_critics_count': 'Critics Votes'})     
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        filtered_df['user_ratings'] = filtered_df['User Ratings'].apply(clean_integer).astype(float)
        filtered_df = filtered_df[~pd.isnull(filtered_df['user_ratings'])]
        filtered_df = filtered_df.sort_values('user_ratings', ascending = False).head(20)
        return generate_data_table(filtered_df, 'top_20_table')
    elif (ratings == "MC"):
        filtered_df = df[["name", "year", "MC_users_rating", "MC_users_count", "MC_critics_rating", "MC_critics_count", "runtimeMinutes", "genres", "titleId"]]      
        filtered_df = filtered_df.rename(columns={'MC_users_rating': 'User Ratings', 'MC_users_count': 'User Votes', 'MC_critics_rating': 'Critics Ratings', 'MC_critics_count': 'Critics Votes'})     
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        filtered_df = filtered_df[~filtered_df['User Ratings'].isin(['tbd'])]
        filtered_df['user_ratings'] = filtered_df['User Ratings'].apply(clean_integer).astype(float)
        filtered_df = filtered_df[~pd.isnull(filtered_df['user_ratings'])]
        filtered_df = filtered_df.sort_values('user_ratings', ascending = False).head(20)
        return generate_data_table(filtered_df, 'top_20_table') 
    
def get_results_data_table(df, years, genres, ratings):
    if (ratings == "IMDB"):
        filtered_df = df[["name", "year", "IMDB_rating", "IMDB_votes", "runtimeMinutes", "genres", "titleId"]]     
        filtered_df = filtered_df.rename(columns={'IMDB_rating': 'Ratings', 'IMDB_votes': 'Votes'})    
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        return generate_data_table(filtered_df, 'results_table')
    elif (ratings == "RT"):
        filtered_df = df[["name", "year", "RT_users_rating", "RT_users_count", "RT_critics_rating", "RT_critics_count", "runtimeMinutes", "genres", "titleId"]]       
        filtered_df = filtered_df.rename(columns={'RT_users_rating': 'User Ratings', 'RT_users_count': 'User Votes', 'RT_critics_rating': 'Critics Ratings', 'RT_critics_count': 'Critics Votes'})     
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        return generate_data_table(filtered_df, 'results_table')
    elif (ratings == "MC"):
        filtered_df = df[["name", "year", "MC_users_rating", "MC_users_count", "MC_critics_rating", "MC_critics_count",  "runtimeMinutes", "genres", "titleId"]]   
        filtered_df = filtered_df.rename(columns={'MC_users_rating': 'User Ratings', 'MC_users_count': 'User Votes', 'MC_critics_rating': 'Critics Ratings', 'MC_critics_count': 'Critics Votes'})     
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        return generate_data_table(filtered_df, 'results_table')        
    
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
        return html.Div([dcc.Graph(id='figure-output', figure={}, style={'display':'none'}, config={'responsive': True})])
    elif tab == "plot-tab": 
        return html.Div([dcc.Graph(id='figure-output',figure={}, style={'display':'none'}, config={'responsive': True})])
    elif tab == "results-tab":  
        return get_results_data_table(df, years, genres, ratings)

@app.callback(
    [
    Output(component_id='figure-output', component_property='figure'),
    Output(component_id='figure-output', component_property='style')],
    [Input(component_id='all-tabs-inline', component_property='value'),
     Input(component_id='year-slider', component_property='value'),
     Input(component_id='genres', component_property='value'),
     Input(component_id='ratings', component_property='value')]
)
def update_figure(tab, years, genres, ratings):
    if tab == "plotratings-tab":
        fig = get_top_20_plot_based_on_user_ratings(df, years, genres, ratings)
        style = {'display':'block', 'width': '90vw', 'height': '70vh'}
        return fig, style
    elif tab == "plot-tab":
        fig = get_top_20_plot_based_on_user_count(df, years, genres, ratings)
        style = {'display':'block', 'width': '90vw', 'height': '70vh'}
        return fig, style
    elif tab == "about-tab":
        fig = {}
        style = {'display':'none'}
        return fig, style
    elif tab == "top20-tab": 
        fig = {}
        style = {'display':'none'}
        return fig, style
    elif tab == "results-tab": 
        fig = {}
        style = {'display':'none'}
        return fig, style
    
def   get_top_20_plot_based_on_user_count(df, years, genres, ratings):
    if (ratings == "IMDB"):
        filtered_df = df[["name", "year", "IMDB_rating", "IMDB_votes", "genres"]]   
        filtered_df = filtered_df.rename(columns={'IMDB_rating': 'Ratings', 'IMDB_votes': 'Votes'})    
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        filtered_df['user_count'] = filtered_df['Votes']
        filtered_df = filtered_df[~pd.isnull(filtered_df.user_count)]
        filtered_df = filtered_df.sort_values('user_count', ascending = False).head(20)
        filtered_df = filtered_df.sort_values('user_count', ascending = True)
  
        fig = px.bar(filtered_df, x='user_count', y='name', orientation='h', color="user_count", color_continuous_scale =px.colors.sequential.Blugrn,)
        fig.update_layout(title="Top 20 movies ranked by user count",
                          title_x=0.5,
                      yaxis_title="Movies",
                      xaxis_title="User count",
                      font=dict(
                          family="Courier New, monospace",
                          size=18,
                          color="RebeccaPurple"),
                          bargap=0.25, # gap between bars of adjacent location coordinates.
                      )
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')           
        
        return fig 
    elif (ratings == "RT"):
        filtered_df = df[["name", "year", "RT_users_rating", "RT_users_count", "genres"]]   
        filtered_df = filtered_df.rename(columns={'RT_users_rating': 'User Ratings', 'RT_users_count': 'User Votes'})     
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        filtered_df['user_count'] = filtered_df['User Votes']
        filtered_df = filtered_df[~pd.isnull(filtered_df.user_count)]
        filtered_df = filtered_df.sort_values('user_count', ascending = False).head(20)
        filtered_df = filtered_df.sort_values('user_count', ascending = True)
    
        fig = px.bar(filtered_df, x='user_count', y='name', orientation='h', color="user_count", color_continuous_scale =px.colors.sequential.Blugrn,)
        fig.update_layout(title="Top 20 movies ranked by user count",
                          title_x=0.5,
                      yaxis_title="Movies",
                      xaxis_title="User count",
                      font=dict(
                          family="Courier New, monospace",
                          size=18,
                          color="RebeccaPurple"),
                          bargap=0.25, # gap between bars of adjacent location coordinates.
                      )   
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')           
        return fig
    elif (ratings == "MC"):
        filtered_df = df[["name", "year", "MC_users_rating", "MC_users_count", "genres"]]   
        filtered_df = filtered_df.rename(columns={'MC_users_rating': 'User Ratings', 'MC_users_count': 'User Votes'})     
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        filtered_df['user_count'] = filtered_df['User Votes']
        filtered_df = filtered_df[~pd.isnull(filtered_df.user_count)]
        filtered_df = filtered_df.sort_values('user_count', ascending = False).head(20)
        filtered_df = filtered_df.sort_values('user_count', ascending = True)
        fig = px.bar(filtered_df, x='user_count', y='name', orientation='h', color="user_count", color_continuous_scale =px.colors.sequential.Blugrn,)
        fig.update_layout(title="Top 20 movies ranked by user count",
                          title_x=0.5,
                          yaxis_title="Movies",
                          xaxis_title="User count",
                          font=dict(
                          family="Courier New, monospace",
                          size=18,
                          color="RebeccaPurple"),
                          bargap=0.25, # gap between bars of adjacent location coordinates.  
                      )
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')   
        return fig
    

def get_top_20_plot_based_on_user_ratings(df, years, genres, ratings):
    if (ratings == "IMDB"):
        filtered_df = df[["name", "year", "IMDB_rating", "IMDB_votes", "genres"]]   
        filtered_df = filtered_df.rename(columns={'IMDB_rating': 'Ratings', 'IMDB_votes': 'Votes'})    
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        filtered_df['user_ratings'] = filtered_df['Ratings'].apply(clean_integer).astype(float)
        filtered_df = filtered_df[~pd.isnull(filtered_df.user_ratings)]
        filtered_df = filtered_df.sort_values('user_ratings', ascending = False).head(20)
        filtered_df = filtered_df.sort_values('user_ratings', ascending = True)
        fig = px.bar(filtered_df, x='user_ratings', y='name', orientation='h', color="user_ratings", color_continuous_scale =px.colors.sequential.Blugrn,)
        fig.update_layout(title="Top 20 movies ranked by user ratings",
                          title_x=0.5,
                          yaxis_title="Movies",
                          xaxis_title="User ratings",
                          font=dict(
                          family="Courier New, monospace",
                          size=18,
                          color="RebeccaPurple"),
                          bargap=0.25, # gap between bars of adjacent location coordinates.   
                      )        
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')           
        return fig
    elif (ratings == "RT"):
        filtered_df = df[["name", "year", "RT_users_rating", "RT_users_count", "genres"]]   
        filtered_df = filtered_df.rename(columns={'RT_users_rating': 'User Ratings', 'RT_users_count': 'User Votes'})     
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        filtered_df['user_ratings'] = filtered_df['User Ratings'].apply(clean_integer).astype(float)
        filtered_df = filtered_df[~pd.isnull(filtered_df.user_ratings)]
        filtered_df = filtered_df.sort_values('user_ratings', ascending = False).head(20)
        filtered_df = filtered_df.sort_values('user_ratings', ascending = True)
        fig = px.bar(filtered_df, x='user_ratings', y='name', orientation='h', color="user_ratings", color_continuous_scale =px.colors.sequential.Blugrn,)
        
        fig.update_layout(title="Top 20 movies ranked by user ratings",
                          title_x=0.5,
                          yaxis_title="Movies",
                          xaxis_title="User ratings",          
                          font=dict(
                              family="Courier New, monospace",
                              size=18,
                              color="RebeccaPurple"),
                          bargap=0.25, # gap between bars of adjacent location coordinates.
                      )        
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')           
        return fig
    elif (ratings == "MC"):
        filtered_df = df[["name", "year", "MC_users_rating", "MC_users_count", "genres"]]   
        filtered_df = filtered_df.rename(columns={'MC_users_rating': 'User Ratings', 'MC_users_count': 'User Votes'})     
        filtered_df = filtered_df[filtered_df.year.isin(years)]
        filtered_df = filtered_df[filtered_df.genres.str.contains('|'.join(genres))]
        filtered_df = filtered_df[~filtered_df['User Ratings'].isin(['tbd'])]
        filtered_df['user_ratings'] = filtered_df['User Ratings'].apply(clean_integer).astype(float)
        
        filtered_df = filtered_df[~pd.isnull(filtered_df.user_ratings)]
        filtered_df = filtered_df.sort_values('user_ratings', ascending = False).head(20)
        filtered_df = filtered_df.sort_values('user_ratings', ascending = True)
        fig = px.bar(filtered_df, x='user_ratings', y='name', orientation='h', color="user_ratings", color_continuous_scale =px.colors.sequential.Blugrn,)
        fig.update_layout(title="Top 20 movies ranked by user ratings",
                          title_x=0.5,
                      yaxis_title="Movies",
                      xaxis_title="User ratings",
                      font=dict(
                          family="Courier New, monospace",
                          size=18,
                          color="RebeccaPurple"),
                          bargap=0.25, # gap between bars of adjacent location coordinates.                     
                      )         
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')        
        return fig    

