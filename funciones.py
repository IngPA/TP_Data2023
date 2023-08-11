import requests
import config
from config import clavepostgres
import psycopg2
import json
apikey = config.mykey

"""
obtener_id_ciudad: dada una ciudad, devuelve el id segun documentacion de la appi
que es una clave unica para cada ciudad

"""
def obtener_id_ciudad(ciudad):
    url = f"http://api.openweathermap.org/data/2.5/find?appid={apikey}&q={ciudad}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['count'] > 0:
            return data['list'][0]['id']
    return None
        
"""
Funcion consulta1: busca en la api los pronosticos(json), 
y devuelve las listas de datos pronostico y citysdate. 
"""
#construcción de la función de consulta endpoint forecast
def consulta1(ciudad, city_id):

  apikey = config.mykey
 
  base_url= 'https://api.openweathermap.org/data/2.5/forecast?'
  url = f'{base_url}id={city_id}&appid={apikey}&units=metric'

  response = requests.get(url)
  if response.status_code == 200:
    response_json = response.json()    
    ciudad= response_json["city"]["name"]
    pronostico = []
    for i in response_json['list']:
        j =[i['dt_txt'],
            ciudad,
            city_id,
            i['main']['temp'],
            i['main']['feels_like'],
            i['main']['pressure'],
            i['main']['humidity'],
            i['wind']['speed'],
            i['wind']['deg'] ,
            i['weather'][0]['description']
            ]
        pronostico.append(j)
 
    citysdate = [
            response_json['city']['id'],
            response_json['city']['name'],
            response_json['city']['coord'],
            response_json['city']['country'],
            response_json['city']['timezone'],
            response_json['city']['sunrise'],
            response_json['city']['sunset'],
            ]
    return pronostico, citysdate
  else:
    print (response.status_code)


"""
Create_database: crea una nueva base de datos
"""

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

