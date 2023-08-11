import config, funciones
import requests
from sqlalchemy import create_engine, Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session 
import pandas as pd
import json

"""
Creacion nueva base de datos
"""
if __name__ == "__main__": 
    funciones.create_database('pronosticos') 

"""
Configuración de conexion a base de datos
"""
usuario = "postgres"
contraseña = config.password
nombre_bbdd = 'pronosticos'
engine = create_engine(f'postgresql://{usuario}:{contraseña}@localhost/{nombre_bbdd}')

Base = declarative_base()

"""
Estructura de la base de datos / definicion de tablas y relaciones
"""
class CitysDates(Base):
    __tablename__ = 'city_data'
    id_city= Column(Integer, primary_key=True)
    name_city= Column(String(30))
    coord= Column(JSON)
    country= Column(String(4))
    timezone= Column(Integer)
    sunrise= Column(Integer)
    susnset= Column(Integer)

class Pronostico5dias(Base):
    __tablename__ = f'pronostico'
    id = Column(Integer, primary_key=True)
    fecha= Column(DateTime)
    ciudad= Column(String(30))
    temperatura= Column(Integer)
    sensacion_termica= Column(Integer)
    presion= Column(Integer)
    humedad= Column(Integer)
    viento_vel= Column(Integer)
    viento_dir= Column(Integer)
    clima = Column(String(50))
    id_city= Column(Integer, ForeignKey('city_data.id_city') )
    city_data = relationship(CitysDates)


Session = sessionmaker(engine)
session = Session()


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

"""
Obtengo diccionario de el diccionario ids_ciudades que proporciona {ciudad:city_id}, 
a partir de una lista de ciudades. 
"""
cityList = ["London", "New York", "Cordoba", "Taipei", "Buenos Aires", "Mexico City", "Dublin", "Amasia", "Bogota", "Tokio"]

ids_ciudades = {}
for ciudad in cityList:
    city_id = funciones.obtener_id_ciudad(ciudad)
    if city_id:
        ids_ciudades[ciudad] = city_id

"""
Obtención de datos meteorológicos de OpenWeatherMap
y Extracción de los datos relevantes --> consulta1() 
"""
datos_ciudad = []
datos_pronostico = []
for ciudad,city_id in ids_ciudades.items():
  pronostico, citysdate = funciones.consulta1(ciudad,city_id)
  datos_ciudad.append(citysdate)
  datos_pronostico.extend(pronostico)
 
"""
Convertir lista en dataframe
"""
dfciudad= pd.DataFrame(datos_ciudad,columns=['id_city', 'name_city', 'coord', 'country', 'timezone', 'sunrise', 'susnset'])
dfpronosticos= pd.DataFrame(datos_pronostico,columns=['fecha', 'ciudad', 'id_city', 'temperatura', 'sensacion_termica', 'presion', 'humedad', 'viento_vel', 'viento_dir', 'clima'])

"""
Convetir dataframe en archivos csv
"""
dfciudad.to_csv('ciudad.csv', index = False)
dfpronosticos.to_csv('pronostico.csv', index = False)

"""
Convertir DataFrame en diccionario
"""
dict_ciudad = dfciudad.to_dict(orient='records')
dict_pronostico = dfpronosticos.to_dict(orient='records')

"""
Convertir el diccionario en un objeto JSON
"""
json_city = json.dumps(dict_ciudad, indent=4)
json_pronosticos = json.dumps(dict_pronostico, indent=4)
 

"""
Almacenamiento de los datos en la base de datos
"""
Session = sessionmaker(bind=engine)
session = Session()

for index, row in dfciudad.iterrows():
    new_row = CitysDates(
        id_city=row['id_city'],
        name_city=row['name_city'],
        coord=row['coord'],
        country=row['country'],
        timezone=row['timezone'],
        sunrise=row['sunrise'],
        susnset=row['susnset']
    )
    session.add(new_row)

session.commit()
print('Datos tabla city_date cargados')

for index, row in dfpronosticos.iterrows():
    new_row = Pronostico5dias(
        fecha=row['fecha'],
        ciudad=row['ciudad'],
        id_city=row['id_city'],
        temperatura=row['temperatura'],
        sensacion_termica=row['sensacion_termica'],
        presion=row['presion'],
        humedad=row['humedad'],
        viento_vel=row['viento_vel'],
        viento_dir=row['viento_dir'],
        clima=row['clima']
    )
    session.add(new_row)
session.commit()
print('Datos tabla pronostico 5 dias cargados')

session.close()

 