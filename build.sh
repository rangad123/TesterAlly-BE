# Stop the script if any command fails
$ErrorActionPreference = "Stop"

# Print the current directory to confirm location
Write-Host "Current Directory: $(Get-Location)"

# Install dependencies from requirements.txt
Write-Host "Installing dependencies..."
pip install -r requirements.txt

# Run database migrations to apply schema changes
Write-Host "Applying database migrations..."
python manage.py migrate

# Collect static files for production
Write-Host "Collecting static files..."
python manage.py collectstatic --noinput

# Create a superuser programmatically
Write-Host "Creating superuser..."
python - <<EOF
from django.contrib.auth.models import User

username = "suriya"
email = "suriya@gmail.com.com"
password = "suriya1234"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created successfully.")
else:
    print(f"Superuser '{username}' already exists.")
EOF

Write-Host "Deployment build complete!"
