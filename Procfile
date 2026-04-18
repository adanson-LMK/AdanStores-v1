web: gunicorn --worker-tmp-dir /dev/shm config.wsgi:application --log-file -
release: python manage.py migrate --noinput || true