from bs4 import BeautifulSoup
import requests
import pandas as pd
from sqlalchemy import create_engine, text

# Datos de la BD
usuario = 'root'
contraseña = 'Airsoud99.'
host = 'localhost'  # o la dirección del servidor
puerto = '3306'
db = 'concesionaria'

# Creando la conexión
engine = create_engine(f'mysql+pymysql://{usuario}:{contraseña}@{host}:{puerto}/{db}')


sitio = 'https://www.cars.com/shopping/results/?stock_type=cpo&makes%5B%'
respuesta = requests.get(sitio)
respuesta.status_code
soup = BeautifulSoup(respuesta.content, 'html.parser')
results = soup.find_all('div', {'class' : 'vehicle-card'})
len(results)

#Nombre
#Millaje
#Nombre marca
#Calificacion
#Contador calificacion
#Precio

name = []
mileage = []
dealer_name = []
rating = []
review_count = []
price = []
for i in range(1, 11):

    # website in variable
    website = 'https://www.cars.com/shopping/results/?page=' + str(
        i) + '&page_size=20&dealer_id=&list_price_max=&list_price_min=&makes[]=mercedes_benz&maximum_distance=20&mileage_max=&sort=best_match_desc&stock_type=cpo&year_max=&year_min=&zip='

    # request to website
    response = requests.get(website)

    # soup object
    soup = BeautifulSoup(response.content, 'html.parser')

    # results
    results = soup.find_all('div', {'class': 'vehicle-card'})

    # loop through results
    for result in results:

        # name
        try:
            name.append(result.find('h2').get_text())
        except:
            name.append('n/a')

        # mileage
        try:
            mileage.append(result.find('div', {'class': 'mileage'}).get_text())
        except:
            mileage.append('n/a')

        # dealer_name
        try:
            dealer_name.append(result.find('div', {'class': 'dealer-name'}).get_text().strip())
        except:
            dealer_name.append('n/a')

        # rating
        try:
            rating.append(result.find('span', {'class': 'sds-rating__count'}).get_text())
        except:
            rating.append('n/a')

        # review_count
        try:
            review_count.append(result.find('span', {'class': 'sds-rating__link'}).get_text())
        except:
            review_count.append('n/a')

        # price
        try:
            price.append(result.find('span', {'class': 'primary-price'}).get_text())
        except:
            price.append('n/a')
#Diccionario
Concesionaria= pd.DataFrame({'Nombre': name, 'Millaje':mileage, "Concesionaria": dealer_name,"Calificacion":rating,
                            "Numero de Reviews":review_count, "Precio":price})

print(Concesionaria)

Concesionaria['Numero de Reviews'] = Concesionaria['Numero de Reviews'].apply(lambda x: x.strip('reviews)').strip('('))


Concesionaria.to_sql('concesionaria', con=engine, index=False, if_exists='append')


