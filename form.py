import streamlit as st
import queryFunctions as qf

def registrar_usuario():    

    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':blue[Ingresa los datos del nuevo empleado.]')
        st.write(':blue[Los datos marcados con (*) son obligatorios.]')
        rut = st.text_input('RUT', placeholder='Ex: 12345678-9 *', )
        nombre = st.text_input('Nombres', placeholder='Ingresa tus nombres *')
        apellido1 = st.text_input('Primer apellido', placeholder='Ingresa tu primer apellido *')
        apellido2 = st.text_input('Segundo apellido', placeholder='Ingresa tu segundo apellido *')
        cargo  = st.selectbox('Cargo', ['Conductor','Administrativo','Nochero','Auxiliar','Trabajador Agricola','Bodeguero','Jefe Campo','Jefe Mecanica','Jefe Logistica','Administrador'], index=0)
        rut_empresa = st.text_input('Rut empresa asociada', placeholder='Ex: 912345678 *')
        b_signup = st.form_submit_button('Registrar')
        if b_signup:
            query = "INSERT INTO proyecto_semestral.empleado (rut_empleado, nombres_empleado, apellido1_empleado, apellido2_empleado, cargo, empresa_asociada) VALUES (%s, %s, %s, %s, %s, %s)"
            data = (rut, nombre, apellido1, apellido2, cargo, rut_empresa)
            qf.insert_data(query, data)
            data = (rut, nombre, apellido1, apellido2, cargo, rut_empresa)
            st.success("Empleado registrado con éxito.", icon="🎉")
            

def registrar_vehiculo():    
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':blue[Ingresa los datos del nuevo vehículo.]')
        st.write(':blue[Los datos marcados con (*) son obligatorios.]')
        patente = st.text_input('Patente', placeholder='Ex: ABCD12 *')
        marca = st.text_input('Marca', placeholder='Ingresa la marca del vehiculo *')
        modelo = st.text_input('Modelo', placeholder='Ingresa el modelo del vehiculo *')
        año = st.number_input('Año', min_value=1900, step=10)
        pdf_rev_tecnica = st.text_input('Link PDF revision tecnica', placeholder='Ingrese el link al PDF *')
        fecha_ven_rev_tec = st.date_input('Fecha de vencimiento Rev. Tecnica')
        pdf_permiso_circ = st.text_input('Link PDF permiso de circulacion', placeholder='Ingrese el link al PDF *')
        pdf_soap = st.text_input('Link PDF del SOAP', placeholder='Ingrese el link al PDF *')
        pdf_contrato_gps = st.checkbox('Contrato del gps')
        fecha_dom_vigente = st.date_input('Fecha emision dominio vigente')
        pdf_dom_vigente = st.text_input('Link PDF dominio vigente', placeholder='Ingrese el link al PDF *')
        tipo_vehiculo = st.text_input('Tipo de vehiculo', placeholder='Ingrese el tipo de vehiculo *')
        rut_empresa = st.text_input('Rut de empresa asociada', placeholder='Ingrese el rut de la empresa *')
        c_signup = st.form_submit_button('Registrar')
        
        if c_signup:
            try:
                # Insertar en dominio_vigente
                query_dominio = "INSERT INTO proyecto_semestral.dominio_vigente (fecha_emision, PDF_dominio_vigente) VALUES (%s, %s) RETURNING ID_dominio_vigente"
                data_dominio = (fecha_dom_vigente, pdf_dom_vigente)
                id_dominio = qf.insert_data_returning_id(query_dominio, data_dominio)

                # Insertar en revision_tecnica
                query_revision = "INSERT INTO proyecto_semestral.revision_tecnica (PDF_revision_tecnica, fecha_ven_rev_tecnica) VALUES (%s, %s) RETURNING ID_revision"
                data_revision = (pdf_rev_tecnica, fecha_ven_rev_tec)
                id_revision = qf.insert_data_returning_id(query_revision, data_revision)

                # Insertar en vehiculo
                query_vehiculo = """
                INSERT INTO proyecto_semestral.vehiculo (
                    patente, marca, año, modelo, ID_revision, PDF_permiso_circulacion, 
                    PDF_SOAP, PDF_contrato_gps, ID_dominio_vigente, tipo_vehiculo, RUT_empresa
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                data_vehiculo = (
                    patente, marca, modelo,año, id_revision, pdf_permiso_circ, 
                    pdf_soap, pdf_contrato_gps, id_dominio, tipo_vehiculo, rut_empresa
                )
                qf.insert_data(query_vehiculo, data_vehiculo)

                st.success("Vehículo registrado con éxito.", icon="🎉")
            except Exception as e:
                st.error(f"Error al registrar el vehículo: {e}")

def registrar_ruta():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':blue[Ingresa los datos de la nueva ruta.]')
        st.write(':blue[Los datos marcados con (*) son obligatorios.]')
        nombre = st.text_input('Nombre de la Ruta', placeholder='Ex: San Carlos Poniente *', )
        comuna = st.text_input('Comuna', placeholder='Ex: San Carlos *')
        d_signup = st.form_submit_button('Registrar')
        if d_signup:
            query = "INSERT INTO proyecto_semestral.ruta (nombre, comuna) VALUES (%s, %s)"
            data = (nombre, comuna)
            qf.insert_data(query, data)
            st.success("Ruta registrada con éxito.", icon="🎉")

def registrar_rendicion():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':blue[Ingresa los datos de la nueva rendición.]')
        st.write(':blue[Los datos marcados con (*) son obligatorios.]')
        rut_empleado = st.text_input('Rut del empleado', placeholder='Ingrese el rut del empleado *')
        tipo_rendicion = st.selectbox('Tipo de rendicion', ['Alimento', 'Combustible', 'Lubricantes', 'Adblue', 'Vulcanizacion', 'Transportes', 'Peaje', 'Repuestos', 'Estacionamiento', 'Hospedaje', 'Otros'], index=0)
        pdf_doc_asociado = st.text_input('Link PDF del documento asociado', placeholder='Ingrese el Link *')
        monto = st.number_input('Monto', min_value=0, step=1000)
        e_signup = st.form_submit_button('Registrar')
        if e_signup:
            query = "INSERT INTO proyecto_semestral.rendicion (RUT_empleado, tipo_rendicion, PDF_doc_asociado, monto) VALUES (%s, %s, %s, %s)"
            data = (rut_empleado, tipo_rendicion, pdf_doc_asociado, monto)
            qf.insert_data(query, data)
            st.success("Rendición registrada con éxito.", icon="🎉")
            

def registrar_recorrido():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':blue[Ingresa los datos del nuevo recorrido.]')
        st.write(':blue[Los datos marcados con (*) son obligatorios.]')
        rut_conductor = st.text_input('Rut Conductor', placeholder='Ingrese Rut del conductor *')
        patente = st.text_input('Patente del vehículo', placeholder='Ingrese la patente del vehículo *')
        nombre_ruta = st.text_input('Nombre Ruta', placeholder='Ingrese el nombre de la ruta *')
        fecha = st.date_input('Fecha del recorrido')
        id_estanque = st.text_input('Id de estanque', placeholder='Ingrese el id del estanque *')
        f_signup = st.form_submit_button('Registrar')
        
        if f_signup:
            if not all([rut_conductor, patente, nombre_ruta, id_estanque]):
                st.error("Por favor, complete todos los campos obligatorios.")
                return
            
            try:
                query = "INSERT INTO proyecto_semestral.recorrido (RUT_conductor, patente, nombre_ruta, fecha, id_estanque) VALUES (%s, %s, %s, %s, %s)"
                data = (rut_conductor, patente, nombre_ruta, fecha, id_estanque)
                qf.insert_data(query, data)
                st.success("Recorrido registrado con éxito.", icon="🎉")
            except Exception as e:
                st.error(f"Error al registrar el recorrido: {e}")

def registrar_cambio_vehiculo():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader(':blue[Ingresa los datos del nuevo cambio de vehículo.]')
        st.write(':blue[Los datos marcados con (*) son obligatorios.]')
        rut_empleado = st.text_input('Rut del empleado', placeholder='Ingrese el rut del empleado *')
        patente = st.text_input('Patente del vehículo', placeholder='Ingrese la patente del vehículo *')
        fecha = st.date_input('Fecha del cambio')
        g_signup = st.form_submit_button('Registrar')
        if g_signup:
            query = "INSERT INTO proyecto_semestral.cambio_vehiculo (rut_empleado, patente, fecha) VALUES (%s, %s, %s)"
            data = (rut_empleado, patente, fecha)
            qf.insert_data(query, data)
            st.success("Cambio de vehículo registrado con éxito.", icon="🎉")