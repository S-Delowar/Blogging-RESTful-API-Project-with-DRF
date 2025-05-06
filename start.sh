#!/bin/sh

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser if not exists..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='${DJANGO_SUPERUSER_USERNAME}').exists():
    User.objects.create_superuser(
        username='${DJANGO_SUPERUSER_USERNAME}', 
        email='${DJANGO_SUPERUSER_EMAIL}', 
        password='${DJANGO_SUPERUSER_PASSWORD}'
    )
"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
gunicorn blogapi.wsgi:application --bind 0.0.0.0:8000 --timeout 120
