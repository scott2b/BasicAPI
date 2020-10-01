# BasicAPI
A proof-of-concept level basic web application with web API using FastAPI

## Quickstart

 * Clone this repository
 * pip install -r reqirements.txt (preferably in a virtualenv)
 * Copy dot.env.example to .env and edit
 * Copy alembic.ini.example to alembic.ini and edit the sqlalchemy.url
 * Run alembic migrations
 * uvicorn app.main:app --reload 

To run the dashboard:
 * cd dashboard
 * npm install
 * npm run start
