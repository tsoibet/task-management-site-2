#!/bin/sh

sleep 5

flask db init
flask db migrate
flask db upgrade

flask run --host=0.0.0.0 --port=5000

# For production env
# gunicorn --config gunicorn_config.py app:app