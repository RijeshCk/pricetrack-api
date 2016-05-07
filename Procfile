web: gunicorn price_track_api.wsgi --log-file -
worker: celery --beat worker --app=price_track_api --loglevel=INFO
