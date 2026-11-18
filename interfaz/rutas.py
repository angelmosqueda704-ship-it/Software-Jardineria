"""Capa de interfaz: rutas web. Solo recibe/valida la petición y delega en logica/ y datos/."""
from decimal import Decimal, InvalidOperation
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from datos import repositorios as repo
from logica import reglas
from logica.auth import autenticar, login_requerido, rol_requerido

rutas = Blueprint("rutas", __name__)
CAMPOS_CLIENTE = ("nombre", "tipo_cliente", "rfc", "telefono", "correo", "direccion")


@rutas.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = autenticar(request.form.get("correo", ""), request.form.get("contrasena", ""))
        if u:
            session["usuario"] = {"id": u["id_usuario"], "nombre": u["nombre_completo"], "rol": u["rol"]}
            return redirect(url_for("rutas.inicio"))
        flash("Correo o contraseña incorrectos.", "error")
    return render_template("login.html")


@rutas.route("/salir", methods=["POST"])
def salir():
    session.pop("usuario", None)
    return redirect(url_for("rutas.login"))


@rutas.route("/")
@login_requerido
def inicio():
    return render_template("inicio.html", r=repo.resumen(), pendientes=repo.listar_cotizaciones("pendiente"))


# ---------- Clientes ----------
@rutas.route("/clientes")
@login_requerido
def clientes():
    q = request.args.get("q", "").strip()
    return render_template("clientes.html", clientes=repo.listar_clientes(q), q=q)


@rutas.route("/clientes/nuevo", methods=["GET", "POST"])
@rol_requerido("gerente", "admin")
def cliente_nuevo():
    datos = {c: request.form.get(c, "").strip() for c in CAMPOS_CLIENTE}
    if request.method == "POST":
        errores = reglas.validar_cliente(datos)
        if not errores:
            repo.crear_cliente(datos)
            flash("Cliente registrado correctamente.", "ok")
            return redirect(url_for("rutas.clientes"))
        for e in errores: flash(e, "error")
    return render_template("cliente_form.html", c=datos, titulo="Nuevo cliente")


@rutas.route("/clientes/<int:id_cliente>/editar", methods=["GET", "POST"])
@rol_requerido("gerente", "admin")
def cliente_editar(id_cliente):
    actual = repo.obtener_cliente(id_cliente) or abort(404)
    if request.method == "POST":
        datos = {c: request.form.get(c, "").strip() for c in CAMPOS_CLIENTE}
        errores = reglas.validar_cliente(datos)
        if not errores:
            repo.actualizar_cliente(id_cliente, datos)
            flash("Cliente actualizado.", "ok")
            return redirect(url_for("rutas.clientes"))
        for e in errores: flash(e, "error")
        actual = datos
    return render_template("cliente_form.html", c=actual, titulo="Editar cliente")


@rutas.route("/clientes/<int:id_cliente>/eliminar", methods=["POST"])
@rol_requerido("gerente", "admin")
def cliente_eliminar(id_cliente):
    if repo.eliminar_cliente(id_cliente):
        flash("Cliente eliminado.", "ok")
    else:
        flash("No se puede eliminar: el cliente tiene cotizaciones registradas.", "error")
    return redirect(url_for("rutas.clientes"))


# ---------- Cotizaciones ----------
@rutas.route("/cotizaciones")
@login_requerido
def cotizaciones():
    estado = request.args.get("estado", "")
    return render_template("cotizaciones.html", cotizaciones=repo.listar_cotizaciones(estado), estado=estado)


@rutas.route("/cotizaciones/nueva", methods=["GET", "POST"])
@rol_requerido("gerente", "admin")
def cotizacion_nueva():
    servicios = repo.listar_servicios()
    if request.method == "POST":
        lineas = []
        try:
            for s in servicios:
                cant = Decimal(request.form.get(f"cant_{s['id_servicio']}") or "0")
                if cant < 0: raise InvalidOperation
                if cant > 0:
                    lineas.append({"id_servicio": s["id_servicio"], "cantidad": cant, "precio": s["precio_unitario"],
                                   "subtotal": reglas.subtotal(cant, s["precio_unitario"])})
        except InvalidOperation:
            flash("Las cantidades deben ser números positivos.", "error")
            return render_template("cotizacion_form.html", clientes=repo.listar_clientes(), servicios=servicios)
        if not request.form.get("id_cliente") or not lineas:
            flash("Selecciona un cliente y al menos un servicio con cantidad.", "error")
        else:
            monto = sum((l["subtotal"] for l in lineas), Decimal("0.00"))
            id_emp = repo.id_empleado_de_usuario(session["usuario"]["id"])
            id_cot = repo.crear_cotizacion(int(request.form["id_cliente"]), id_emp, lineas, monto,
                                           reglas.requiere_revision(monto))
            flash("Cotización creada. " + ("Requiere revisión de Dirección Financiera (monto > $50,000)."
                                           if reglas.requiere_revision(monto) else "No requiere revisión financiera."), "ok")
            return redirect(url_for("rutas.cotizacion_detalle", id_cot=id_cot))
    return render_template("cotizacion_form.html", clientes=repo.listar_clientes(), servicios=servicios)


@rutas.route("/cotizaciones/<int:id_cot>")
@login_requerido
def cotizacion_detalle(id_cot):
    cot = repo.obtener_cotizacion(id_cot) or abort(404)
    return render_template("cotizacion_detalle.html", c=cot, aprobadores=reglas.ROLES_APRUEBAN)


@rutas.route("/cotizaciones/<int:id_cot>/resolver", methods=["POST"])
@rol_requerido(*reglas.ROLES_APRUEBAN)
def cotizacion_resolver(id_cot):
    decision = request.form.get("decision")
    if decision not in ("aprobada", "rechazada"): abort(400)
    ok = repo.resolver_cotizacion(id_cot, repo.id_empleado_de_usuario(session["usuario"]["id"]), decision)
    flash(f"Cotización {decision}." if ok else "La cotización ya fue resuelta.", "ok" if ok else "error")
    return redirect(url_for("rutas.cotizacion_detalle", id_cot=id_cot))


# ---------- Obras ----------
@rutas.route("/obras")
@login_requerido
def obras():
    return render_template("obras.html", obras=repo.listar_obras())


@rutas.app_template_filter("mxn")
def mxn(v):
    return f"${v:,.2f}"
