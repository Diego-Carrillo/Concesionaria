from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine

# Función para crear el dashboard
def create_dashboard():
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    # Conexión a la base de datos y carga de datos
    engine = create_engine('mysql+pymysql://root:Airsoud99.@localhost:3306/concesionaria')
    df = pd.read_sql_query("SELECT * FROM concesionaria", engine)

    # Calcular estadísticas descriptivas
    media_precio = df['Precio'].mean()
    mediana_precio = df['Precio'].median()
    moda_precio = df['Precio'].mode()[0]
    desviacion_estandar_precio = df['Precio'].std()
    rango_precio = df['Precio'].max() - df['Precio'].min()

    # Dropdown para seleccionar la marca
    marcas = df['Marca'].unique()
    dropdown_marcas = dcc.Dropdown(
        id='marca-dropdown',
        options=[{'label': marca, 'value': marca} for marca in marcas],
        value=marcas[0],
        clearable=False,
        style={'color': 'black'}
    )

    # Estilo para el fondo negro y texto claro
    style_black_background = {
        'backgroundColor': 'black',
        'color': 'white',
        'padding': '10px'
    }

    # Layout de la aplicación Dash
    app.layout = dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Dashboard de Concesionaria", style=style_black_background), width=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.Label("Selecciona una Marca:", style=style_black_background),
                dropdown_marcas
            ], width=4),
            dbc.Col([
                html.Div([
                    html.H3("Estadísticas de Precios", style=style_black_background),
                    html.P(f"Media: {media_precio:.2f}", style=style_black_background),
                    html.P(f"Mediana: {mediana_precio:.2f}", style=style_black_background),
                    html.P(f"Moda: {moda_precio:.2f}", style=style_black_background),
                    html.P(f"Desviación Estándar: {desviacion_estandar_precio:.2f}", style=style_black_background),
                    html.P(f"Rango: {rango_precio:.2f}", style=style_black_background)
                ])
            ], width=8)
        ], style=style_black_background),
        dbc.Row([
            dbc.Col(dcc.Graph(id='graph-precio'), width=6),
            dbc.Col(dcc.Graph(id='graph-calificacion'), width=6)
        ], style=style_black_background)
    ], fluid=True, style=style_black_background)

    # Callback para actualizar el gráfico de precio basado en la selección de la marca
    @app.callback(
        Output('graph-precio', 'figure'),
        Input('marca-dropdown', 'value')
    )
    def update_graph(selected_marca):
        filtered_df = df[df['Marca'] == selected_marca]
        fig = px.bar(filtered_df, x='Nombre', y='Precio', title=f'Precios de los Vehículos de {selected_marca}')
        fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='white')
        return fig

    return app

# Ejecutar la aplicación
if __name__ == '__main__':
    app = create_dashboard()
    app.run_server(debug=True)