#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Navigating to Django project..."
cd ransomware_control

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running database migrations..."
python manage.py migrate

echo "Build completed successfully!"
