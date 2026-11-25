# Sistema de Gestión de Restaurante - Platos (INACAP Backend Unidad 2)

Proyecto desarrollado con **Django 5.2** y **MariaDB (XAMPP)** para la gestión de platos de un restaurante (Temática N°9).

## Requisitos previos

- Python 3.12+
- XAMPP con el servicio **MySQL (MariaDB)** activo en `127.0.0.1:3306`

## Pasos para ejecutar el proyecto

### 1. Iniciar XAMPP y crear la base de datos

1. Abre el panel de control de **XAMPP** e inicia el módulo **MySQL**.
2. Crea la base de datos `restaurante_db` con cotejamiento `utf8mb4` (desde phpMyAdmin o consola MySQL):

```sql
CREATE DATABASE IF NOT EXISTS restaurante_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

### 2. Crear y activar el entorno virtual (`venv`)

En PowerShell, dentro de la carpeta del proyecto:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 4. Ejecutar migraciones

Verifica la configuración y crea las tablas en MariaDB:

```powershell
python manage.py check
python manage.py migrate
```

### 5. Cargar datos de prueba (`seed_platos`)

```powershell
python manage.py seed_platos
```

### 6. Iniciar el servidor de desarrollo

```powershell
python manage.py runserver
```

Luego abre en tu navegador: `http://127.0.0.1:8000/`

## Variables de entorno opcionales

Por defecto `settings.py` usa la configuración local de XAMPP (`root` sin contraseña en `127.0.0.1:3306` y base `restaurante_db`). Puedes sobreescribirlas con:

- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
