#!/usr/bin/env bash
set -o errexit

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python ransomware_control/manage.py collectstatic --no-input

echo "Running database migrations..."
python ransomware_control/manage.py migrate

echo "Build completed successfully!"
