# Sistema Web de Votaciones – Festival de la Leyenda Vallenata 2027

Entrega 2 · Desarrollo Web · Fundación Universitaria del Área Andina.
Aplicación Django (patrón MVT) con MySQL. Jerarquía de datos: **Edición → Categoría → Votación → Opción** (el modelo `Voto` queda listo para la siguiente entrega).

## Qué incluye esta fase
- Proyecto Django `festival` y aplicación `votaciones`.
- Conexión a MySQL, modelos relacionados y migraciones.
- Registro, inicio y cierre de sesión (autenticación de Django).
- Django Admin para gestionar ediciones, categorías, votaciones y opciones.
- Interfaz pública que muestra datos reales de MySQL: ediciones → categorías → votaciones → opciones.

## Requisitos
Python 3.10+, MySQL 8 (o MariaDB) y Git.

## Instalación (Windows)
```bat
git clone https://github.com/USUARIO/REPOSITORIO.git
cd REPOSITORIO
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Base de datos MySQL
1. En MySQL Workbench o consola:
   ```sql
   CREATE DATABASE votaciones_festival CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
2. Copia `.env.example` como `.env` y escribe tu usuario y contraseña local de MySQL (el archivo `.env` no se sube al repositorio).

## Puesta en marcha
```bat
python manage.py migrate
python manage.py cargar_datos
python manage.py createsuperuser
python manage.py runserver
```
- Sitio público: http://127.0.0.1:8000/
- Administración: http://127.0.0.1:8000/admin/

`cargar_datos` crea datos de prueba (ediciones 2026 y 2027, categorías, votaciones y opciones). Se puede ejecutar varias veces.

## Pruebas
```bat
set DB_ENGINE=sqlite
python manage.py test votaciones
```
(Las pruebas también corren con MySQL si el usuario tiene permiso para crear bases de datos.)

## Estructura
```
festival/        configuración del proyecto (settings, urls)
votaciones/      modelos, vistas, plantillas, admin y pruebas
  templates/     HTML con Bootstrap 5
  management/    comando cargar_datos
```

## Seguridad
No hay contraseñas ni claves en el repositorio. Los datos de conexión se leen del archivo `.env` o de variables de entorno.
