import streamlit as st
import psycopg2
import pandas as pd

st.set_page_config(page_title="Aljibe", page_icon="🚛", layout="wide")

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

# Ejemplo de uso
rows = run_query("SELECT * FROM proyecto_semestral.empleado")
if rows is not None:
    for row in rows:
        print(row)
if __name__ == "__main__":
    connect_to_database()
conn = connect_to_database()

@ st.cache_data
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    
rows = run_query("SELECT * FROM proyecto_semestral.empleado")
    
data = pd.DataFrame(rows)
data.columns = ["rut_empleado","nombres_empleado","apellido1_empleado","apellido2_empleado","cargo","empresa_asociada"]


st.dataframe(data, use_container_width=True, hide_index=True)

consulta = run_query("SELECT re.patente AS patente_vehiculo, e.nombres_empleado AS nombre_conductor, e.apellido1_empleado AS apellido_paterno, e.apellido2_empleado AS apellido_materno, es.capacidad AS capacidad_estanque, r.nombre AS nombre_ruta, re.fecha AS fecha FROM proyecto_semestral.recorrido re JOIN proyecto_semestral.conductor c ON re.rut_conductor = c.rut_conductor JOIN proyecto_semestral.empleado e ON c.rut_conductor = e.rut_empleado JOIN proyecto_semestral.vehiculo v ON re.patente = v.patente JOIN proyecto_semestral.ruta r ON re.nombre_ruta = r.nombre JOIN proyecto_semestral.estanque es ON re.id_estanque = es.id WHERE re.fecha = CURRENT_DATE;")

dataConsulta = pd.DataFrame(consulta)
dataConsulta.columns = ["patente_vehiculo","nombre_conductor","apellido_paterno","apellido_materno","capacidad_estanque","nombre_ruta","fecha"]

st.dataframe(dataConsulta, use_container_width=True, hide_index=True)


""" 
query = "INSERT INTO proyecto_semestral.empleado (rut_empleado, nombres_empleado, apellido1_empleado, apellido2_empleado, cargo, empresa_asociada) VALUES (%s, %s, %s, %s, %s, %s)"
data = ('12345678-9', 'Juan', 'Pérez', 'González', 'Administrativo', '01234567890')

insert_data(query, data)
 """
