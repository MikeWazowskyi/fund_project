#!/bin/sh
python -m pip install --upgrade pip
python -m venv venv
source venv/bin/activate
python -m pip install --no-cache-dir -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host localhost --port 80