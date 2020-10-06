release: python3 manage.py migrate
web: gunicorn health.wsgi
worker: python manage.py runworker channels --settings=health.settings -v2
