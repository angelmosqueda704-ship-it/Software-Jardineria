# Sistema Integral de Gestión — Agua y Jardín

**Materia:** Análisis y Diseño de Software · **Grupo:** 31
**Equipo:** Emmanuel Rico López, Angel Adrián Mosqueda López, María de la Luz de Jesús Andrés, Pedro Encina Villegas

Primer avance funcional (web) del sistema: inicio de sesión real con roles, gestión de clientes (CRUD completo), cotizaciones con la regla de revisión financiera y consulta de obras, todo conectado a una base de datos PostgreSQL.

## Tecnologías (decisiones del equipo)
| Elemento | Elección |
|---|---|
| Lenguaje | Python 3.10+ (framework web Flask) |
| Base de datos | PostgreSQL 14+ (acceso con psycopg2) |
| Editor | Visual Studio Code |

## Estructura de carpetas
```
agua_y_jardin/
├── app.py                 Punto de entrada de la aplicación
├── interfaz/              Pantallas: rutas, templates (HTML) y estilos (CSS)
├── logica/                Reglas de negocio (tabla de decisión) y autenticación/roles
├── datos/                 Conexión a PostgreSQL, consultas, schema.sql, seed.sql
├── recursos/              Logo y capturas de pantalla
├── pruebas/               Pruebas automáticas (pytest)
├── .env.example           Plantilla de credenciales (el .env real NO se sube)
└── requirements.txt
```

## Instalación y ejecución en VS Code
1. Instala Python, PostgreSQL y VS Code (extensión *Python*). Abre esta carpeta con **File → Open Folder**.
2. En la terminal de VS Code:
   ```
   python -m venv venv
   venv\Scripts\activate          (Windows)   |   source venv/bin/activate   (Mac/Linux)
   pip install -r requirements.txt
   ```
3. Crea la base de datos vacía (en pgAdmin o con `psql`):  `CREATE DATABASE agua_y_jardin;`
4. Copia `.env.example` como `.env` y escribe tu usuario y contraseña de PostgreSQL.
5. Crea las tablas y carga datos ficticios:  `python -m datos.inicializar_bd`
6. Inicia la página:  `flask --app app run --debug`  y abre http://localhost:5000
   (también puedes usar el botón ▶ de VS Code: configuración "Flask: Agua y Jardín").

> Atención: `inicializar_bd` borra y recrea todas las tablas. Úsalo solo en la base de pruebas.

## Usuarios de prueba (ficticios) — contraseña: `Demo2026!`
| Correo | Rol | Puede |
|---|---|---|
| gerente@aguayjardin.example | gerente | Todo; aprobar/rechazar cotizaciones |
| ventas@aguayjardin.example | admin | Clientes y cotizaciones (crear/editar) |
| finanzas@aguayjardin.example | finanzas | Consultar y aprobar/rechazar cotizaciones |
| campo@aguayjardin.example | tecnico | Solo consulta |

## Qué incluye este avance
- Base de datos con las **18 tablas** y **27 llaves foráneas** del Diagrama Entidad–Relación (`datos/schema.sql`) y datos ficticios (`datos/seed.sql`).
- **Login** con contraseñas cifradas (hash) y **permisos por rol**.
- **Clientes:** alta, consulta con búsqueda, edición y baja (no deja eliminar clientes con cotizaciones).
- **Cotizaciones:** alta con varios servicios, total calculado, regla de la tabla de decisión (monto > $50,000 MXN → revisión de Dirección Financiera), aprobación/rechazo.
- **Obras:** listado con cuadrilla asignada y avance.
- Seguridad básica: consultas parametrizadas (sin inyección SQL), token CSRF en formularios, credenciales fuera del código.

## Pruebas
`python -m pytest pruebas` (13 pruebas: reglas de negocio, login, permisos, CRUD de clientes y cotizaciones; requieren la BD inicializada).

## Pendiente para próximas entregas
Módulos de cuadrillas/personal, finanzas y nómina, calidad y prevención; reportes de avance desde la app móvil; facturación CFDI.

*Todos los datos de ejemplo son ficticios.*
