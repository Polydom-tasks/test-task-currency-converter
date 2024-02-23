#!/bin/sh

# Wait for the database to be ready
./wait-for-it.sh db:5432 --timeout=30 -- echo "Database is up"

alembic upgrade head
uvicorn main:app --host 0.0.0.0 --reload
