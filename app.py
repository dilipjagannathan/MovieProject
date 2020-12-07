# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 14:50:53 2020

@author: dilip
"""

import dash

import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True