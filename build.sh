#!/bin/bash

# Stop the script if any command fails
set -e

# Print the current directory to confirm location
echo "Current Directory: $(pwd)"

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

# Run database migrations to apply schema changes
echo "Applying database migrations..."
python manage.py migrate



# Create a superuser programmatically
echo "Creating superuser..."
python <<EOF
from django.contrib.auth.models import User

username = "admin"
email = "admin@example.com"
password = "password"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created successfully.")
else:
    print(f"Superuser '{username}' already exists.")
EOF

echo "Deployment build complete!"
