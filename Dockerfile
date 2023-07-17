FROM python:3.10-slim

LABEL authors="https://github.com/MikeWazowskyi"

WORKDIR /fund-app

COPY alembic ./alembic

COPY alembic.ini ./

COPY requirements.txt ./

COPY init_database.sh ./

COPY .env ./

COPY app ./app

RUN python -m pip install --upgrade pip

RUN python -m venv venv

RUN python -m pip install --no-cache-dir -r requirements.txt

RUN chmod +x ./init_database.sh

RUN ./init_database.sh

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
