#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files (for CSS/Images)
python manage.py collectstatic --no-input

# Run migrations to set up database tables
python manage.py migrate