import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re

service = Service("C:/Program Files/Google/Chrome/Application/chrome.exe")  # Asegúrate de que la ruta es correcta
# Configurando Selenium WebDriver
opc = Options()
navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opc)


# Descargando datos de las 250 mejores películas de IMDb
navegador.get('http://www.imdb.com/chart/top')
time.sleep(5)  # Espera para que la página se cargue completamente

# Obteniendo el HTML de la página
html = navegador.page_source
soup = BeautifulSoup(html, "html.parser")

# Extrayendo información de las películas
peliculas = soup.select('td.titleColumn')
elenco = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
calificaciones = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]

# Lista para almacenar información de las películas
lista_peliculas = []

# Iterando sobre las películas para extraer cada detalle
for indice in range(0, len(peliculas)):
    cadena_pelicula = peliculas[indice].get_text()
    pelicula = (' '.join(cadena_pelicula.split()).replace('.', ''))
    titulo_pelicula = pelicula[len(str(indice)) + 1:-7]
    anio = re.search('\((.*?)\)', cadena_pelicula).group(1)
    posicion = pelicula[:len(str(indice)) - (len(pelicula))]
    datos = {
        "posicion": posicion,
        "titulo_pelicula": titulo_pelicula,
        "calificacion": calificaciones[indice],
        "anio": anio,
        "elenco": elenco[indice],
    }
    lista_peliculas.append(datos)

# Cerrando el navegador
navegador.quit()

# Creando un DataFrame y guardando en CSV
df = pd.DataFrame(lista_peliculas)
df.to_csv('imdb_top_250_peliculas.csv', index=False)
