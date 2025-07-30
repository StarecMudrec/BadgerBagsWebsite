#!/bin/sh
until pg_isready -h db -U postgres -d badgerbags; do
  echo "Waiting for db..."
  sleep 2
done
flask db upgrade
exec "$@"