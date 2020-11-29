# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 18:39:30 2020

@author: dilip
"""

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import os
from datetime import date
import json

file_path = os.getcwd()
df = pd.read_csv(file_path+os.sep+'output_df.csv', index_col=0, parse_dates=True)

years = df.year.unique()
current_year = date.today().year
years = [ year for year in years if (year > 2010)  & (year <= current_year) ]
years = sorted (years)
genres_list=sorted(df.genres.str.split(',').explode().unique())
print (genres_list)

tab_style = {
    "borderBottom": "1px solid #d6d6d6",
    "padding": "2px",
    "fontWeight": "bold",
    "vertical-align": "middle",
}

tab_selected_style = {
    "borderTop": "1px solid #d6d6d6",
    "borderBottom": "1px solid #d6d6d6",
    "backgroundColor": "black",
    "color": "white",
    "padding": "10px",
    "font-size": 20,
}

def get_marks(years):
    year_marks = {}
    for year in years:
        year_dict = {}
        year_style = {}
        year_dict['label'] = str(year)
        year_style['color'] = 'white'
        year_dict['style'] = year_style

        year_marks[int(year)] = {}
        year_marks[int(year)] = year_dict

    return year_marks

def get_genres(genres):
    genre_list = []
    for genre in genres:
        genre_dict = {}
        genre_dict['label'] = genre
        genre_dict['value'] = genre
        genre_list.append(genre_dict)
    print (genre_list)
    return genre_list
        
input = html.Div([
      		html.H6('Release Year:',
                              style={
                                  "display": "inline-block",
                                  "margin": "0px",
                                  "color": "white",
                                  "line-height": "0.1",
                              },),

      		dcc.RangeSlider(
              id='year-slider',
              min=years[0],
              max=years[-1],
              step=1,
              value=[years[0], years[-1]],  
              marks = get_marks(years),
      		),
            html.H6('Genres:',
                          style={
                              "display": "inline-block",
                              "margin": "0px",
                              "color": "white",
                              "line-height": "0.1",
                          },),
            dcc.Dropdown(
                id='genres',
                options=get_genres(genres_list),
                value=genres_list,
                multi=True,
                ),
            html.H6('Ratings:',
                          style={
                              "display": "inline-block",
                              "margin": "0px",
                              "color": "white",
                              "line-height": "0.1",
                          },),     
        dcc.RadioItems(
            id='ratings',
            options=[
                {'label': 'IMDB', 'value': 'IMDB'},
                {'label': 'Rotten Tomatoes', 'value': 'RT'},
                {'label': 'Metacritic', 'value': 'MC'},
                {'label': 'Overall', 'value': 'Overall'}
            ],
            value='IMDB',
            style={
                "display": "inline-block",
                "margin": "0px",
                "color": "white",
                "line-height": "0.1",
            },
        labelStyle={'display': 'inline-block'})
                      
])

footer = html.Div(
    className="footer",
    children=[
        html.Div(
            [
                html.Div(
                    [
                        html.H3(
                            "Created by ",
                            style={
                                "display": "inline-block",
                                "margin": "0px",
                                "color": "white",
                                "line-height": "0.1",
                            },
                        ),
                        html.A(
                            html.Img(
                                src="assets/images/dilip.png",
                                alt="author",
                                style={
                                    "height": "10%",
                                    "width": "3.75%",
                                    "display": "inline-block",
                                    "border-radius": "50%",
                                    "margin": "10px",
                                },
                            ),
                            href="https://www.linkedin.com/in/dilip-j-1506bb3/",
                            style={"vertical-align": "middle"},
                        ),
                    ],
                ),
                html.H3(
                    "Source code available on ",
                    style={
                        "display": "inline-block",
                        "margin": "0px",
                        "color": "white",
                        "line-height": "0.1",
                    },
                ),
                html.A(
                    html.Img(
                        src="assets/images/github.png",
                        alt="github",
                        className="git-image",
                        style={
                            "height": "10%",
                            "width": "7%",
                            "display": "inline-block",
                        },
                    ),
                    href="https://github.com/dilipjagannathan/MovieProject",
                    className="git-code",
                    style={"vertical-align": "middle"},
                ),
            ],
        ),
    ],
    style={"textAlign": "center"},
)

layout = html.Div(
    [
        html.H1(
            "Movie Dashboard",
            style={
                "textAlign": "center",
                "color": "white",
                #"background": "yellow"
            },
        ),
        input,
        dcc.Tabs(
            id="all-tabs-inline",
            className="all-tabs-inline",
            value="about-tab",
            children=[
                dcc.Tab(
                    label="About",
                    value="about-tab",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="Top 20 movies",
                    value="top20-tab",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="User score vs Critic score",
                    value="uservscritic-tab",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="Plot of 20 movies",
                    value="plot-tab",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="Results",
                    value="results-tab",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),                
            ],
            colors={
                "border": "yellow",
                "primary": "red",
                "background": "orange",
            },
        ),
        html.Div(id="movie-output"),  # Tab output
        html.Div(footer),
        html.Div(
            children=[
                dcc.Markdown('''
#### Primary Data Sources: 
[IMDB](https://www.imdb.com/) 
[Rotten Tomato](https://www.rottentomatoes.com) 
[Metacritic](http://www.metacritic.com)
'''
                            
                )
            ],
            style={"textAlign": "center", "background": "orange"},
        ),
    ],
    style={"background": "black"},
)
