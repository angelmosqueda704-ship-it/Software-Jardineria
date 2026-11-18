-- Datos FICTICIOS de prueba (no corresponden a personas ni empresas reales)
INSERT INTO empleado (id_empleado, id_cuadrilla, nombre_completo, puesto, area, rfc, nss, telefono, fecha_ingreso, salario_base, activo) VALUES
 (1, NULL, 'Laura Méndez Ortega',   'Gerente General',        'administración', 'MEOL800101AB1', '12345678901', '4491000001', '2019-03-01', 28000, TRUE),
 (2, NULL, 'Ricardo Salas Vega',    'Ejecutivo de ventas',    'administración', 'SAVR850505CD2', '12345678902', '4491000002', '2020-06-15', 14000, TRUE),
 (3, NULL, 'Patricia Núñez Ibarra', 'Directora Financiera',   'finanzas',       'NUIP820909EF3', '12345678903', '4491000003', '2018-01-10', 32000, TRUE),
 (4, NULL, 'Jorge Castañeda Ruiz',  'Jefe de cuadrilla',      'campo',          'CARJ880303GH4', '12345678904', '4491000004', '2021-02-01', 12000, TRUE),
 (5, NULL, 'Miguel Torres Lara',    'Jardinero',              'campo',          'TOLM900707IJ5', '12345678905', '4491000005', '2022-04-18',  9000, TRUE),
 (6, NULL, 'Sofía Herrera Pons',    'Inspectora de calidad',  'calidad',        'HEPS920202KL6', '12345678906', '4491000006', '2022-09-05', 13000, TRUE),
 (7, NULL, 'Andrés Cortés Valle',   'Jefe de cuadrilla',      'campo',          'COVA870808MN7', '12345678907', '4491000007', '2020-11-20', 12000, TRUE);

INSERT INTO cuadrilla (id_cuadrilla, id_responsable, nombre, especialidad, estado) VALUES
 (1, 4, 'Cuadrilla Alfa', 'Paisajismo',    'asignada'),
 (2, 7, 'Cuadrilla Beta', 'Mantenimiento', 'disponible');
UPDATE empleado SET id_cuadrilla = 1 WHERE id_empleado IN (4, 5);
UPDATE empleado SET id_cuadrilla = 2 WHERE id_empleado = 7;

INSERT INTO cliente (id_cliente, nombre, tipo_cliente, rfc, telefono, correo, direccion) VALUES
 (1, 'Residencial Los Encinos (ficticio)', 'empresa',    'REN010101AA1', '4492000001', 'admin@encinos.example',  'Av. de las Flores 120, Aguascalientes'),
 (2, 'Familia Domínguez Rojas',            'particular', 'DORF750101BB2', '4492000002', 'dominguez@example.com', 'Calle Naranjos 45, Aguascalientes'),
 (3, 'Municipio Demo (ficticio)',          'gobierno',   'MDE000101CC3', '4492000003', 'obras@municipio.example', 'Plaza Principal s/n'),
 (4, 'Hotel Jardín del Sol (ficticio)',    'empresa',    'HJS050505DD4', '4492000004', 'compras@hjs.example',    'Blvd. Zacatecas 800');

INSERT INTO servicio (id_servicio, nombre, categoria, descripcion, unidad, precio_unitario) VALUES
 (1, 'Mantenimiento de jardín',      'mantenimiento', 'Poda, riego y limpieza general',        'm2',    18.50),
 (2, 'Diseño de paisajismo',         'paisajismo',    'Proyecto y plantación de áreas verdes',  'm2',   145.00),
 (3, 'Instalación de riego',         'obra',          'Sistema de riego por aspersión/goteo',   'm2',    95.00),
 (4, 'Estudio de suelo',             'estudio',       'Análisis técnico de suelo y drenaje',    'pieza', 6500.00),
 (5, 'Obra de cisterna',             'obra',          'Construcción de cisterna de captación',  'pieza', 48000.00);

INSERT INTO cotizacion (id_cotizacion, id_cliente, id_empleado_elabora, id_aprobador, fecha_emision, monto_total, estado, requiere_revision) VALUES
 (1, 1, 2, 3,    '2026-09-10', 72500.00, 'aprobada',  TRUE),
 (2, 2, 2, NULL, '2026-10-02',  9250.00, 'pendiente', FALSE),
 (3, 3, 2, NULL, '2026-10-15', 96000.00, 'pendiente', TRUE),
 (4, 4, 2, 1,    '2026-09-25',  3700.00, 'rechazada', FALSE);

INSERT INTO detalle_cotizacion (id_cotizacion, id_servicio, cantidad, precio_pactado, subtotal) VALUES
 (1, 2, 400, 145.00, 58000.00),
 (1, 3, 152.63, 95.00, 14500.00),
 (2, 1, 500, 18.50, 9250.00),
 (3, 5, 2, 48000.00, 96000.00),
 (4, 1, 200, 18.50, 3700.00);

INSERT INTO obra (id_obra, id_cotizacion, nombre_obra, tipo_servicio, direccion_obra, fecha_inicio, fecha_fin_estimada, estado, porcentaje_avance) VALUES
 (1, 1, 'Áreas verdes Residencial Los Encinos', 'paisajismo', 'Av. de las Flores 120', '2026-09-20', '2026-11-30', 'en curso', 45.00);

INSERT INTO asignacion_obra (id_asignacion, id_obra, id_cuadrilla, fecha_inicio, fecha_fin) VALUES
 (1, 1, 1, '2026-09-20', NULL);

INSERT INTO reporte_avance (id_reporte, id_obra, id_empleado, fecha_reporte, porcentaje_reportado, descripcion, evidencia_url) VALUES
 (1, 1, 4, '2026-10-05 17:30', 30.00, 'Se terminó la preparación del terreno y la nivelación.', 'recursos/ejemplo1.jpg'),
 (2, 1, 4, '2026-10-19 17:45', 45.00, 'Plantación de césped en el 45 % del área.', 'recursos/ejemplo2.jpg');

INSERT INTO proveedor (id_proveedor, razon_social, rfc, contacto, telefono, correo) VALUES
 (1, 'Viveros Demo S.A. (ficticio)', 'VDE010101EE5', 'Carlos Pérez', '4493000001', 'ventas@viveros.example');
INSERT INTO material (id_material, id_proveedor, nombre, unidad, costo_unitario, stock_actual) VALUES
 (1, 1, 'Césped en rollo', 'm2', 38.00, 600),
 (2, 1, 'Tierra negra', 'm3', 420.00, 40);
INSERT INTO consumo_material (id_consumo, id_obra, id_material, cantidad, fecha_uso) VALUES
 (1, 1, 1, 180, '2026-10-19'),
 (2, 1, 2, 12,  '2026-10-05');

INSERT INTO factura (id_factura, id_obra, folio_cfdi, uuid_sat, fecha_emision, subtotal, iva, total, estado_pago) VALUES
 (1, 1, 'A-0001', '00000000-0000-0000-0000-000000000001', '2026-09-22', 31250.00, 5000.00, 36250.00, 'pagada');
INSERT INTO nomina (id_nomina, id_empleado, periodo_inicio, periodo_fin, sueldo_bruto, deducciones, sueldo_neto, fecha_pago) VALUES
 (1, 4, '2026-10-01', '2026-10-15', 6000.00, 780.00, 5220.00, '2026-10-15');
INSERT INTO transaccion (id_transaccion, id_factura, id_nomina, id_proveedor, id_obra, tipo, concepto, monto, fecha) VALUES
 (1, 1, NULL, NULL, 1, 'ingreso', 'Anticipo 50 % factura A-0001', 36250.00, '2026-09-25'),
 (2, NULL, 1, NULL, 1, 'egreso',  'Nómina quincenal J. Castañeda', 5220.00, '2026-10-15');

INSERT INTO inspeccion (id_inspeccion, id_obra, id_inspector, fecha, tipo, resultado, observaciones) VALUES
 (1, 1, 6, '2026-10-10', 'seguridad', 'con observaciones', 'Falta señalización en zona de excavación.');
INSERT INTO incidente (id_incidente, id_obra, id_inspeccion, id_empleado, fecha, gravedad, descripcion, accion_correctiva, estado) VALUES
 (1, 1, 1, 5, '2026-10-09 11:20', 'leve', 'Corte menor con herramienta de poda.', 'Uso obligatorio de guantes; capacitación breve.', 'cerrado');

-- Reinicia las secuencias SERIAL para continuar después de los datos de prueba
SELECT setval(pg_get_serial_sequence('cliente','id_cliente'), (SELECT MAX(id_cliente) FROM cliente));
SELECT setval(pg_get_serial_sequence('cotizacion','id_cotizacion'), (SELECT MAX(id_cotizacion) FROM cotizacion));
SELECT setval(pg_get_serial_sequence('servicio','id_servicio'), (SELECT MAX(id_servicio) FROM servicio));
SELECT setval(pg_get_serial_sequence('obra','id_obra'), (SELECT MAX(id_obra) FROM obra));
SELECT setval(pg_get_serial_sequence('cuadrilla','id_cuadrilla'), (SELECT MAX(id_cuadrilla) FROM cuadrilla));
SELECT setval(pg_get_serial_sequence('empleado','id_empleado'), (SELECT MAX(id_empleado) FROM empleado));
SELECT setval(pg_get_serial_sequence('asignacion_obra','id_asignacion'), (SELECT MAX(id_asignacion) FROM asignacion_obra));
SELECT setval(pg_get_serial_sequence('reporte_avance','id_reporte'), (SELECT MAX(id_reporte) FROM reporte_avance));
SELECT setval(pg_get_serial_sequence('proveedor','id_proveedor'), (SELECT MAX(id_proveedor) FROM proveedor));
SELECT setval(pg_get_serial_sequence('material','id_material'), (SELECT MAX(id_material) FROM material));
SELECT setval(pg_get_serial_sequence('consumo_material','id_consumo'), (SELECT MAX(id_consumo) FROM consumo_material));
SELECT setval(pg_get_serial_sequence('nomina','id_nomina'), (SELECT MAX(id_nomina) FROM nomina));
SELECT setval(pg_get_serial_sequence('factura','id_factura'), (SELECT MAX(id_factura) FROM factura));
SELECT setval(pg_get_serial_sequence('transaccion','id_transaccion'), (SELECT MAX(id_transaccion) FROM transaccion));
SELECT setval(pg_get_serial_sequence('inspeccion','id_inspeccion'), (SELECT MAX(id_inspeccion) FROM inspeccion));
SELECT setval(pg_get_serial_sequence('incidente','id_incidente'), (SELECT MAX(id_incidente) FROM incidente));
