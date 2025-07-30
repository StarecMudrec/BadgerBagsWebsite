#!/bin/sh

# Wait for PostgreSQL to be ready
until pg_isready -h db -U postgres -d badgerbags; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

# Run migrations
flask db upgrade

# Start the main application
exec gunicorn --bind 0.0.0.0:8000 wsgi:app