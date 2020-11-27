"""
Solution to exercise #1 on Week 11
"""
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import os
from app import app
from app import server

# pandas dataframe to html table
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




file_path = os.getcwd()
df = pd.read_csv(file_path+os.sep+'output_df.csv', index_col=0, parse_dates=True)


app.layout = html.Div([
    html.H1('DJ Movie Dashboard!', style={'textAlign': 'center'}),
    generate_table(df)
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
    





