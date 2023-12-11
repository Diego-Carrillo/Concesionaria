import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, dash_table, callback, Input, Output
import mysql.connector

# Conexión a la base de datos MySQL
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    database="Concesionaria"
)

# Consulta SQL para obtener los datos
sql_query = "SELECT * FROM posiciones"
data = pd.read_sql(sql_query, con=db_connection)

# Cerrar la conexión a la base de datos
db_connection.close()


def dashboard(data):
    # Obtener lista de equipos y temporadas
    equipos = data["año"].unique()
    temporadas = data["ubicacion"].unique()

    # Diseño utilizando componentes de Dash Bootstrap
    pagina = dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("Dashboard Concesionaria"), width=12)
        ]),
        dbc.Row([
            dbc.Col(html.P(
                "Objetivo: Mostrar los autos mas nuevos"),
                    width=12)
        ]),
        dbc.Row([
            dbc.Col(html.Hr(), width=12)
        ]),
        dbc.Row([



if __name__ == "__main__":
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = dashboard(data)
    app.run_server(debug=True