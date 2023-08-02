# Charity Fund
[![FastAPI CI](https://github.com/MikeWazowskyi/fund_project/actions/workflows/main.yml/badge.svg)](https://github.com/MikeWazowskyi/fund_project/actions/workflows/main.yml)

## Описание

Charity Fund - API-сервис для сбора средств на благотворительность

## Установка

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:MikeWazowskyi/cat_charity_fund.git
```

```
cd cat_charity_fund
```

Настроить файл .env про примеру файла .env_example:

```
.env_example
```
* В контейнере Docker + GNU make:

    ```
    make start
    ```

* Если у вас Linux/macOS

    ```
    chmod +x run.sh
  
    ./run.sh
    ```

* Если у вас windows

    ```
    run.bat
    ```

## Примеры запросов к REST API:

## Создание новых благотворительных проектов

### POST /charity_project/

Request:

Content-Type: application/json

```
{
  "name": "New project",
  "description": "New project description",
  "full_amount": 10000 
}
```

Response:

```
{
  "name": "New project",
  "description": "New project description",
  "full_amount": 10000,
  "id": 1,
  "invested_amount": 0,
  "fully_invested": false,
  "create_date": "2023-08-24T14:15:22Z",
  "close_date": "2023-08-24T14:15:22Z"
}
```

### GET /charity_project/

Content-Type: application/json

Response:

```
[
  {
    "name": "New project",
    "description": "New project description",
    "full_amount": 10000,
    "id": 1,
    "invested_amount": 0,
    "fully_invested": false,
    "create_date": "2023-08-24T14:15:22Z",
    "close_date": "2023-08-24T14:15:22Z"
  }
]
```

### DELETE /charity_project/{project_id}

Content-Type: application/json

Response:

```
[
  {
    "name": "New project",
    "description": "New project description",
    "full_amount": 10000,
    "id": 1,
    "invested_amount": 0,
    "fully_invested": false,
    "create_date": "2023-08-24T14:15:22Z",
    "close_date": "2023-08-24T14:15:22Z"
  }
]
```

### UPDATE /charity_project/{project_id}

Content-Type: application/json

Request:

Editable fields:
  * name
  * description
  * full_amount

```
{
  "name": "Updated new project",
  "description": "Updated new project description",
  "full_amount": 10000 0
}
```

Response:

```
[
  {
    "name": "Updated new project",
    "description": "Updated new project description",
    "full_amount": 100000,
    "id": 1,
    "invested_amount": 0,
    "fully_invested": false,
    "create_date": "2023-08-24T14:15:22Z",
    "close_date": "2023-08-24T14:15:22Z"
  }
]
```

## Создание новых пожертвований

### POST /charity_project/

Request:

Optional fields:
  * comment

Content-Type: application/json

```
{
  "comment": "New donation",
  "full_amount": 10000 
}
```

Response:

```
{
  "full_amount": 10000,
  "comment": "New donation",
  "id": 1,
  "create_date": "2023-08-24T14:15:22Z"
}
```

### GET /donation/

Content-Type: application/json

Response:

```
[
  {
    "full_amount": 1000,
    "comment": "New donation",
    "id": 1,
    "create_date": "2023-08-24T14:15:22Z",
    "user_id": 1,
    "invested_amount": 0,
    "fully_invested": false,
    "close_date": "2023-08-24T14:15:22Z"
  }
]
```

### GET /donation/my

Content-Type: application/json

Response:

```
[
  {
    "full_amount": 1000,
    "comment": "New comment",
    "id": 1,
    "create_date": "2023-08-24T14:15:22Z"
  }
]
```

### Адрес полной документации к API:

```
http://<host>/docs
```


## Об авторе:

https://github.com/MikeWazowskyi
