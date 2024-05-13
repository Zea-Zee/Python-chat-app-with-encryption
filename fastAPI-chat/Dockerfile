FROM python:3.11-slim

COPY . .

CMD ['pip install -r requirements.txt', 'alembic revision --autogenerate', 'alembic upgrade head', 'uvicorn main:app --reload', 'celery -A tasks.tasks:celery worker --loglevel=INFO --pool=solo']
