"""Punto de entrada. Ejecutar:  flask --app app run --debug"""
import os, secrets
from flask import Flask, session, request, abort, send_from_directory
from dotenv import load_dotenv

load_dotenv()
RAIZ = os.path.dirname(os.path.abspath(__file__))


def create_app():
    app = Flask(__name__, template_folder="interfaz/templates", static_folder="interfaz/static")
    app.secret_key = os.getenv("SECRET_KEY") or secrets.token_hex(16)

    from interfaz.rutas import rutas
    app.register_blueprint(rutas)

    @app.before_request
    def proteger_csrf():
        if request.method == "POST":
            if not session.get("csrf") or request.form.get("csrf") != session["csrf"]:
                abort(400, "Token CSRF inválido")

    @app.context_processor
    def inyectar():
        session.setdefault("csrf", secrets.token_hex(16))
        return {"csrf": session["csrf"], "usuario": session.get("usuario")}

    @app.route("/recursos/<path:archivo>")
    def recursos(archivo):
        return send_from_directory(os.path.join(RAIZ, "recursos"), archivo)

    return app


app = create_app()
