#!/bin/sh

# Apply database migrations
echo "Initializing database..."
until alembic upgrade head; do
  echo "Waiting for db to be ready..."
  sleep 2
done

