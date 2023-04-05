# REST API With Flask & SQL Alchemy

> TODOS API using Python Flask, SQL Alchemy and Marshmallow

## Quick Start Using Pipenv

```bash
# Activate venv
$ pipenv shell

# Install dependencies
$ pipenv install

# Create DB and table migrations
$ python

from app import app, db

with app.app_context():
    db.create_all()


# Run Server (http://localhst:5000)
python app.py
```

## Endpoints

- GET /todos
- GET /todos/:id
- POST /todos
- PUT /todos/:id
- DELETE /todos/:id
