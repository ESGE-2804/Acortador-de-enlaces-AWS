# URL Shortener — AWS (S3 + DynamoDB + EC2)

Acortador de enlaces desplegado con:

| Componente        | Servicio AWS | Rol |
|-------------------|--------------|----|
| Frontend          | S3 Static    | HTML/CSS/JS estático |
| Backend (API)     | EC2 + FastAPI| Crear, consultar y redirigir |
| Base de datos     | DynamoDB     | Persistencia de enlaces |

## Requisitos
- Python 3.10+
- AWS CLI v2
- Git

## Ejecución local (backend)
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export AWS_REGION=us-east-1
export DYNAMODB_TABLE_NAME=url_shortener
uvicorn app.main:app --reload --port 8000
