web: gunicorn price_track_api.wsgi --log-file -
worker: celery --app=price_track_api worker --loglevel=INFO
beat:celery --app=price_track_api --beat worker
