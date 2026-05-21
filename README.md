# Plataforma Educativa - Ciencia de Datos y Algoritmos

Plataforma web interactiva para el aprendizaje de Ciencia de Datos, incluyendo cursos de Regresión Lineal y Algoritmos Genéticos con demos interactivas y exámenes calificables.

## Características

- 🎓 Cursos autoguiados con teoría y ejemplos prácticos
- 📊 Demo interactiva de Regresión Lineal con carga de CSV
- 🧬 Simulación interactiva de Algoritmos Genéticos
- 📝 Exámenes con calificación automática
- 👥 Sistema de usuarios con perfiles y progreso
- 📱 Diseño responsivo con Bootstrap 5

## Requisitos

- Python 3.10+
- PostgreSQL (opcional, usa SQLite por defecto)
- pip

## Instalación

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd IA-Academy
```

2. Crear y activar entorno virtual:
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate    # Linux/Mac
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

5. Ejecutar migraciones y cargar datos:
```bash
python manage.py migrate
python manage.py loaddata fixtures/courses.json
python manage.py createsuperuser
```

6. Iniciar servidor:
```bash
python manage.py runserver
```

Link de la web app: https://ia-academy-app-r46v2.ondigitalocean.app/
