#!/bin/sh

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create superuser if it doesn't exist (change with your desired username/password/email)
echo "Creating superuser..."
python manage.py createsuperuser --noinput || echo "Superuser already exists."

# Start the Django development server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
