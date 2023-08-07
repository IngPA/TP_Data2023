import config, funciones, creacionBD
import requests
from sqlalchemy import create_engine, Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session 

#________________________________________________________________

# Conexión a la base de datos PostgreSQL usando SQLAlchemy

# Configuración de conexion a base de datos
usuario = "postgres"
contraseña = config.password
nombre_bbdd = 'pronosticos'
engine = create_engine(f'postgresql://{usuario}:{contraseña}@localhost/{nombre_bbdd}')

Base = declarative_base()

#________________________________________________________________


datospronostico, datoscitysdate = funciones.consulta1('London', 2643743)
#print(datoscitysdate)
#print(datospronostico)


# Almacenamiento de los datos en la base de datos
#session = Session()
city_data = CitysDates(
    datoscitysdate[id_city, coord, country, timezone, sunrise, susnset])
session.add(city_data)
session.commit()

pronostico = Pronostico5dias(
    datospronostico[dt, fecha, temperatura, sensacion_termica, presion, humedad, viento_vel, viento_dir, clima])

session.add(pronostico)
session.commit()

session.close()

print("Datos meteorológicos almacenados con éxito.")
