
import requests
import config

#_________________________________________________________________________
# Funciones:
#  1 Función para obtener el ID de una ciudad, mediante nombre existente en listado
#  2 Función consulta api whetermap endpoint forecast
#  3 Función creacion nueva bbdd en postgres

#_________________________________________________________________________
# 1 
# API Key de OpenWeatherMap
apikey = config.mykey

# Función para obtener el ID de una ciudad
def obtener_id_ciudad(ciudad):
    url = f"http://api.openweathermap.org/data/2.5/find?appid={apikey}&q={ciudad}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['count'] > 0:
            return data['list'][0]['id']
    return None

# Lista de ciudades
cityList = ["London", "New York", "Cordoba", "Taipei", "Buenos Aires", "Mexico City", "Dublin", "Amasia", "Bogota", "Tokio"]

# Obtener los IDs de las ciudades
ids_ciudades = {}
for ciudad in cityList:
    city_id = obtener_id_ciudad(ciudad)
    if city_id:
        ids_ciudades[ciudad] = city_id

# Imprimir los IDs de las ciudades
for ciudad, city_id in ids_ciudades.items():
    print(f"{ciudad}: {city_id}")

#_________________________________________________________________________
# 2 Consulta a la API, con estructura
# pronostico para cinco días
### seleccionando datos de interes ###
import requests
import json
import config

#construcción de la función de consulta endpoint forecast
def consulta1(ciudad, city_id):
  # API Key de OpenWeatherMap
  apikey = config.mykey
  #Ciudad id --BUSCA EN DICCIONARIO

  # construccion url
  base_url= 'https://api.openweathermap.org/data/2.5/forecast?'
  url = f'{base_url}id={city_id}&appid={apikey}&units=metric'

  # llamada HTTP GET
  response = requests.get(url)
  if response.status_code == 200:
    response_json = response.json()      #trae los pronosticos a 5 dias para la ciudad consultada,
    ciudad= response_json["city"]["name"]
    pronostico = []
    for i in response_json['list']:
        j =[i['dt'],
            i['dt_txt'],
            # if i['rain']['3h'] is not None, else:  n'precipitacion(acum3hs)', 'nieve(acum3hs)',
            # i['snow']['3h'],
            i['main']['temp'],
            i['main']['feels_like'],
            i['main']['pressure'],
            i['main']['humidity'],
            i['wind']['speed'],
            i['wind']['deg'] ,
            i['weather'][0]['description']
            ]
        pronostico.append(j)
    #print(pronostico)
    # Selecciono los datos relevantes de cada json para cada ciudad
    # caracteristicas de las ciudades consultadas
    citysdate = [                           #response_json['city'],
            response_json['city']['id'],
            response_json['city']['name'],
            response_json['city']['coord'],
            response_json['city']['country'],
            response_json['city']['timezone'],
            response_json['city']['sunrise'],
            response_json['city']['sunset'],
            ]
    #print(citysdate)

    return pronostico, citysdate
  else:
    print (response.status_code)

#pronostico, citysdate = consulta1('London', 2643743)
#print(citysdate)
#print(pronostico)

#_________________________________________________________________________
# 3 
from config import clavepostgres
import psycopg2

def create_database(nombre_base_de_datos): 
    nueevabd = nombre_base_de_datos
    try: 
        # Conectarse al servidor PostgreSQL
        conn = psycopg2.connect(database="postgres", user='postgres', 
                                password=clavepostgres, host='127.0.0.1', port= '5432'
                                )
        conn.autocommit = True 

        # Crear un objeto de conexión para ejecutar comandos SQL 
        cursor = conn.cursor() 

        # Presparar query para crear base de datos
        sql = f'CREATE database {nueevabd}'

        # Crear la base de datos 
        cursor.execute(sql) 
        print(f"Base de datos {nueevabd} creada exitosamente.") 

    except psycopg2.Error as e: 
        print(f"Error al crear la base de datos: {e}") 
    finally: 
        # Cerrar la conexión 
        if conn: 
            conn.close() 

if __name__ == "__main__": 
    create_database('mydb')
    """
    for i in 1,2: 
        databasename= f'mydb{i}'
        create_database(databasename)
    """

#_________________________________________________________________________


#_________________________________________________________________________
