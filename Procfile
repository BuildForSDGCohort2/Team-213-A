release: python3 manage.py migrate
web: gunicorn health.wsgi
web: daphne health.wsgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=core.settings -v2