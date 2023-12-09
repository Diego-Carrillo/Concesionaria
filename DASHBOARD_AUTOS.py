from sqlalchemy import create_engine #Un ejemplo venia con esta libreria y se me hace mas simple que el conector
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, dash_table, Input, Output, callback


engine = create_engine('mysql+pymysql://root:Airsoud99.@host:3306/concesionaria')
df = pd.read_sql_query("SELECT * FROM concesionaria", engine)

