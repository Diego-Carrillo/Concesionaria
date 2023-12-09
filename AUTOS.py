from bs4 import BeautifulSoup
import requests
import pandas as pd
from sqlalchemy import create_engine

# Datos de la BD
usuario = 'root'
contraseña = 'Airsoud99.'
host = 'localhost'  # o la dirección del servidor
puerto = '3306'
db = 'concesionaria'

# Creando la conexión
engine = create_engine(f'mysql+pymysql://{usuario}:{contraseña}@{host}:{puerto}/{db}')

# Lista para almacenar los datos
name = []
mileage = []
dealer_name = []
rating = []
review_count = []
price = []

for i in range(1, 11):
    website = 'https://www.cars.com/shopping/results/?page=' + str(i) + '&page_size=20&dealer_id=&list_price_max=&list_price_min=&makes[]=mercedes_benz&maximum_distance=20&mileage_max=&sort=best_match_desc&stock_type=cpo&year_max=&year_min=&zip='
    response = requests.get(website)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all('div', {'class': 'vehicle-card'})

    for result in results:
        # Extracción y almacenamiento de datos
        name.append(result.find('h2').get_text() if result.find('h2') else 'n/a')
        mileage.append(result.find('div', {'class': 'mileage'}).get_text() if result.find('div', {'class': 'mileage'}) else 'n/a')
        dealer_name.append(result.find('div', {'class': 'dealer-name'}).get_text().strip() if result.find('div', {'class': 'dealer-name'}) else 'n/a')
        rating.append(result.find('span', {'class': 'sds-rating__count'}).get_text() if result.find('span', {'class': 'sds-rating__count'}) else 'n/a')
        review_count.append(result.find('span', {'class': 'sds-rating__link'}).get_text() if result.find('span', {'class': 'sds-rating__link'}) else 'n/a')
        price.append(result.find('span', {'class': 'primary-price'}).get_text() if result.find('span', {'class': 'primary-price'}) else 'n/a')

# Creación del DataFrame
Concesionaria = pd.DataFrame({'Nombre': name, 'Millaje': mileage, "Concesionaria": dealer_name, "Calificacion": rating, "Numero de Reviews": review_count, "Precio": price})

# Limpieza y conversión de tipos de datos
Concesionaria['Millaje'] = Concesionaria['Millaje'].str.replace(r'\D', '', regex=True).astype(float)
Concesionaria['Calificacion'] = Concesionaria['Calificacion'].astype(float)
Concesionaria['Numero de Reviews'] = Concesionaria['Numero de Reviews'].str.replace(r'\D', '', regex=True).astype(int)
Concesionaria['Precio'] = Concesionaria['Precio'].str.replace(r'\D', '', regex=True).astype(float)

# Insertar datos en MySQL
Concesionaria.to_sql('concesionaria', con=engine, index=False, if_exists='append')
