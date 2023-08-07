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