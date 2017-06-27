web: gunicorn config.wsgi:application  --log-file=- --loglevel=info --preload
worker: celery worker --app=falmer.taskapp --loglevel=info
