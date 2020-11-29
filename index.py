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

# pandas dataframe to html table
# def generate_table(dataframe, max_rows=10):
#     return html.Table([
#         html.Thead(
#             html.Tr([html.Th(col) for col in dataframe.columns])
#         ),
#         html.Tbody([
#             html.Tr([
#                 html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#             ]) for i in range(min(len(dataframe), max_rows))
#         ])
#     ])

app.layout = layout

# app.layout = html.Div([
#     html.H1('DJ Movie Dashboard!', style={'textAlign': 'center'}),
#     generate_table(df)
#     ])

if __name__ == '__main__':
    app.run_server(debug=True)
    





