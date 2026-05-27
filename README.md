# AI Academy 🎓

**URL:** https://ia-academy-app-r46v2.ondigitalocean.app/
Perfil Administrador: admin-ia
Clave: Fares20032011

Plataforma web interactiva para el aprendizaje de Ciencia de Datos e Inteligencia Artificial. Desarrollada con Django, ofrece cursos autoguiados, demos interactivas (Regresión Lineal y Algoritmos Genéticos) y exámenes con calificación automática.

## ✨ Características

- **Cursos autoguiados** con teoría, ejemplos prácticos y lecciones
- **Demo interactiva de Regresión Lineal** con carga de CSV y visualización
- **Simulación de Algoritmos Genéticos** con parámetros ajustables en tiempo real
- **Exámenes** con calificación automática y seguimiento de progreso
- **Sistema de usuarios**: registro, inicio de sesión, perfiles, recuperación de contraseña (email/SMS)
- **Panel de administración** para gestionar inscripciones, usuarios y contenido
- **Diseño responsivo** con Bootstrap 5 y tema oscuro

## 🛠️ Tecnologías

| Categoría | Tecnologías |
|---|---|
| Backend | Python 3.12, Django 4.2, django-environ |
| Base de datos | SQLite (desarrollo) / PostgreSQL (producción) |
| Ciencia de Datos | pandas, numpy, scikit-learn, plotly, deap |
| Frontend | Bootstrap 5, CSS personalizado, JavaScript |
| Despliegue | Digital Ocean App Platform |
| Otros | Pillow, psycopg2, gunicorn |

## 📁 Estructura del proyecto

```
IA-Academy/
├── apps/
│   ├── courses/          # Cursos y lecciones
│   ├── exams/            # Exámenes calificables
│   ├── genetic_demo/     # Demo de algoritmo genético
│   ├── regression_demo/  # Demo de regresión lineal
│   └── users/            # Autenticación, perfiles, SMS
├── config/               # Configuración de Django
│   └── settings/         # base.py, production.py
├── fixtures/             # Datos de semilla (cursos.json)
├── static/               # CSS, JS, favicon
├── templates/            # HTML templates
├── docs/                 # Documentación técnica
├── manage.py             # Punto de entrada de Django
└── requirements.txt      # Dependencias del proyecto
```

## 📦 Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/Fzp07/IA-academy.git
   cd IA-academy
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
   ```
   Editar `.env` con tus valores:
   | Variable | Descripción | Ejemplo |
   |---|---|---|
   | `DEBUG` | Modo depuración | `True` |
   | `SECRET_KEY` | Clave secreta de Django | `tu-clave-aqui` |
   | `DATABASE_URL` | URL de conexión a BD | `sqlite:///db.sqlite3` |

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

## 🤝 Contribuir

1. Haz fork del proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Haz commit de tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

MIT
