"""Crea las tablas, carga los datos ficticios y crea los usuarios de prueba.
Uso:  python -m datos.inicializar_bd
"""
import os
from werkzeug.security import generate_password_hash
from datos.conexion import obtener_conexion

CARPETA = os.path.dirname(__file__)
CLAVE_DEMO = "Demo2026!"  # contraseña FICTICIA solo para pruebas
USUARIOS = [  # (id_empleado, correo, rol)
    (1, "gerente@aguayjardin.example", "gerente"),
    (2, "ventas@aguayjardin.example", "admin"),
    (3, "finanzas@aguayjardin.example", "finanzas"),
    (4, "campo@aguayjardin.example", "tecnico"),
]


def ejecutar():
    conn = obtener_conexion()
    try:
        with conn.cursor() as cur:
            cur.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
            for archivo in ("schema.sql", "seed.sql"):
                with open(os.path.join(CARPETA, archivo), encoding="utf-8") as f:
                    cur.execute(f.read())
            for id_emp, correo, rol in USUARIOS:
                cur.execute(
                    "INSERT INTO usuario (id_empleado, correo, password_hash, rol, activo) VALUES (%s,%s,%s,%s,TRUE)",
                    (id_emp, correo, generate_password_hash(CLAVE_DEMO), rol),
                )
        conn.commit()
        print("Base de datos lista: 18 tablas, datos ficticios y 4 usuarios de prueba.")
    finally:
        conn.close()


if __name__ == "__main__":
    ejecutar()
