#!/bin/bash

python manage.py wait_for_database
python manage.py migrate --no-input
python manage.py insert_demo_data
python manage.py runserver 0.0.0.0:8000
