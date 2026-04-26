# Blacklist Email API

Microservicio REST para manejar una lista negra global de correos. Permite agregar un email y consultar si esta bloqueado.

## Requisitos

- Python 3.11
- pip

## Levantar en local

1. Crear entorno virtual e instalar dependencias:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Crear archivo de entorno:

```bash
copy .env.example .env
```

3. Ajustar variables en `.env`:

- `STATIC_TOKEN`
- `JWT_SECRET_KEY`
- `DATABASE_URL` (opcional en local; si no existe usa SQLite)

4. Ejecutar la API:

```bash
python -m flask --app app run
```

La API queda en `http://127.0.0.1:5000`.

## Endpoints principales

- `GET /health`
- `POST /blacklists`
- `GET /blacklists/<email>`

Para `POST /blacklists` y `GET /blacklists/<email>` se requiere:

`Authorization: Bearer <STATIC_TOKEN>`

## Prueba rapida

Health check:

```bash
curl http://127.0.0.1:5000/health
```

Agregar email a blacklist:

```bash
curl -X POST http://127.0.0.1:5000/blacklists ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer <STATIC_TOKEN>" ^
  -d "{\"email\":\"demo@empresa.com\",\"app_uuid\":\"550e8400-e29b-41d4-a716-446655440000\",\"blocked_reason\":\"Fraude\"}"
```

## Tests

```bash
python -m pytest tests/ -v
```

## Despliegue (resumen)

El proyecto esta preparado para AWS Elastic Beanstalk usando `Procfile` y Gunicorn. Para desplegar, configura en el entorno de EB las variables `DATABASE_URL`, `JWT_SECRET_KEY` y `STATIC_TOKEN`.
 
