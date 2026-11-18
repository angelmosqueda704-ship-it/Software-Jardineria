from decimal import Decimal
from logica import reglas


def test_umbral_exacto_no_requiere_revision():
    assert reglas.requiere_revision(50000) is False

def test_monto_alto_requiere_revision():
    assert reglas.requiere_revision(50000.01) is True

def test_total_de_lineas():
    assert reglas.total([(2, "48000"), (500, "18.50")]) == Decimal("105250.00")

def test_cliente_valido():
    d = dict(nombre="Ana", tipo_cliente="particular", rfc="ABCD010101AB1", telefono="4491234567", correo="a@b.mx")
    assert reglas.validar_cliente(d) == []

def test_cliente_invalido():
    assert len(reglas.validar_cliente(dict(nombre="", tipo_cliente="x", rfc="1", telefono="abc", correo="mal"))) == 5
