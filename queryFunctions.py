import psycopg2
import streamlit as st

def connect_to_database():
    try:
        conn = psycopg2.connect(
           host="localhost",
            port="5432",
            database="proyecto_semestral",
            user="postgres",
            password="."
            )
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def run_query(query):
    conn = connect_to_database()
    if conn is not None:
        with conn.cursor() as cur:
            cur.execute(query)
            # Asumiendo que es una consulta SELECT, de lo contrario ajusta según sea necesario
            rows = cur.fetchall()
            return rows
    else:
        print("La conexión a la base de datos no se estableció.")
        return None
    
def insert_data(query, data):
    """
    - query: Consulta SQL de inserción.
    - data: Tupla con los datos a insertar.
    """
    conn = connect_to_database()
    if conn is not None:
        try:
            with conn.cursor() as cur:
                cur.execute(query, data)
                conn.commit()  # Confirma la transacción
                print("Datos insertados correctamente.")
        except Exception as e:
            print(f"Error al insertar datos: {e}")
        finally:
            conn.close()  # Cierra la conexión
    else:
        print("La conexión a la base de datos no se estableció.")

def insert_data_returning_id(query, data):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(query, data)
        id_returned = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        print("Datos insertados correctamente.")
        return id_returned
    except Exception as e:
        st.error(f"Error inserting data: {e}")
        return None
