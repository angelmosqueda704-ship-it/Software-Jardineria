"""Autenticación y permisos por rol."""
from functools import wraps
from flask import session, redirect, url_for, flash
from werkzeug.security import check_password_hash
from datos import repositorios as repo


def autenticar(correo, contrasena):
    u = repo.usuario_por_correo(correo.strip().lower())
    if u and u["activo"] and check_password_hash(u["password_hash"], contrasena):
        return u
    return None


def login_requerido(f):
    @wraps(f)
    def interior(*a, **k):
        if "usuario" not in session:
            return redirect(url_for("rutas.login"))
        return f(*a, **k)
    return interior


def rol_requerido(*roles):
    def deco(f):
        @wraps(f)
        @login_requerido
        def interior(*a, **k):
            if session["usuario"]["rol"] not in roles:
                flash("Tu rol no tiene permiso para esta acción.", "error")
                return redirect(url_for("rutas.inicio"))
            return f(*a, **k)
        return interior
    return deco
