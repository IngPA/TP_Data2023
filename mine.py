#1 Con el nombre de las ciudades requeridas, construimos un diccionario ciudad-id
import requests
import config
import funciones
import json

# API Key de OpenWeatherMap
apikey = config.mykey

# Lista de ciudades
cityList = ["London", "New York", "Cordoba", "Taipei", "Buenos Aires", "Mexico City", "Dublin", "Amasia", "Bogota", "Tokio"]

# Obtener diccionario {ciudad : IDs de las ciudades}
ciudades_ids = {}
for ciudad in cityList:
    city_id = funciones.obtener_id_ciudad(ciudad)
    if city_id:
        ciudades_ids[ciudad] = city_id

# Con este diccionario llamamos a las consultas a la api, 

# Las funciones para traer los datos de la api estan construidas en el archivo funciones.py
# Se utiliza la consulta forecast, y se seleccionan datos relevantes del response.
# consulta1(ciudad, city_id):, retorna dos listas:  pronostico y citysdate 
# con pronostico para cinco días de una ciudad. 

# para rellenar la bbdd utilizaremos estas listas

_________________________________________________________________________
# Construccion de bbdd
import sqlalchemy
# Construccion de bbdd
# sqlalchemy, config
# importamos librerias requeridas
import config
from sqlalchemy import create_engine

#import pandas as pd
#from datetime import datetime
#from sqlalchemy.orm import sessionmaker, declarative_base, relationship
#from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey

#CONEXION A BBDD
#parametros: 
host="localhost"
port="5432"
usuario = "postgres"
contraseña = config.password
nombre_bbdd = 'tpData2023'
#creación del conector engine (crea la bbdd si no existe)
engine = create_engine(f'postgresql://{usuario}:{contraseña}@localhost:5432/{nombre_bbdd}')

# Creación estructura de la bbdd

"""

Base = declarative_base()

class Empleado(Base):
    __tablename__ = 'empleado'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50))
    apellido = Column(String(50))

class Pedido(Base):
    __tablename__ = 'pedido'
    id = Column(Integer, primary_key=True, autoincrement=True)
    texto = Column(String(50))
    fecha_hora = Column(DateTime)
    empleado_id = Column(Integer, ForeignKey('empleado.id'))
    empleado = relationship(Empleado)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    username = Column(String(50), nullable=False, unique=True) 
    email = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime(), default=datetime.now())

    def __str__(self):
        return self.username


Session = sessionmaker(engine)
session = Session()


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
"""


# Descarga de la información en json, para 10 ciudades


# Procesamiento y actualización de la información en la base de datos
#se debe poder ejecutar desde un archivo .py













#_________________________________________________________________________
## Consulta a la API, endpoint forecast
# consulta1(ciudad, city_id):, que retorna dos listas:  pronostico y citysdate 
# con pronostico para cinco días de una ciudad (datos relevantes seleccionados)


for ciudad, city_id in ids_ciudades.items():
    #print(f"{ciudad}: {city_id}")
    pronostico, citysdate = consulta1(ciudad, city_id)
