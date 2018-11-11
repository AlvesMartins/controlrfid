#!/usr/bin/env bash

python /data/web/ControlRfid/manage.py makemigrations
python /data/web/ControlRfid/manage.py migrate
python /data/web/ControlRfid/manage.py runserver 0.0.0.0:8000
echo "END..."
exec "$@";

