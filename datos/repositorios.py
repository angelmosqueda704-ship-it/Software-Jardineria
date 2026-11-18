"""Consultas SQL (capa de datos). Siempre con parámetros %s para evitar inyección SQL."""
from datos.conexion import cursor


# ---------- Usuarios ----------
def usuario_por_correo(correo):
    with cursor() as cur:
        cur.execute(
            """SELECT u.id_usuario, u.correo, u.password_hash, u.rol, u.activo, e.nombre_completo
               FROM usuario u JOIN empleado e ON e.id_empleado = u.id_empleado
               WHERE u.correo = %s""", (correo,))
        return cur.fetchone()


# ---------- Resumen ----------
def resumen():
    with cursor() as cur:
        cur.execute("""SELECT
            (SELECT COUNT(*) FROM cliente) AS clientes,
            (SELECT COUNT(*) FROM cotizacion WHERE estado='pendiente') AS cot_pendientes,
            (SELECT COUNT(*) FROM obra WHERE estado='en curso') AS obras_en_curso,
            (SELECT COUNT(*) FROM cuadrilla WHERE estado='disponible') AS cuadrillas_libres,
            (SELECT COALESCE(SUM(monto_total),0) FROM cotizacion WHERE estado='aprobada') AS monto_aprobado""")
        return cur.fetchone()


# ---------- Clientes (CRUD) ----------
def listar_clientes(buscar=""):
    with cursor() as cur:
        cur.execute("SELECT * FROM cliente WHERE nombre ILIKE %s OR rfc ILIKE %s ORDER BY nombre",
                    (f"%{buscar}%", f"%{buscar}%"))
        return cur.fetchall()


def obtener_cliente(id_cliente):
    with cursor() as cur:
        cur.execute("SELECT * FROM cliente WHERE id_cliente=%s", (id_cliente,))
        return cur.fetchone()


def crear_cliente(d):
    with cursor() as cur:
        cur.execute("""INSERT INTO cliente (nombre,tipo_cliente,rfc,telefono,correo,direccion)
                       VALUES (%(nombre)s,%(tipo_cliente)s,%(rfc)s,%(telefono)s,%(correo)s,%(direccion)s)
                       RETURNING id_cliente""", d)
        return cur.fetchone()["id_cliente"]


def actualizar_cliente(id_cliente, d):
    with cursor() as cur:
        cur.execute("""UPDATE cliente SET nombre=%(nombre)s,tipo_cliente=%(tipo_cliente)s,rfc=%(rfc)s,
                       telefono=%(telefono)s,correo=%(correo)s,direccion=%(direccion)s
                       WHERE id_cliente=%(id)s""", {**d, "id": id_cliente})


def eliminar_cliente(id_cliente):
    """Devuelve False si el cliente tiene cotizaciones (integridad referencial)."""
    with cursor() as cur:
        cur.execute("SELECT COUNT(*) AS n FROM cotizacion WHERE id_cliente=%s", (id_cliente,))
        if cur.fetchone()["n"]:
            return False
        cur.execute("DELETE FROM cliente WHERE id_cliente=%s", (id_cliente,))
        return True


# ---------- Servicios ----------
def listar_servicios():
    with cursor() as cur:
        cur.execute("SELECT * FROM servicio ORDER BY categoria, nombre")
        return cur.fetchall()


# ---------- Cotizaciones ----------
def listar_cotizaciones(estado=""):
    with cursor() as cur:
        cur.execute("""SELECT c.*, cl.nombre AS cliente FROM cotizacion c
                       JOIN cliente cl ON cl.id_cliente = c.id_cliente
                       WHERE (%s = '' OR c.estado = %s) ORDER BY c.id_cotizacion DESC""", (estado, estado))
        return cur.fetchall()


def obtener_cotizacion(id_cot):
    with cursor() as cur:
        cur.execute("""SELECT c.*, cl.nombre AS cliente, e.nombre_completo AS elabora, a.nombre_completo AS aprobador
                       FROM cotizacion c JOIN cliente cl ON cl.id_cliente=c.id_cliente
                       JOIN empleado e ON e.id_empleado=c.id_empleado_elabora
                       LEFT JOIN empleado a ON a.id_empleado=c.id_aprobador
                       WHERE c.id_cotizacion=%s""", (id_cot,))
        cot = cur.fetchone()
        if cot:
            cur.execute("""SELECT d.*, s.nombre, s.unidad FROM detalle_cotizacion d
                           JOIN servicio s ON s.id_servicio=d.id_servicio WHERE d.id_cotizacion=%s""", (id_cot,))
            cot["detalle"] = cur.fetchall()
        return cot


def crear_cotizacion(id_cliente, id_empleado, lineas, monto, requiere_rev):
    """lineas: lista de dicts {id_servicio, cantidad, precio, subtotal}. Todo en una sola transacción."""
    with cursor() as cur:
        cur.execute("""INSERT INTO cotizacion (id_cliente,id_empleado_elabora,fecha_emision,monto_total,estado,requiere_revision)
                       VALUES (%s,%s,CURRENT_DATE,%s,'pendiente',%s) RETURNING id_cotizacion""",
                    (id_cliente, id_empleado, monto, requiere_rev))
        id_cot = cur.fetchone()["id_cotizacion"]
        for l in lineas:
            cur.execute("""INSERT INTO detalle_cotizacion (id_cotizacion,id_servicio,cantidad,precio_pactado,subtotal)
                           VALUES (%s,%s,%s,%s,%s)""", (id_cot, l["id_servicio"], l["cantidad"], l["precio"], l["subtotal"]))
        return id_cot


def resolver_cotizacion(id_cot, id_aprobador, nuevo_estado):
    with cursor() as cur:
        cur.execute("""UPDATE cotizacion SET estado=%s, id_aprobador=%s
                       WHERE id_cotizacion=%s AND estado='pendiente'""", (nuevo_estado, id_aprobador, id_cot))
        return cur.rowcount == 1


def id_empleado_de_usuario(id_usuario):
    with cursor() as cur:
        cur.execute("SELECT id_empleado FROM usuario WHERE id_usuario=%s", (id_usuario,))
        return cur.fetchone()["id_empleado"]


# ---------- Obras ----------
def listar_obras():
    with cursor() as cur:
        cur.execute("""SELECT o.*, cl.nombre AS cliente, cu.nombre AS cuadrilla
                       FROM obra o JOIN cotizacion c ON c.id_cotizacion=o.id_cotizacion
                       JOIN cliente cl ON cl.id_cliente=c.id_cliente
                       LEFT JOIN asignacion_obra a ON a.id_obra=o.id_obra AND a.fecha_fin IS NULL
                       LEFT JOIN cuadrilla cu ON cu.id_cuadrilla=a.id_cuadrilla
                       ORDER BY o.id_obra DESC""")
        return cur.fetchall()
