CREATE SCHEMA proyecto_semestral;

CREATE TABLE proyecto_semestral.empresa(
    RUT_empresa VARCHAR(11) PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE proyecto_semestral.empleado(
    RUT_empleado VARCHAR(11) PRIMARY KEY,
    nombres_empleado TEXT NOT NULL,
    apellido1_empleado TEXT NOT NULL,
    apellido2_empleado TEXT NOT NULL,
    cargo TEXT CHECK (cargo IN ('Conductor','Administrativo','Nochero','Auxiliar','Trabajador Agricola','Bodeguero','Jefe Campo','Jefe Mecanica','Jefe Logistica','Administrador')) NOT NULL,
    empresa_asociada VARCHAR(11) REFERENCES proyecto_semestral.empresa(RUT_empresa)
);

CREATE TABLE proyecto_semestral.contrato(
    ID NUMERIC PRIMARY KEY,
    fecha_inicio DATE,
    fecha_termino DATE,
    AFP_prevision TEXT,
    tipo_contrato TEXT CHECK (tipo_contrato IN ('Por turno','Faena','Plazo Indefinido','Plazo Fijo')) NOT NULL,
    RUT_empleado VARCHAR(11) REFERENCES proyecto_semestral.empleado(RUT_empleado),
    RUT_empresa VARCHAR(11) REFERENCES proyecto_semestral.empresa(RUT_empresa)
);

CREATE TABLE proyecto_semestral.contrato_por_turno(
    ID NUMERIC REFERENCES proyecto_semestral.contrato(ID) PRIMARY KEY,
    turno TEXT,
    tipo_turno TEXT CHECK (tipo_turno IN ('Ordinario','Extraordinario')) NOT NULL,
    PDF_permiso_inspeccion TEXT
);

CREATE TABLE proyecto_semestral.contrato_por_faena(
    ID NUMERIC REFERENCES proyecto_semestral.contrato(ID) PRIMARY KEY,
    fecha_termino DATE NOT NULL
);

CREATE TABLE proyecto_semestral.contrato_por_plazo_fijo(
    ID NUMERIC REFERENCES proyecto_semestral.contrato(ID) PRIMARY KEY,
    fecha_termino DATE NOT NULL
);

CREATE TABLE proyecto_semestral.rendicion(
    ID SERIAL PRIMARY KEY,
    RUT_empleado VARCHAR(11) REFERENCES proyecto_semestral.empleado(RUT_empleado),
    tipo_rendicion TEXT CHECK (tipo_rendicion IN ('Alimento','Combustible','Lubricantes','Adblue','Vulcanizacion','Transportes','Peaje','Repuestos','Estacionamiento','Hospedaje','Otros')) NOT NULL,
    estado TEXT CHECK (estado IN ('Pendiente','Aprobada','Rechazada')) DEFAULT 'Pendiente',
    PDF_doc_asociado TEXT NOT NULL,
    monto INT NOT NULL
);

CREATE TABLE proyecto_semestral.dominio_vigente(
    ID_dominio_vigente SERIAL PRIMARY KEY,
    fecha_emision DATE,
    PDF_dominio_vigente TEXT NOT NULL
);

CREATE TABLE proyecto_semestral.revision_tecnica(
    ID_revision SERIAL PRIMARY KEY,
    PDF_revision_tecnica TEXT NOT NULL,
    fecha_ven_rev_tecnica DATE NOT NULL
);

CREATE TABLE proyecto_semestral.vehiculo(
    patente VARCHAR(11) PRIMARY KEY,
    marca TEXT,
    modelo TEXT,
    año INT,
    ID_revision SERIAL REFERENCES proyecto_semestral.revision_tecnica(ID_revision),
    PDF_permiso_circulacion TEXT NOT NULL,
    PDF_SOAP TEXT NOT NULL,
    PDF_contrato_gps BOOLEAN NOT NULL,
    ID_dominio_vigente SERIAL REFERENCES proyecto_semestral.dominio_vigente(ID_dominio_vigente),
    tipo_vehiculo TEXT,
    RUT_empresa VARCHAR(11) REFERENCES proyecto_semestral.empresa(RUT_empresa)
);

CREATE TABLE proyecto_semestral.licencia(
    ID_licencia SERIAL PRIMARY KEY,
    PDF_licencia TEXT NOT NULL,
    fecha_ven_licencia DATE NOT NULL,
    tipo_licencia TEXT CHECK (tipo_licencia IN ('A1','A2','A3','A4','A5','B')) NOT NULL
);

CREATE TABLE proyecto_semestral.carnet(
    ID_carnet SERIAL PRIMARY KEY,
    PDF_carnet TEXT NOT NULL,
    fecha_ven_carnet DATE NOT NULL
);

CREATE TABLE proyecto_semestral.conductor(
    RUT_conductor VARCHAR(11) REFERENCES proyecto_semestral.empleado(RUT_empleado) PRIMARY KEY,
    ID_carnet SERIAL REFERENCES proyecto_semestral.carnet(ID_carnet) UNIQUE,
    ID_licencia SERIAL REFERENCES proyecto_semestral.licencia(ID_licencia) UNIQUE,
    certificado_DS41 BOOLEAN NOT NULL
);

CREATE TABLE proyecto_semestral.cambio(
    ID_cambio SERIAL PRIMARY KEY,
    fecha_cambio DATE DEFAULT NOW(),
    motivo_cambio TEXT,
    autor_cambio TEXT
);

CREATE TABLE proyecto_semestral.conductor_en_vehiculo(
    RUT_conductor VARCHAR(11) REFERENCES proyecto_semestral.conductor(RUT_conductor),
    patente VARCHAR(6) REFERENCES proyecto_semestral.vehiculo(patente),
    fecha_inicio DATE DEFAULT NOW(),
    fecha_termino DATE,
    ID_cambio SERIAL REFERENCES proyecto_semestral.cambio(ID_cambio),    
    PRIMARY KEY (RUT_conductor,patente,fecha_inicio)
);

CREATE TABLE proyecto_semestral.ruta(
    nombre TEXT PRIMARY KEY,
    comuna TEXT NOT NULL
);

CREATE TABLE proyecto_semestral.estanque(
    ID SERIAL PRIMARY KEY,
    material TEXT NOT NULL,
    capacidad TEXT NOT NULL
);

CREATE TABLE proyecto_semestral.recorrido(
    RUT_conductor VARCHAR(11) REFERENCES proyecto_semestral.conductor(RUT_conductor),
    patente VARCHAR(6) REFERENCES proyecto_semestral.vehiculo(patente),
    nombre_ruta TEXT REFERENCES proyecto_semestral.ruta(nombre),
    fecha DATE DEFAULT NOW(),
    ID_estanque SERIAL REFERENCES proyecto_semestral.estanque(ID),
    PRIMARY KEY (RUT_conductor,patente,nombre_ruta,fecha)
);

-- Tabla empresa
INSERT INTO proyecto_semestral.empresa (RUT_empresa, nombre) VALUES
    ('12345678901', 'Empresa Uno'),
    ('23456789012', 'Empresa Dos'),
    ('34567890123', 'Empresa Tres'),
    ('45678901234', 'Empresa Cuatro'),
    ('56789012345', 'Empresa Cinco'),
    ('67890123456', 'Empresa Seis'),
    ('78901234567', 'Empresa Siete'),
    ('89012345678', 'Empresa Ocho'),
    ('90123456789', 'Empresa Nueve'),
    ('01234567890', 'Empresa Diez');

-- Tabla empleado
INSERT INTO proyecto_semestral.empleado (RUT_empleado, nombres_empleado, apellido1_empleado, apellido2_empleado, cargo, empresa_asociada) VALUES
    ('11111111111', 'Juan Pablo', 'Perez', 'Gomez', 'Conductor', '12345678901'),
    ('22222222222', 'Pedro Esteban', 'Lopez', 'Martinez', 'Jefe Campo', '23456789012'),
    ('33333333333', 'María Paz', 'Hernandez', 'Sanchez', 'Administrativo', '34567890123'),
    ('44444444444', 'Ana María', 'Garcia', 'Rodriguez', 'Conductor', '45678901234'),
    ('55555555555', 'Luis Ignacio', 'Martinez', 'Perez', 'Nochero', '56789012345'),
    ('66666666666', 'José Carlos', 'Gonzalez', 'Fernandez', 'Conductor', '67890123456'),
    ('77777777777', 'Laura Esperanza', 'Torres', 'Diaz', 'Nochero', '78901234567'),
    ('88888888888', 'Carlos Tomás', 'Alvarez', 'Norambuena', 'Conductor', '89012345678'),
    ('99999999999', 'Marta Ignacia', 'Gomez', 'Ruiz', 'Administrativo', '90123456789'),
    ('10101010101', 'Miguel Ángel', 'Sanchez', 'Garcia', 'Conductor', '01234567890');

-- Tabla contrato
INSERT INTO proyecto_semestral.contrato (ID, fecha_inicio, fecha_termino, AFP_prevision, tipo_contrato, RUT_empleado, RUT_empresa) VALUES
    (1, '2023-01-01', '2024-01-01', 'AFP 1', 'Por turno', '11111111111', '12345678901'),
    (2, '2023-02-01', '2024-02-01', 'AFP 2', 'Faena', '22222222222', '23456789012'),
    (3, '2023-03-01', '2024-03-01', 'AFP 3', 'Plazo Indefinido', '33333333333', '34567890123'),
    (4, '2023-04-01', '2024-04-01', 'AFP 4', 'Por turno', '44444444444', '45678901234'),
    (5, '2023-05-01', '2024-05-01', 'AFP 5', 'Faena', '55555555555', '56789012345'),
    (6, '2023-06-01', '2024-06-01', 'AFP 6', 'Plazo Indefinido', '66666666666', '67890123456'),
    (7, '2023-07-01', '2024-07-01', 'AFP 7', 'Por turno', '77777777777', '78901234567'),
    (8, '2023-08-01', '2024-08-01', 'AFP 8', 'Plazo Fijo', '88888888888', '89012345678'),
    (9, '2023-09-01', '2024-09-01', 'AFP 9', 'Faena', '99999999999', '90123456789'),
    (10, '2023-10-01', '2024-10-01', 'AFP 10', 'Por turno', '10101010101', '01234567890');

-- Tabla rendicion
INSERT INTO proyecto_semestral.rendicion (tipo_rendicion, RUT_empleado, estado, PDF_doc_asociado, monto) VALUES
    ('Alimento','11111111111', 'Pendiente', 'combustible1.pdf', 50000),
    ('Peaje', '22222222222', 'Aprobada', 'reparacion1.pdf', 150000),
    ('Repuestos', '33333333333', 'Rechazada', 'mantenimiento1.pdf', 20000),
    ('Transportes', '44444444444', 'Pendiente', 'combustible2.pdf', 45000),
    ('Combustible', '55555555555', 'Aprobada', 'reparacion2.pdf', 120000),
    ('Adblue', '66666666666', 'Pendiente', 'mantenimiento2.pdf', 30000),
    ('Hospedaje', '77777777777', 'Aprobada', 'combustible3.pdf', 55000),
    ('Repuestos', '88888888888', 'Rechazada', 'reparacion3.pdf', 180000),
    ('Vulcanizacion', '99999999999', 'Pendiente', 'mantenimiento3.pdf', 25000),
    ('Otros', '10101010101', 'Aprobada', 'combustible4.pdf', 60000);

-- Tabla dominio_vigente
INSERT INTO proyecto_semestral.dominio_vigente (fecha_emision, PDF_dominio_vigente) VALUES
    ('2023-01-15', 'dominio1.pdf'),
    ('2023-02-20', 'dominio2.pdf'),
    ('2023-03-25', 'dominio3.pdf'),
    ('2023-04-30', 'dominio4.pdf'),
    ('2023-05-05', 'dominio5.pdf'),
    ('2023-06-10', 'dominio6.pdf'),
    ('2023-07-15', 'dominio7.pdf'),
    ('2023-08-20', 'dominio8.pdf'),
    ('2023-09-25', 'dominio9.pdf'),
    ('2023-10-30', 'dominio10.pdf');

-- Tabla revision_tecnica
INSERT INTO proyecto_semestral.revision_tecnica (PDF_revision_tecnica, fecha_ven_rev_tecnica) VALUES
    ('rev_tecnica1.pdf', '2025-06-01'),
    ('rev_tecnica2.pdf', '2025-06-15'),
    ('rev_tecnica3.pdf', '2025-07-01'),
    ('rev_tecnica4.pdf', '2025-07-15'),
    ('rev_tecnica5.pdf', '2025-08-01'),
    ('rev_tecnica6.pdf', '2025-08-15'),
    ('rev_tecnica7.pdf', '2025-09-01'),
    ('rev_tecnica8.pdf', '2025-09-15'),
    ('rev_tecnica9.pdf', '2025-10-01'),
    ('rev_tecnica10.pdf', '2025-10-15');

-- Tabla vehiculo
INSERT INTO proyecto_semestral.vehiculo (patente, marca, modelo, año, ID_revision, Pdf_permiso_circulacion, pdf_SOAP, pdf_contrato_gps, id_dominio_vigente, tipo_vehiculo, RUT_empresa) VALUES
    ('ABCD12', 'Toyota', 'Hilux', 2010, 1, 'permiso1.pdf', 'SOAP1.pdf', TRUE, 1, 'Camioneta', '12345678901'),
    ('EFGH34', 'Nissan', 'Navara', 2011, 2, 'permiso2.pdf', 'SOAP2.pdf', TRUE, 2, 'Camioneta', '23456789012'),
    ('IJKL56', 'Chevrolet', 'Luv', 2012, 3, 'permiso3.pdf', 'SOAP3.pdf', TRUE, 3, 'Camioneta', '34567890123'),
    ('MNOP78', 'Ford', 'Ranger', 2013, 4, 'permiso4.pdf', 'SOAP4.pdf', TRUE, 4, 'Camioneta', '45678901234'),
    ('QRST90', 'Mitsubishi', 'L200', 2014, 5, 'permiso5.pdf', 'SOAP5.pdf', TRUE, 5, 'Camioneta', '56789012345'),
    ('UVWX12', 'Toyota', 'Hilux', 2015, 6, 'permiso6.pdf', 'SOAP6.pdf', TRUE, 6, 'Camioneta', '67890123456'),
    ('YZAB34', 'Nissan', 'Navara', 2016, 7, 'permiso7.pdf', 'SOAP7.pdf', TRUE, 7, 'Camioneta', '78901234567'),
    ('CDEF56', 'Chevrolet', 'Luv', 2017, 8, 'permiso8.pdf', 'SOAP8.pdf', TRUE, 8, 'Camioneta', '89012345678'),
    ('GHIJ78', 'Ford', 'Ranger', 2018, 9, 'permiso9.pdf', 'SOAP9.pdf', TRUE, 9, 'Camioneta', '90123456789'),
    ('KLMN90', 'Mitsubishi', 'L200', 2019, 10, 'permiso10.pdf', 'SOAP10.pdf', TRUE, 10, 'Camioneta', '01234567890');

-- Tabla estanque
INSERT INTO proyecto_semestral.estanque (material, capacidad) VALUES
    ('Acero', '1000L'),
    ('Fibra', '2000L'),
    ('Acero', '3000L'),
    ('Fibra', '4000L'),
    ('Acero', '5000L'),
    ('Fibra', '1000L'),
    ('Acero', '2000L'),
    ('Fibra', '3000L'),
    ('Acero', '4000L'),
    ('Fibra', '5000L');

-- Tabla ruta
INSERT INTO proyecto_semestral.ruta (nombre, comuna) VALUES
    ('Ruta 1', 'Comuna A'),
    ('Ruta 2', 'Comuna B'),
    ('Ruta 3', 'Comuna C'),
    ('Ruta 4', 'Comuna D'),
    ('Ruta 5', 'Comuna E'),
    ('Ruta 6', 'Comuna F'),
    ('Ruta 7', 'Comuna G'),
    ('Ruta 8', 'Comuna H'),
    ('Ruta 9', 'Comuna I'),
    ('Ruta 10', 'Comuna J');

-- Tabla licencia
INSERT INTO proyecto_semestral.licencia (pdf_licencia, fecha_ven_licencia, tipo_licencia) VALUES
    ('licencia1.pdf', '2024-06-01', 'A1'),
    ('licencia2.pdf', '2024-06-15', 'A2'),
    ('licencia3.pdf', '2024-07-01', 'A3'),
    ('licencia4.pdf', '2024-07-15', 'B'),
    ('licencia5.pdf', '2024-08-01', 'B'),
    ('licencia6.pdf', '2024-08-15', 'A5'),
    ('licencia7.pdf', '2024-09-01', 'A3'),
    ('licencia8.pdf', '2024-09-15', 'A1'),
    ('licencia9.pdf', '2024-10-01', 'B'),
    ('licencia10.pdf', '2024-10-15', 'A1');

-- Tabla carnet
INSERT INTO proyecto_semestral.carnet (pdf_carnet, fecha_ven_carnet) VALUES
    ('carnet1.pdf', '2024-06-01'),
    ('carnet2.pdf', '2024-06-15'),
    ('carnet3.pdf', '2024-07-01'),
    ('carnet4.pdf', '2024-07-15'),
    ('carnet5.pdf', '2024-08-01'),
    ('carnet6.pdf', '2024-08-15'),
    ('carnet7.pdf', '2024-09-01'),
    ('carnet8.pdf', '2024-09-15'),
    ('carnet9.pdf', '2024-10-01'),
    ('carnet10.pdf', '2024-10-15');

-- Tabla conductor
INSERT INTO proyecto_semestral.conductor (RUT_conductor, id_carnet, id_licencia, certificado_DS41) VALUES
    ('11111111111', 1, 1, TRUE),
    ('22222222222', 2, 2, FALSE),
    ('33333333333', 3, 3, TRUE),
    ('44444444444', 4, 4, FALSE),
    ('55555555555', 5, 5, TRUE),
    ('66666666666', 6, 6, FALSE),
    ('77777777777', 7, 7, TRUE),
    ('88888888888', 8, 8, FALSE),
    ('99999999999', 9, 9, TRUE),
    ('10101010101', 10, 10, FALSE);

-- Tabla cambio
INSERT INTO proyecto_semestral.cambio (fecha_cambio, motivo_cambio, autor_cambio) VALUES
    ('2023-01-01', 'Cambio de ruta', 'Admin1'),
    ('2023-02-01', 'Cambio de ruta', 'Admin2'),
    ('2023-03-01', 'Cambio de ruta', 'Admin3'),
    ('2023-04-01', 'Cambio de ruta', 'Admin4'),
    ('2023-05-01', 'Cambio de ruta', 'Admin5'),
    ('2023-06-01', 'Cambio de ruta', 'Admin6'),
    ('2023-07-01', 'Cambio de ruta', 'Admin7'),
    ('2023-08-01', 'Cambio de ruta', 'Admin8'),
    ('2023-09-01', 'Cambio de ruta', 'Admin9'),
    ('2023-10-01', 'Cambio de ruta', 'Admin10');

-- Tabla conductor_en_vehiculo
INSERT INTO proyecto_semestral.conductor_en_vehiculo (RUT_conductor, patente, fecha_inicio, fecha_termino, id_cambio) VALUES
    ('11111111111', 'ABCD12', '2023-01-01', '2023-02-01', 1),
    ('22222222222', 'EFGH34', '2023-02-01', '2023-03-01', 2),
    ('33333333333', 'IJKL56', '2023-03-01', '2023-04-01', 3),
    ('44444444444', 'MNOP78', '2023-04-01', '2023-05-01', 4),
    ('55555555555', 'QRST90', '2023-05-01', '2023-06-01', 5),
    ('66666666666', 'UVWX12', '2023-06-01', '2023-07-01', 6),
    ('77777777777', 'YZAB34', '2023-07-01', '2023-08-01', 7),
    ('88888888888', 'CDEF56', '2023-08-01', '2023-09-01', 8),
    ('99999999999', 'GHIJ78', '2023-09-01', '2023-10-01', 9),
    ('10101010101', 'KLMN90', '2023-10-01', '2023-11-01', 10);

--Conductor que no ha cambiado de vehiculo
INSERT INTO proyecto_semestral.conductor_en_vehiculo (RUT_conductor, patente, fecha_inicio) VALUES
    ('11111111111', 'ABCD12', '2024-01-01'),
    ('22222222222', 'EFGH34', '2024-01-01'),
    ('33333333333', 'IJKL56', '2024-01-01'),
    ('44444444444', 'MNOP78', '2024-01-01'),
    ('55555555555', 'QRST90', '2024-01-01'),
    ('66666666666', 'UVWX12', '2024-01-01'),
    ('77777777777', 'YZAB34', '2024-01-01'),
    ('88888888888', 'CDEF56', '2024-01-01'),
    ('99999999999', 'GHIJ78', '2024-01-01'),
    ('10101010101', 'KLMN90', '2024-01-01');
    

--Tabla conductor_en_ruta en fechas anteriores
INSERT INTO proyecto_semestral.recorrido (RUT_conductor, patente, nombre_ruta, fecha, id_estanque) VALUES
    ('11111111111', 'ABCD12', 'Ruta 1','2023-02-01',1),
    ('22222222222', 'EFGH34', 'Ruta 2','2023-02-04',2),
    ('33333333333', 'MNOP78', 'Ruta 3','2023-02-03',3),
    ('44444444444', 'IJKL56', 'Ruta 4','2023-02-02',4);

--Tabla conductor_en_ruta en fechas actuales
INSERT INTO proyecto_semestral.recorrido (RUT_conductor, patente, nombre_ruta, fecha, id_estanque) VALUES
    ('55555555555', 'QRST90', 'Ruta 5', CURRENT_DATE,5),
    ('66666666666', 'UVWX12', 'Ruta 6', CURRENT_DATE,6),
    ('77777777777', 'YZAB34', 'Ruta 7', CURRENT_DATE,7),
    ('88888888888', 'CDEF56', 'Ruta 8', CURRENT_DATE,8),
    ('99999999999', 'GHIJ78', 'Ruta 9', CURRENT_DATE,9),
    ('10101010101', 'KLMN90', 'Ruta 10', CURRENT_DATE,10);

-- Tabla contrato_por_turno
INSERT INTO proyecto_semestral.contrato_por_turno (ID, turno, tipo_turno, PDF_permiso_inspeccion) VALUES
    (1, 'Diurno', 'Ordinario', 'inspeccion1.pdf'),
    (2, 'Nocturno', 'Extraordinario', 'inspeccion2.pdf'),
    (3, 'Diurno', 'Ordinario', 'inspeccion3.pdf'),
    (4, 'Nocturno', 'Extraordinario', 'inspeccion4.pdf'),
    (5, 'Diurno', 'Ordinario', 'inspeccion5.pdf'),
    (6, 'Nocturno', 'Extraordinario', 'inspeccion6.pdf'),
    (7, 'Diurno', 'Ordinario', 'inspeccion7.pdf'),
    (8, 'Nocturno', 'Extraordinario', 'inspeccion8.pdf'),
    (9, 'Diurno', 'Ordinario', 'inspeccion9.pdf'),
    (10, 'Nocturno', 'Extraordinario', 'inspeccion10.pdf');

-- Tabla contrato_por_faena
INSERT INTO proyecto_semestral.contrato_por_faena (ID, fecha_termino) VALUES
    (1, '2024-01-01'),
    (2, '2024-02-01'),
    (3, '2024-03-01'),
    (4, '2024-04-01'),
    (5, '2024-05-01'),
    (6, '2024-06-01'),
    (7, '2024-07-01'),
    (8, '2024-08-01'),
    (9, '2024-09-01'),
    (10, '2024-10-01');

-- Tabla contrato_por_plazo_fijo
INSERT INTO proyecto_semestral.contrato_por_plazo_fijo (ID, fecha_termino) VALUES
    (1, '2024-01-01'),
    (2, '2024-02-01'),
    (3, '2024-03-01'),
    (4, '2024-04-01'),
    (5, '2024-05-01'),
    (6, '2024-06-01'),
    (7, '2024-07-01'),
    (8, '2024-08-01'),
    (9, '2024-09-01'),
    (10, '2024-10-01');

--nombre y apellido del conductor, la patente del vehículo, la capacidad del estanque y el nombre de la ruta
SELECT 
    re.patente AS patente_vehiculo,
    e.nombres_empleado AS nombre_conductor,
    e.apellido1_empleado AS apellido_paterno,
    e.apellido2_empleado AS apellido_materno,
    es.capacidad AS capacidad_estanque,
    r.nombre AS nombre_ruta,
    re.fecha AS fecha
FROM 
    proyecto_semestral.recorrido re
JOIN 
    proyecto_semestral.conductor c ON re.rut_conductor = c.rut_conductor
JOIN 
    proyecto_semestral.empleado e ON c.rut_conductor = e.rut_empleado
JOIN 
    proyecto_semestral.vehiculo v ON re.patente = v.patente
JOIN 
    proyecto_semestral.ruta r ON re.nombre_ruta = r.nombre
JOIN 
    proyecto_semestral.estanque es ON re.id_estanque = es.id
WHERE 
    re.fecha = CURRENT_DATE;


-- Datos sobre rendiciones pendientes
SELECT 
    r.Id,
    r.rut_empleado,
    r.Tipo_rendicion,
    r.Estado,
    r.PDF_doc_asociado,
    r.Monto
FROM 
    proyecto_semestral.rendicion r
WHERE 
    Estado = 'Pendiente';

-- Conductores con el certificado DS41
SELECT c.rut_conductor AS rut,
    e.nombres_empleado AS nombre,
    e.apellido1_empleado AS apellido_materno,
    e.apellido2_empleado AS apellido_paterno
FROM proyecto_semestral.conductor C
JOIN proyecto_semestral.empleado E ON e.rut_empleado = c.rut_conductor
WHERE c.certificado_ds41 = TRUE