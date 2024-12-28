# Stop the script if any command fails
$ErrorActionPreference = "Stop"

# Print the current directory to confirm location


# Install dependencies from requirements.txt

pip install -r requirements.txt

# Run database migrations to apply schema changes

python manage.py migrate

# Collect static files for production

python manage.py collectstatic --noinput

# Optionally, create a superuser if you need to (uncomment if needed)
python manage.py createsuperuser --noinput


