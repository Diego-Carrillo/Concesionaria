from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# Configuración de la conexión a la base de datos
engine = create_engine('mysql+pymysql://root:Airsoud99.@localhost:3306/concesionaria')

# Crea la aplicación Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Cargar datos de la base de datos
df = pd.read_sql_query("SELECT * FROM concesionaria", engine)

# Dropdown para seleccionar la marca
marcas = df['Concesionaria'].unique()
dropdown_marcas = dcc.Dropdown(
    id='Concesionaria-dropdown',
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
    dbc.Row(dbc.Col(html.H1("Dashboard de Concesionaria", style=style_black_background))),
    dbc.Row([
        dbc.Col([
            html.Label("Selecciona una Concesionaria:", style=style_black_background),
            dropdown_marcas
        ], width=4),
        dbc.Col([
            html.Div([
                html.H3("Estadísticas de Precios", style=style_black_background),
                html.P(id='stat-media', children="Media: ", style=style_black_background),
                html.P(id='stat-mediana', children="Mediana: ", style=style_black_background),
                html.P(id='stat-moda', children="Moda: ", style=style_black_background),
                html.P(id='stat-desviacion', children="Desviación Estándar: ", style=style_black_background),
                html.P(id='stat-rango', children="Rango: ", style=style_black_background)
            ], style=style_black_background)
        ], width=8)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='graph-precio'), width=6),
        dbc.Col(dcc.Graph(id='scatter-plot'), width=6),
    ], style=style_black_background),
    dbc.Row([
        dbc.Col(dcc.Graph(id='box-plot'), width=6),
        # Añade más gráficos aquí según sea necesario
    ], style=style_black_background)
], fluid=True, style=style_black_background)

# Callback para actualizar las estadísticas y los gráficos basados en la selección de la concesionaria
@app.callback(
    [
        Output('stat-media', 'children'),
        Output('stat-mediana', 'children'),
        Output('stat-moda', 'children'),
        Output('stat-desviacion', 'children'),
        Output('stat-rango', 'children'),
        Output('graph-precio', 'figure'),
        Output('scatter-plot', 'figure'),
        Output('box-plot', 'figure')
    ],
    [Input('Concesionaria-dropdown', 'value')]
)
def update_output(selected_concesionaria):
    filtered_df = df[df['Concesionaria'] == selected_concesionaria]
    media_precio = filtered_df['Precio'].mean()
    mediana_precio = filtered_df['Precio'].median()
    moda_precio = filtered_df['Precio'].mode()[0]
    desviacion_estandar_precio = filtered_df['Precio'].std()
    rango_precio = filtered_df['Precio'].max() - filtered_df['Precio'].min()
    fig_precio = px.bar(filtered_df, x='Nombre', y='Precio', title=f'Precios de los Vehículos de {selected_concesionaria}')
    fig_scatter = px.scatter(filtered_df, x='Millaje', y='Precio', title=f'Relación entre Millaje y Precio en {selected_concesionaria}')
    fig_box = px.box(filtered_df, y='Precio', title=f'Distribución de Precios en {selected_concesionaria}')
    return (
        f"Media: {media_precio:.2f}",
        f"Mediana: {mediana_precio:.2f}",
        f"Moda: {moda_precio}",
        f"Desviación Estándar: {desviacion_estandar_precio:.2f}",
        f"Rango: {rango_precio:.2f}",
        fig_precio.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='white'),
        fig_scatter.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='white'),
        fig_box.update_layout(plot_bgcolor='black', paper_bgcolor='black', font_color='white')
    )

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)