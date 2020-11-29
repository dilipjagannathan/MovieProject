# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 18:39:52 2020

@author: dilip
"""
import pandas as pd
import os

file_path = os.getcwd()
df = pd.read_csv(file_path+os.sep+'output_df.csv', index_col=0, parse_dates=True)