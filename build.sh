#!/usr/bin/env bash
# exit on error
set -o errexit

# Set the Django settings module
export DJANGO_SETTINGS_MODULE="testerally_be.settings"

pip install -r requirements.txt

python manage.py migrate

# Create a superuser with a username, email, and password
python -c "
import os
import django
from django.contrib.auth.models import User

# Setup Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'testerally_be.settings'
django.setup()

username = 'admin'
email = 'admin@example.com'
password = 'admin1234'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser {username} with email {email} created successfully.')
else:
    print(f'Superuser {username} already exists.')
"
