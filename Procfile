web: gunicorn --log-file=- --log-level=debug --preload config.wsgi:application
worker: celery worker --app=falmer.taskapp --loglevel=info
beat: celery beat --app=falmer.taskapp --loglevel=info
