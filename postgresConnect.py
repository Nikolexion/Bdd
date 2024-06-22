import streamlit as st
import pandas as pd
import queryFunctions as qf
import utils
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Aljibe", page_icon="🚛", layout="centered")

# Carga de animaciones Lottie
lottie_truck = utils.load_lottieurl("https://lottie.host/f9c20961-d879-4345-9e5f-566e4b16a5f5/APTiUuxZQl.json")
lottie_employee = utils.load_lottieurl("https://lottie.host/984d9209-266d-427e-a312-1017a42fc389/MqgsBYt17v.json")

# Menú lateral
with st.sidebar:
    st.image("resources\LOGO_LOGISTICA_Y_DISTRIBUCION-1.png", width=150,use_column_width=True)
    selected = option_menu(
        menu_title= "Aljibe App 🚛",
        options=["Home", "Empleados", "Vehículos", "Rutas actuales", "Rendiciones", "Recorridos", "Cambios de vehículo"],
        icons=["house", "person-arms-up", "truck", "geo-alt", "cash-stack", "clock-history", "tools"],
        menu_icon="list",
        default_index=0,
    )
if selected == "Home":
    # Header section
    st.title("Aljibe App 🚛")
    st.subheader(":white[Distribuidora de agua potable y recursos varios]", divider="rainbow")
    left_column, right_column = st.columns(2,)
    with left_column: 
        st.markdown("""
        <style>
        .big-font {
            font-size:22px !important;
        }
        </style>
        <p class="big-font">Bienvenido a la aplicación de monitoreo de la flota de vehículos y personal de Aljibe. Selecciona una opción del menú lateral para comenzar.</p>
        """, unsafe_allow_html=True)
    with right_column:
        st_lottie(lottie_truck, height=250, key = "truck")

    # Ejemplo de uso
    if __name__ == "__main__":
        qf.connect_to_database()
    conn = qf.connect_to_database()

    consulta = qf.run_query("SELECT re.patente AS patente_vehiculo, e.nombres_empleado AS nombre_conductor, e.apellido1_empleado AS apellido_paterno, e.apellido2_empleado AS apellido_materno, es.capacidad AS capacidad_estanque, r.nombre AS nombre_ruta, re.fecha AS fecha FROM proyecto_semestral.recorrido re JOIN proyecto_semestral.conductor c ON re.rut_conductor = c.rut_conductor JOIN proyecto_semestral.empleado e ON c.rut_conductor = e.rut_empleado JOIN proyecto_semestral.vehiculo v ON re.patente = v.patente JOIN proyecto_semestral.ruta r ON re.nombre_ruta = r.nombre JOIN proyecto_semestral.estanque es ON re.id_estanque = es.id WHERE re.fecha = CURRENT_DATE;")

    st.markdown("""
    <style>
    .big-font {
        font-size: 22px !important;
    }
    </style>
    <p class="big-font">Conductores, vehículos y rutas asignadas para el día de hoy</p>
    """, unsafe_allow_html=True)
    
    dataConsulta = pd.DataFrame(consulta)
    dataConsulta.columns = ["patente_vehiculo","nombre_conductor","apellido_paterno","ape   llido_materno","capacidad_estanque","nombre_ruta","fecha"]

    st.dataframe(dataConsulta, use_container_width=True, hide_index=True)
    st.markdown("""
    <style>
    .big-font {
        font-size: 22px !important;
    }
    </style>
    <p class="big-font">Rendiciones pendientes</p>
    """, unsafe_allow_html=True)

    rendiciones = qf.run_query("SELECT  r.Id, r.rut_empleado, r.Tipo_rendicion, r.Estado, r.PDF_doc_asociado, r.Monto FROM  proyecto_semestral.rendicion r WHERE  Estado = 'Pendiente';")

    dataRendiciones = pd.DataFrame(rendiciones)
    dataRendiciones.columns = ["Id","rut_empleado","Tipo_rendicion","Estado","PDF_doc_asociado","Monto"]

    st.dataframe(dataRendiciones, use_container_width=True, hide_index=True)

    """ Conductores con el certificado DS41 """

    certds41 = qf.run_query("SELECT c.rut_conductor AS rut, e.nombres_empleado AS nombre, e.apellido1_empleado AS apellido_materno, e.apellido2_empleado AS apellido_paterno FROM proyecto_semestral.conductor C JOIN proyecto_semestral.empleado E ON e.rut_empleado = c.rut_conductor WHERE c.certificado_ds41 = TRUE;")

    dataCertds41 = pd.DataFrame(certds41)
    dataCertds41.columns = ["rut","nombre","apellido_materno","apellido_paterno"]

    st.dataframe(dataCertds41, use_container_width=True, hide_index=True)

if selected == "Empleados":
    st.title("Empleados")
    st_lottie(lottie_employee, height=250, key = "employee")
    # Employees section
    
    rows = qf.run_query("SELECT * FROM proyecto_semestral.empleado")
    st.markdown("""
    <style>
    .big-font {
        font-size: 22px !important;
    }
    </style>
    <p class="big-font">Todos los empleados </p>
    """, unsafe_allow_html=True)

    data = pd.DataFrame(rows)
    data.columns = ["rut_empleado","nombres_empleado","apellido1_empleado","apellido2_empleado","cargo","empresa_asociada"]

    st.dataframe(data, use_container_width=True, hide_index=True)

if selected == "Vehículos":
    # Vehicles section
    st.title("Vehículos")
    st.write("En esta sección se muestran los vehículos de la empresa Aljibe.")
    vehiculos = qf.run_query("SELECT * FROM proyecto_semestral.vehiculo")

    st.markdown("""
    <style>
    .big-font {
        font-size: 22px !important;
    }
    </style>
    <p class="big-font">Todos los vehículos</p>
    """, unsafe_allow_html=True)

    dataVehiculos = pd.DataFrame(vehiculos)
    dataVehiculos.columns = ["patente","marca","modelo","año","ID_revision","ID_dominio_vigente","tipo_vehiculo","RUT_empresa","PDF_permiso_circulacion","PDF_SOAP","PDF_contrato_gps"]

    st.dataframe(dataVehiculos, use_container_width=True, hide_index=True)

if selected == "Rutas actuales":
    # Current routes section
    st.title("Rutas actuales")
    st.write("En esta sección se muestran las rutas actuales de los vehículos de la empresa Aljibe.")
    rutas = qf.run_query("SELECT * FROM proyecto_semestral.ruta")

    st.markdown("""
    <style>
    .big-font {
        font-size: 22px !important;
    }
    </style>
    <p class="big-font">Todas las rutas</p>
    """, unsafe_allow_html=True)

    dataRutas = pd.DataFrame(rutas)
    dataRutas.columns = ["nombre","comuna"]

    st.dataframe(dataRutas, use_container_width=True, hide_index=True)

if selected == "Rendiciones":
    # Renditions section
    st.title("Rendiciones")
    st.write("En esta sección se muestran las rendiciones de los empleados de la empresa Aljibe.")

    rendicionesPendientes = qf.run_query("SELECT  r.rut_empleado, r.Tipo_rendicion, r.Estado, r.PDF_doc_asociado, r.Monto FROM proyecto_semestral.rendicion r WHERE Estado = 'Pendiente';")
    rendiciones = qf.run_query("SELECT  r.rut_empleado, r.Tipo_rendicion, r.Estado, r.PDF_doc_asociado, r.Monto FROM proyecto_semestral.rendicion r;")

    st.markdown("""
    <style>
    .big-font {
        font-size: 22px !important;
    }
    </style>
    <p class="big-font">Rendiciones pendientes</p>
    """, unsafe_allow_html=True)
    dataRendicionesPendientes = pd.DataFrame(rendicionesPendientes)
    dataRendicionesPendientes.columns = ["rut_empleado","tipo_rendicion","estado","pdf_doc_asociado","monto"] 

    st.dataframe(dataRendicionesPendientes, use_container_width=True, hide_index=True)

    st.markdown("""
    <style>
    .big-font {
        font-size: 22px !important;
    }
    </style>
    <p class="big-font">Todas las rendiciones</p>
    """, unsafe_allow_html=True)

    dataRendiciones = pd.DataFrame(rendiciones)
    dataRendiciones.columns = ["rut_empleado","tipo_rendicion","estado","pdf_doc_asociado","monto"]

    st.dataframe(dataRendiciones, use_container_width=True, hide_index=True)

if selected == "Recorridos":
    # Previous routes section
    st.title("Recorridos anteriores")
    st.write("En esta sección se muestran los recorridos anteriores de los vehículos de la empresa Aljibe.")
    recorridos = qf.run_query("SELECT * FROM proyecto_semestral.recorrido")
    
    st.markdown("""
    <style>
    .big-font {
        font-size: 22px !important;
    }
    </style>
    <p class="big-font">Todos los recorridos</p>
    """, unsafe_allow_html=True)
    
    dataRecorridos = pd.DataFrame(recorridos)
    dataRecorridos.columns = ["rut_conductor","patente","nombre_ruta","fecha","id_estanque"]

    st.dataframe(dataRecorridos, use_container_width=True, hide_index=True)

if selected == "Cambios de vehículo":
    # Vehicle changes section
    st.title("Cambios de vehículo")
    st.write("En esta sección se muestran los cambios de vehículo de los conductores de la empresa Aljibe.")

    cambios = qf.run_query("SELECT cv.rut_conductor AS rut_conductor, cv.patente AS patente, cv.fecha_inicio AS fecha_inicio, cv.fecha_termino AS fecha_termino, c.motivo_cambio AS motivo_cambio, c.autor_cambio AS autor_cambio FROM proyecto_semestral.conductor_en_vehiculo cv JOIN proyecto_semestral.cambio c ON cv.id_cambio = c.id_cambio WHERE fecha_termino IS NOT NULL;")
    st.markdown("""
    <style>
    .big-font {
        font-size: 22px !important;
    }
    </style>
    <p class="big-font">Todos los vehiculos</p>
    """, unsafe_allow_html=True)

    dataCambios = pd.DataFrame(cambios)
    dataCambios.columns = ["rut_conductor","patente","fecha_inicio","fecha_termino","motivo_cambio","autor_cambio"]

    st.dataframe(dataCambios, use_container_width=True, hide_index=True)

    



#query = "INSERT INTO proyecto_semestral.empleado (rut_empleado, nombres_empleado, apellido1_empleado, apellido2_empleado, cargo, empresa_asociada) VALUES (%s, %s, %s, %s, %s, %s)"
#data = ('12345678-9', 'Juan', 'Pérez', 'González', 'Administrativo', '01234567890')
#insert_data(query, data)

