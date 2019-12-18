#!/bin/sh
python manage.py migrate
while true; do
    python manage.py runserver 0.0.0.0:8000
    sleep 5s
done
