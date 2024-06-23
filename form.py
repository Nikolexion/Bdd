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
        cargo = st.text_input('Cargo', placeholder='Ingresa el cargo del empleado *')
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
        patente = st.text_input('Patente', placeholder='Ex: ABCD12 *', )
        marca = st.text_input('Marca', placeholder='Ingresa la marca del vehiculo *')
        modelo = st.text_input('Modelo', placeholder='Ingresa el modelo del vehiculo *')
        pdf_rev_tecnica = st.text_input('Link PDF revision tecnica', placeholder='Ingrese el link al PDF *')
        fecha_ven_rev_tec = st.date_input('Fecha de vencimiento Rev. Tecnica')
        pdf_permiso_circ = st.text_input('Link PDF permiso de circulacion', placeholder='Ingrese el link al PDF *')
        pdf_soap = st.text_input('Link PDF del SOAP', placeholder='Ingrese el link al PDF *')
        pdf_contrato_gps = st.text_input('Link PDF del contrato del gps', placeholder='Ingrese el link al PDF *')
        fecha_dom_vigente = st.date_input('Fecha emision dominio vigente')
        pdf_dom_vigente = st.text_input('Link PDF dominio vigente', placeholder='Ingrese el link al PDF *')
        tipo_vehiculo = st.text_input('Tipo de vehiculo', placeholder='Ingrese el tipo de vehiculo *')
        rut_empresa = st.text_input('Rut de empresa asociada', placeholder='Ingrese el rut de la empresa *')
        c_signup = st.form_submit_button('Registrar')
        if c_signup:
            query = "INSERT INTO proyecto_semestral.vehiculo (patente, marca, modelo, pdf_rev_tecnica, fecha_ven_rev_tec, pdf_permiso_circ, pdf_soap, pdf_contrato_gps, fecha_dom_vigente, pdf_dom_vigente, tipo_vehiculo, rut_empresa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (patente, marca, modelo, pdf_rev_tecnica, fecha_ven_rev_tec, pdf_permiso_circ, pdf_soap, pdf_contrato_gps, fecha_dom_vigente, pdf_dom_vigente, tipo_vehiculo, rut_empresa)
            qf.insert_data(query, data)
            st.success("Empleado registrado con éxito.", icon="🎉")