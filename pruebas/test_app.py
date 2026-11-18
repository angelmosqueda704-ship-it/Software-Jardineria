"""Pruebas de integración: requieren PostgreSQL con la BD inicializada (python -m datos.inicializar_bd)."""
import re, pytest
from app import create_app


@pytest.fixture
def cli():
    app = create_app(); app.config["TESTING"] = True
    return app.test_client()

def token(cli, url="/login"):
    return re.search(r'name="csrf" value="(\w+)"', cli.get(url).get_data(as_text=True)).group(1)

def entrar(cli, correo="gerente@aguayjardin.example", clave="Demo2026!"):
    return cli.post("/login", data={"correo": correo, "contrasena": clave, "csrf": token(cli)}, follow_redirects=True)

def test_login_correcto(cli):
    assert "Resumen general" in entrar(cli).get_data(as_text=True)

def test_login_incorrecto(cli):
    assert "incorrectos" in entrar(cli, clave="mala").get_data(as_text=True)

def test_requiere_sesion(cli):
    assert cli.get("/clientes").status_code == 302

def test_post_sin_csrf_rechazado(cli):
    assert cli.post("/login", data={"correo": "x", "contrasena": "y"}).status_code == 400

def test_crud_cliente(cli):
    entrar(cli); t = token(cli, "/clientes/nuevo")
    d = dict(nombre="Cliente Prueba SA", tipo_cliente="empresa", rfc="CPR010101AA1", telefono="4491112233",
             correo="p@prueba.example", direccion="Calle 1", csrf=t)
    assert "registrado" in cli.post("/clientes/nuevo", data=d, follow_redirects=True).get_data(as_text=True)
    from datos import repositorios as r
    c = [x for x in r.listar_clientes("Cliente Prueba") if x["nombre"] == "Cliente Prueba SA"][0]
    d["nombre"] = "Cliente Editado SA"
    assert "actualizado" in cli.post(f"/clientes/{c['id_cliente']}/editar", data=d, follow_redirects=True).get_data(as_text=True)
    assert "eliminado" in cli.post(f"/clientes/{c['id_cliente']}/eliminar", data={"csrf": t}, follow_redirects=True).get_data(as_text=True)

def test_no_elimina_cliente_con_cotizaciones(cli):
    entrar(cli)
    assert "No se puede eliminar" in cli.post("/clientes/1/eliminar", data={"csrf": token(cli, "/clientes")}, follow_redirects=True).get_data(as_text=True)

def test_cotizacion_alta_requiere_revision(cli):
    entrar(cli); t = token(cli, "/cotizaciones/nueva")
    r = cli.post("/cotizaciones/nueva", data={"id_cliente": "2", "cant_5": "2", "csrf": t}, follow_redirects=True)
    assert "$96,000.00" in r.get_data(as_text=True) and "revisión" in r.get_data(as_text=True)

def test_tecnico_no_puede_crear_cliente(cli):
    entrar(cli, "campo@aguayjardin.example")
    assert "no tiene permiso" in cli.get("/clientes/nuevo", follow_redirects=True).get_data(as_text=True)
