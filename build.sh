#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py migrate

# Create a superuser with a username, email, and password
python <<EOF
from django.contrib.auth.models import User

username = "admin"
email = "admin@example.com"
password = "admin1234"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' with email '{email}' created successfully.")
else:
    print(f"Superuser '{username}' already exists.")
EOF
