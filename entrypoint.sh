#!/bin/sh
pip install pyopenssl --upgrade

python manage.py makemigrations --no-input

python manage.py migrate --no-input

python manage.py collectstatic --no-input

# python manage.py runserver 0.0.0.0:8000
daphne -b 0.0.0.0 -p 8000 call_center.asgi:application
