web: gunicorn --log-file=- --loglevel=info --preload config.wsgi:application
worker: celery worker --app=falmer.taskapp --loglevel=info
