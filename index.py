"""
Solution to exercise #1 on Week 11
"""
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

from app import app
from app import server
import callbacks
from layouts import layout


app.layout = layout

if __name__ == '__main__':
    app.run_server(debug=True)
    





