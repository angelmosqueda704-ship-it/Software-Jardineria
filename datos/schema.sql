-- Esquema PostgreSQL generado desde el Diagrama Entidad-Relación (18 entidades)
-- Sistema Integral de Gestión — Agua y Jardín

CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    tipo_cliente VARCHAR(20) NOT NULL,
    rfc VARCHAR(13) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL
);

CREATE TABLE cotizacion (
    id_cotizacion SERIAL PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_empleado_elabora INT NOT NULL,
    id_aprobador INT,
    fecha_emision DATE NOT NULL,
    monto_total NUMERIC(12,2) NOT NULL,
    estado VARCHAR(15) NOT NULL,
    requiere_revision BOOLEAN NOT NULL
);

CREATE TABLE servicio (
    id_servicio SERIAL PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL,
    categoria VARCHAR(30) NOT NULL,
    descripcion VARCHAR(200) NOT NULL,
    unidad VARCHAR(15) NOT NULL,
    precio_unitario NUMERIC(10,2) NOT NULL
);

CREATE TABLE detalle_cotizacion (
    id_cotizacion INT NOT NULL,
    id_servicio INT NOT NULL,
    cantidad NUMERIC(10,2) NOT NULL,
    precio_pactado NUMERIC(10,2) NOT NULL,
    subtotal NUMERIC(12,2) NOT NULL,
    PRIMARY KEY (id_cotizacion, id_servicio)
);

CREATE TABLE obra (
    id_obra SERIAL PRIMARY KEY,
    id_cotizacion INT NOT NULL UNIQUE,
    nombre_obra VARCHAR(100) NOT NULL,
    tipo_servicio VARCHAR(30) NOT NULL,
    direccion_obra VARCHAR(200) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin_estimada DATE NOT NULL,
    estado VARCHAR(20) NOT NULL,
    porcentaje_avance NUMERIC(5,2) NOT NULL
);

CREATE TABLE cuadrilla (
    id_cuadrilla SERIAL PRIMARY KEY,
    id_responsable INT NOT NULL UNIQUE,
    nombre VARCHAR(60) NOT NULL,
    especialidad VARCHAR(40) NOT NULL,
    estado VARCHAR(15) NOT NULL
);

CREATE TABLE empleado (
    id_empleado SERIAL PRIMARY KEY,
    id_cuadrilla INT,
    nombre_completo VARCHAR(120) NOT NULL,
    puesto VARCHAR(60) NOT NULL,
    area VARCHAR(40) NOT NULL,
    rfc VARCHAR(13) NOT NULL,
    nss VARCHAR(11) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    fecha_ingreso DATE NOT NULL,
    salario_base NUMERIC(10,2) NOT NULL,
    activo BOOLEAN NOT NULL
);

CREATE TABLE asignacion_obra (
    id_asignacion SERIAL PRIMARY KEY,
    id_obra INT NOT NULL,
    id_cuadrilla INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE
);

CREATE TABLE reporte_avance (
    id_reporte SERIAL PRIMARY KEY,
    id_obra INT NOT NULL,
    id_empleado INT NOT NULL,
    fecha_reporte TIMESTAMP NOT NULL,
    porcentaje_reportado NUMERIC(5,2) NOT NULL,
    descripcion VARCHAR(300) NOT NULL,
    evidencia_url VARCHAR(255) NOT NULL
);

CREATE TABLE proveedor (
    id_proveedor SERIAL PRIMARY KEY,
    razon_social VARCHAR(120) NOT NULL,
    rfc VARCHAR(13) NOT NULL,
    contacto VARCHAR(80) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    correo VARCHAR(100) NOT NULL
);

CREATE TABLE material (
    id_material SERIAL PRIMARY KEY,
    id_proveedor INT NOT NULL,
    nombre VARCHAR(80) NOT NULL,
    unidad VARCHAR(15) NOT NULL,
    costo_unitario NUMERIC(10,2) NOT NULL,
    stock_actual NUMERIC(10,2) NOT NULL
);

CREATE TABLE consumo_material (
    id_consumo SERIAL PRIMARY KEY,
    id_obra INT NOT NULL,
    id_material INT NOT NULL,
    cantidad NUMERIC(10,2) NOT NULL,
    fecha_uso DATE NOT NULL
);

CREATE TABLE nomina (
    id_nomina SERIAL PRIMARY KEY,
    id_empleado INT NOT NULL,
    periodo_inicio DATE NOT NULL,
    periodo_fin DATE NOT NULL,
    sueldo_bruto NUMERIC(10,2) NOT NULL,
    deducciones NUMERIC(10,2) NOT NULL,
    sueldo_neto NUMERIC(10,2) NOT NULL,
    fecha_pago DATE NOT NULL
);

CREATE TABLE factura (
    id_factura SERIAL PRIMARY KEY,
    id_obra INT NOT NULL,
    folio_cfdi VARCHAR(40) NOT NULL UNIQUE,
    uuid_sat VARCHAR(36) NOT NULL,
    fecha_emision DATE NOT NULL,
    subtotal NUMERIC(12,2) NOT NULL,
    iva NUMERIC(12,2) NOT NULL,
    total NUMERIC(12,2) NOT NULL,
    estado_pago VARCHAR(15) NOT NULL
);

CREATE TABLE transaccion (
    id_transaccion SERIAL PRIMARY KEY,
    id_factura INT,
    id_nomina INT,
    id_proveedor INT,
    id_obra INT,
    tipo VARCHAR(10) NOT NULL,
    concepto VARCHAR(120) NOT NULL,
    monto NUMERIC(12,2) NOT NULL,
    fecha DATE NOT NULL
);

CREATE TABLE inspeccion (
    id_inspeccion SERIAL PRIMARY KEY,
    id_obra INT NOT NULL,
    id_inspector INT NOT NULL,
    fecha DATE NOT NULL,
    tipo VARCHAR(15) NOT NULL,
    resultado VARCHAR(20) NOT NULL,
    observaciones VARCHAR(300) NOT NULL
);

CREATE TABLE incidente (
    id_incidente SERIAL PRIMARY KEY,
    id_obra INT NOT NULL,
    id_inspeccion INT,
    id_empleado INT,
    fecha TIMESTAMP NOT NULL,
    gravedad VARCHAR(10) NOT NULL,
    descripcion VARCHAR(300) NOT NULL,
    accion_correctiva VARCHAR(300) NOT NULL,
    estado VARCHAR(15) NOT NULL
);

CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,
    id_empleado INT NOT NULL UNIQUE,
    correo VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(30) NOT NULL,
    activo BOOLEAN NOT NULL
);

-- Llaves foráneas (después de crear las tablas: hay referencias circulares empleado/cuadrilla)
ALTER TABLE cotizacion ADD CONSTRAINT fk_cotizacion_id_cliente FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente);
ALTER TABLE cotizacion ADD CONSTRAINT fk_cotizacion_id_empleado_elabora FOREIGN KEY (id_empleado_elabora) REFERENCES empleado(id_empleado);
ALTER TABLE cotizacion ADD CONSTRAINT fk_cotizacion_id_aprobador FOREIGN KEY (id_aprobador) REFERENCES empleado(id_empleado);
ALTER TABLE detalle_cotizacion ADD CONSTRAINT fk_detalle_cotizacion_id_cotizacion FOREIGN KEY (id_cotizacion) REFERENCES cotizacion(id_cotizacion);
ALTER TABLE detalle_cotizacion ADD CONSTRAINT fk_detalle_cotizacion_id_servicio FOREIGN KEY (id_servicio) REFERENCES servicio(id_servicio);
ALTER TABLE obra ADD CONSTRAINT fk_obra_id_cotizacion FOREIGN KEY (id_cotizacion) REFERENCES cotizacion(id_cotizacion);
ALTER TABLE cuadrilla ADD CONSTRAINT fk_cuadrilla_id_responsable FOREIGN KEY (id_responsable) REFERENCES empleado(id_empleado);
ALTER TABLE empleado ADD CONSTRAINT fk_empleado_id_cuadrilla FOREIGN KEY (id_cuadrilla) REFERENCES cuadrilla(id_cuadrilla);
ALTER TABLE asignacion_obra ADD CONSTRAINT fk_asignacion_obra_id_obra FOREIGN KEY (id_obra) REFERENCES obra(id_obra);
ALTER TABLE asignacion_obra ADD CONSTRAINT fk_asignacion_obra_id_cuadrilla FOREIGN KEY (id_cuadrilla) REFERENCES cuadrilla(id_cuadrilla);
ALTER TABLE reporte_avance ADD CONSTRAINT fk_reporte_avance_id_obra FOREIGN KEY (id_obra) REFERENCES obra(id_obra);
ALTER TABLE reporte_avance ADD CONSTRAINT fk_reporte_avance_id_empleado FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado);
ALTER TABLE material ADD CONSTRAINT fk_material_id_proveedor FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor);
ALTER TABLE consumo_material ADD CONSTRAINT fk_consumo_material_id_obra FOREIGN KEY (id_obra) REFERENCES obra(id_obra);
ALTER TABLE consumo_material ADD CONSTRAINT fk_consumo_material_id_material FOREIGN KEY (id_material) REFERENCES material(id_material);
ALTER TABLE nomina ADD CONSTRAINT fk_nomina_id_empleado FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado);
ALTER TABLE factura ADD CONSTRAINT fk_factura_id_obra FOREIGN KEY (id_obra) REFERENCES obra(id_obra);
ALTER TABLE transaccion ADD CONSTRAINT fk_transaccion_id_factura FOREIGN KEY (id_factura) REFERENCES factura(id_factura);
ALTER TABLE transaccion ADD CONSTRAINT fk_transaccion_id_nomina FOREIGN KEY (id_nomina) REFERENCES nomina(id_nomina);
ALTER TABLE transaccion ADD CONSTRAINT fk_transaccion_id_proveedor FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor);
ALTER TABLE transaccion ADD CONSTRAINT fk_transaccion_id_obra FOREIGN KEY (id_obra) REFERENCES obra(id_obra);
ALTER TABLE inspeccion ADD CONSTRAINT fk_inspeccion_id_obra FOREIGN KEY (id_obra) REFERENCES obra(id_obra);
ALTER TABLE inspeccion ADD CONSTRAINT fk_inspeccion_id_inspector FOREIGN KEY (id_inspector) REFERENCES empleado(id_empleado);
ALTER TABLE incidente ADD CONSTRAINT fk_incidente_id_obra FOREIGN KEY (id_obra) REFERENCES obra(id_obra);
ALTER TABLE incidente ADD CONSTRAINT fk_incidente_id_inspeccion FOREIGN KEY (id_inspeccion) REFERENCES inspeccion(id_inspeccion);
ALTER TABLE incidente ADD CONSTRAINT fk_incidente_id_empleado FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado);
ALTER TABLE usuario ADD CONSTRAINT fk_usuario_id_empleado FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado);

CREATE INDEX idx_cotizacion_estado ON cotizacion(estado);
CREATE INDEX idx_obra_estado ON obra(estado);
