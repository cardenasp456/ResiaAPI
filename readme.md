# Resia API — Backend (Python)

**Resia API** es el servicio backend de Resia. Expone endpoints REST para autenticación, gestión de datos académicos (por ejemplo: pruebas de estado del estudiante) y otros módulos del proyecto.

> 📌 **Stack sugerido:** Python 3.10+, Flask o FastAPI, SQLAlchemy, Alembic (migraciones), PyTest, Black/Ruff.  
> Si tu proyecto ya está definido (Flask/FastAPI), adapta los comandos marcados como *opcional*.

---

## 🚀 Quickstart

### 1) Requisitos
- **Python** ≥ 3.10
- **pip** y (opcional) **virtualenv**
- (Opcional) **PostgreSQL** / **MySQL** / **SQLite** para persistencia

### 2) Crear entorno virtual (recomendado)
```bash
# Linux/Mac
python -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3) Instalar dependencias
Asegúrate de tener `requirements.txt` actualizado y ejecuta:
```bash
pip install -r requirements.txt
```

### 4) Variables de entorno
Crea un archivo **.env** en la raíz del proyecto (o usa variables del sistema). Ejemplo:

```ini
# .env (ejemplo)
APP_NAME=ResiaAPI
ENV=development
HOST=0.0.0.0
PORT=8000

# Base de datos (elige una)
#DATABASE_URL=sqlite:///./resia.db
#DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/resia
#DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/resia

JWT_SECRET=change_me
CORS_ORIGINS=http://localhost:4200,http://127.0.0.1:4200
LOG_LEVEL=INFO
```

> ✅ **No subas** `.env` al repo público. Usa variables seguras en CI/CD.

### 5) Inicializar base de datos (opcional, si usas SQLAlchemy + Alembic)
```bash
# generar/actualizar tablas con migraciones
alembic upgrade head
```
> Si aún no configuraste Alembic:
> ```bash
> alembic init alembic
> # ajusta alembic.ini y env.py a tu DATABASE_URL y modelos
> alembic revision --autogenerate -m "init"
> alembic upgrade head
> ```

### 6) Ejecutar la aplicación (desarrollo)
La forma **rápida** (según indicaste):
```bash
python app.py
```
Alternativas según framework:
- **Flask (app factory)**  
  ```bash
  export FLASK_APP="resia:create_app()"   # Linux/Mac
  set FLASK_APP="resia:create_app()"      # Windows
  flask run --host=$HOST --port=$PORT
  ```
- **FastAPI (Uvicorn)**  
  ```bash
  uvicorn app:app --host $HOST --port $PORT --reload
  ```

Abre `http://localhost:8000` (o el puerto configurado).

---

## 📚 Documentación de API

- **Swagger/OpenAPI**: según tu framework y librería:
  - FastAPI: `http://localhost:8000/docs` y `http://localhost:8000/redoc`
  - Flask (Flasgger/Swagger-UI): ruta configurada (ej.: `/api/docs`)

Incluye una colección de **Postman/Insomnia** en `docs/` si está disponible.

---

## 🧩 Estructura sugerida del proyecto

```
resia-api/
├─ app.py                  # punto de entrada (Flask/FastAPI)
├─ resia/                  # paquete principal
│  ├─ __init__.py
│  ├─ api/                 # blueprints/routers (v1, v2, etc.)
│  ├─ models/              # SQLAlchemy models / pydantic schemas
│  ├─ services/            # lógica de negocio
│  ├─ repositories/        # acceso a datos
│  ├─ core/                # config, seguridad, middlewares
│  └─ utils/               # helpers
├─ alembic/                # migraciones (si aplica)
├─ tests/                  # pruebas
├─ docs/                   # documentación adicional
├─ requirements.txt
└─ README.md
```

---

## 🔐 Seguridad

- **CORS**: configura `CORS_ORIGINS` para permitir el dominio del frontend (Angular).
- **JWT**: usa `JWT_SECRET` fuerte y rotación de tokens cuando sea posible.
- **Logging**: ajusta `LOG_LEVEL` y usa trazas con IDs de petición si tienes reverse proxy.

---

## 🧪 Pruebas & Calidad

### Unit tests
```bash
pytest -q
# con cobertura
pytest --cov=resia --cov-report=term-missing
```

### Lint/format
```bash
ruff check .
black .
```

> Agrega hooks de **pre-commit** para asegurar formato/lint antes de hacer push.

---

## 📦 Despliegue

### Producción (gunicorn + uvicorn worker / wsgi)
- **FastAPI**:
  ```bash
  gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8000
  ```
- **Flask** (WSGI):
  ```bash
  gunicorn -w 4 "app:create_app()" --bind 0.0.0.0:8000
  # o si app.py expone 'app' directamente:
  gunicorn -w 4 app:app --bind 0.0.0.0:8000
  ```

### Docker (opcional)
```dockerfile
# Dockerfile (ejemplo)
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "app.py"]
```
```bash
docker build -t resia-api .
docker run -p 8000:8000 --env-file .env resia-api
```

---

## 🔎 Endpoints de ejemplo (ilustrativos)
| Método | Ruta                        | Descripción                               | Auth |
|-------:|-----------------------------|-------------------------------------------|:----:|
| GET    | `/health`                   | Health check                              | ❌   |
| POST   | `/auth/login`               | Autenticación (JWT)                       | ❌   |
| GET    | `/tests`                    | Listar pruebas                            | ✅   |
| POST   | `/tests`                    | Crear prueba                              | ✅   |
| GET    | `/tests/{id}`               | Obtener detalle de prueba                 | ✅   |
| POST   | `/tests/{id}/responses`     | Enviar respuestas de estudiante           | ✅   |

> Ajusta a tus rutas reales. Documenta los esquemas (request/response) en OpenAPI.

---

## 🧰 Troubleshooting

- **No arranca por dependencia faltante**: confirma `requirements.txt` y vuelve a `pip install -r requirements.txt`.
- **Error de conexión a DB**: revisa `DATABASE_URL` y credenciales/puerto.
- **CORS bloquea peticiones**: agrega el origen del front a `CORS_ORIGINS`.
- **Migraciones fallan**: valida `alembic.ini` y que los modelos coinciden con la DB.

---

## 👥 Mantenimiento

- **Owners:** @tu-usuario  
- **Issues:** usar GitHub Issues con etiquetas (`bug`, `feat`, `tech-debt`).  
- **Versionado:** SemVer + `CHANGELOG.md`.

---

## 📝 Comandos mínimos que pediste

### Instalar dependencias
```bash
pip install -r requirements.txt
```

### Ejecutar la aplicación
```bash
python app.py
```

> Si necesitas, puedo generarte también un **`.env.example`** y un **Dockerfile** listos para tu repo.
