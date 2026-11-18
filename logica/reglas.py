"""Reglas de negocio (capa de lógica). No dependen de Flask ni de la base de datos."""
from decimal import Decimal

UMBRAL_REVISION = Decimal("50000")  # MXN: arriba de este monto interviene Dirección Financiera
ROLES_APRUEBAN = ("gerente", "finanzas")


def requiere_revision(monto) -> bool:
    """Regla de la tabla de decisión: monto > $50,000 MXN -> revisión financiera."""
    return Decimal(str(monto)) > UMBRAL_REVISION


def subtotal(cantidad, precio) -> Decimal:
    return (Decimal(str(cantidad)) * Decimal(str(precio))).quantize(Decimal("0.01"))


def total(lineas) -> Decimal:
    """lineas: lista de (cantidad, precio)."""
    return sum((subtotal(c, p) for c, p in lineas), Decimal("0.00"))


def puede_aprobar(rol: str, monto) -> bool:
    """Montos altos solo los aprueba Gerencia/Finanzas; los normales también los puede aprobar Gerencia."""
    return rol in ROLES_APRUEBAN


def validar_cliente(datos: dict) -> list:
    errores = []
    if not datos.get("nombre", "").strip():
        errores.append("El nombre es obligatorio.")
    if datos.get("tipo_cliente") not in ("particular", "empresa", "gobierno"):
        errores.append("Selecciona un tipo de cliente válido.")
    rfc = datos.get("rfc", "").strip()
    if not (12 <= len(rfc) <= 13):
        errores.append("El RFC debe tener 12 o 13 caracteres.")
    if "@" not in datos.get("correo", ""):
        errores.append("El correo no es válido.")
    tel = datos.get("telefono", "").strip()
    if not (tel.isdigit() and 10 <= len(tel) <= 15):
        errores.append("El teléfono debe tener entre 10 y 15 dígitos.")
    return errores
