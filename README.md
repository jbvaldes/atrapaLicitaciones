# Atrapando Licitaciones

Una aplicación Flask para gestionar licitaciones obtenidas de la API de Mercado Público y administrar usuarios con roles (admin/usuario). Incluye paginación de 10 registros por página y autenticación segura.

## Características
- Consulta licitaciones desde la API de Mercado Público con un ticket.
- Paginación (10 registros por página) para licitaciones y usuarios.
- Módulo de administración de usuarios (crear, editar, eliminar) solo para administradores.
- Interfaz responsiva con Bootstrap 5.
- Base de datos MySQL para persistencia de datos.

## Tecnologías
- **Backend**: Flask, Python, MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Dependencias**: `flask`, `mysql-connector-python`, `requests`, `python-dotenv`

## Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/jbvaldes/atrapaLicitaciones.git
   cd atrapaLicitaciones
