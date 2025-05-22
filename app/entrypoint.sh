#!/bin/sh

set -e

echo "Ожидание загрузки БД"
sleep 30

echo "Миграция"
alembic upgrade head

echo "Згрузка тестовых данных"
poetry run python -m src.load_test_data

echo "Запуск приложения"
exec poetry run gunicorn -k uvicorn.workers.UvicornWorker \
  --worker-tmp-dir /dev/shm src.main:app --bind=0.0.0.0:7000
