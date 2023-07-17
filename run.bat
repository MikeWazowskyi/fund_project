@echo off

REM Upgrade pip
call python -m pip install --upgrade pip

REM Create the virtual environment
call python -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Install all dependencies
call python -m pip install --no-cache-dir -r requirements.txt

REM Run the FastAPI application using uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 80