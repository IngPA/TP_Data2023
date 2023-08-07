import config, funciones
import requests
from sqlalchemy import create_engine, Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session 

# Creo bbdd
if __name__ == "__main__": 
    funciones.create_database('pronosticos')        #usar minusculas

#________________________________________________________________

# Conexión a la base de datos PostgreSQL usando SQLAlchemy

# Configuración de conexion a base de datos
usuario = "postgres"
contraseña = config.password
nombre_bbdd = 'pronosticos'
engine = create_engine(f'postgresql://{usuario}:{contraseña}@localhost/{nombre_bbdd}')

Base = declarative_base()

# Estructura de la base de datos / definicion de tablas y relaciones

class CitysDates(Base):
    __tablename__ = 'city_data'
    id_city= Column(Integer, primary_key=True)
    coord= Column(JSON)
    country= Column(String(4))
    timezone= Column(Integer)
    sunrise= Column(Integer)
    susnset= Column(Integer)

class Pronostico5dias(Base):
    __tablename__ = f'pronostico'
    id = Column(Integer, primary_key=True)
    dt = Column(Integer)
    fecha= Column(DateTime)
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

# Creación de la estructura de la base de datos
if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

#________________________________________________________________

# Lista de ciudades
#cityList = ["London", "New York", "Cordoba", "Taipei", "Buenos Aires", "Mexico City", "Dublin", "Amasia", "Bogota", "Tokio"]
# Obtener los IDs de las ciudades
"""
ids_ciudades = {}
for ciudad in cityList:
    city_id = funciones.obtener_id_ciudad(ciudad)
    if city_id:
        ids_ciudades[ciudad] = city_id
#el diccionario ids_ciudades proporciona {ciudad:city_id}
"""
#________________________________________________________________

# Obtención de datos meteorológicos de OpenWeatherMap
# y Extracción de los datos relevantes

#Datos a almacenar
#for ciudad in ids_ciudades: 
 #   pronostico, citysdate = funciones.consulta1(ciudad, city_id)
#print(citysdate)
#print(pronostico)

datospronostico, datoscitysdate = funciones.consulta1('London', 2643743)
#print(datoscitysdate)
#print(datospronostico)

# Almacenamiento de los datos en la base de datos
#session = Session()
city_data = CitysDates[id_city, coord, country, timezone, sunrise, susnset](datoscitysdate)
session.add(city_data)
session.commit()

pronostico = Pronostico5dias[
    dt, fecha, temperatura, sensacion_termica, presion, humedad, viento_vel, viento_dir, clima
    ](datospronostico)

session.add(pronostico)
session.commit()

session.close()

print("Datos meteorológicos almacenados con éxito.")
