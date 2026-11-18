"""Conexión real a PostgreSQL. Las credenciales se leen del archivo .env (nunca van en el código)."""
import os
from contextlib import contextmanager
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


def obtener_conexion():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "agua_y_jardin"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
    )


@contextmanager
def cursor():
    """Entrega un cursor que devuelve diccionarios; confirma (commit) o revierte (rollback) solo."""
    conn = obtener_conexion()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
