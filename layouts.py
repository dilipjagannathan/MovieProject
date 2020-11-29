# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 18:39:30 2020

@author: dilip
"""

import dash_core_components as dcc
import dash_html_components as html

tab_style = {
    "borderBottom": "1px solid #d6d6d6",
    "padding": "2px",
    "fontWeight": "bold",
    "vertical-align": "middle",
}

tab_selected_style = {
    "borderTop": "1px solid #d6d6d6",
    "borderBottom": "1px solid #d6d6d6",
    "backgroundColor": "white",
    "color": "blue",
    "padding": "10px",
    "font-size": 20,
}

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
        html.Div(id="movie-input"),
        dcc.Tabs(
            id="all-tabs-inline",
            className="all-tabs-inline",
            value="tab-1",
            children=[
                dcc.Tab(
                    label="About",
                    value="tab-1",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="Top 20 movies",
                    value="tab-2",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="User score vs Critic score",
                    value="tab-3",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="Plot of 20 movies",
                    value="tab-4",
                    style=tab_style,
                    selected_style=tab_selected_style,
                ),
                dcc.Tab(
                    label="Results",
                    value="tab-5",
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
            style={"textAlign": "center", "background": "yellow"},
        ),
    ],
    style={"background": "#000080"},
)
