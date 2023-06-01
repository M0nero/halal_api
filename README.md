# halal-scanner-api

## Setup DB connection
First of all, you should restore database into PostgresSQL by using PgAdmin. 

Replace below variable located in **database.py** with appropriate values

```bash
SQLALCHEMY_DATABASE_URL="postgresql://username:password@localhost/db_name"
```

## Installation

Install requirements for this project

```bash
  pip install -r requirements.txt
```

## Run API

```bash
  uvicorn main:app --reload
```
API endpoints available on http://127.0.0.1:8000/


## Swagger Panel

Official Swagger Panel available on http://127.0.0.1:8000/docs. It helps a lot to interact with API endpoints.
