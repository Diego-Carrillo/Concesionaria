import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

Direccion= 'http://www.imdb.com/chart/top'
respuesta = requests.get(Direccion)
soup = BeautifulSoup(respuesta.text, "html.parser")