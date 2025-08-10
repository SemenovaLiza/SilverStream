#!/bin/bash

echo "Waiting for postgres..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

python manage.py migrate
python manage.py compilemessages -l en -l ru
python manage.py collectstatic --no-input 

gunicorn -b 0.0.0.0:8000 config.wsgi:application

exec "$@"