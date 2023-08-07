import config
from sqlalchemy import create_engine, Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship 


# Conexión a la base de datos PostgreSQL usando SQLAlchemy
usuario = 'postgres'
contraseña = config.password
nombre_bbdd = 'pronosticos'
engine = create_engine(f'postgresql://{usuario}:{contraseña}@localhost/{nombre_bbdd}')

# Estructura de los datos
Base = declarative_base()

class CitysDates(Base):
    __tablename__ = 'city_dates'
    id_city= Column(Integer, primary_key=True)
    coord= Column(JSON)
    country= Column(String(50))
    timezone= Column(Integer)
    sunrise= Column(Integer)
    susnset= Column(Integer)

class Pronostico5dias(Base):
    __tablename__ = f'Clima5dias'
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
    id_city= Column(Integer, ForeignKey('city_dates.id_city') )
    city_dates = relationship(CitysDates)

Session = sessionmaker(engine)
session = Session()

if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

# Obtuve un json desde la APi whethermap
# La trabaje para obtener listas de datos relevantes
#Hago una base de datos, que voy a cargar con la lista de cada ciudad
#Podria hacer una sola tabla con todos los valores traidos, o una tabla por ciudad.
# cargo una tabla por ciudad