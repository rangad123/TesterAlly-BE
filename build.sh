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

# Optionally, create a superuser if you need to (uncomment if needed)
# python manage.py createsuperuser --noinput

Write-Host "Deployment build complete!"
