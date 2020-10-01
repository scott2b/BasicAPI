# BasicAPI

Basic starter API built with [FastAPI](https://fastapi.tiangolo.com/)

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


## About

This is a stripped down and heavily refactored version of the official
[full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql)
cookiecutter.

The full stack cookie cutter is a very heavy stack which makes a LOT of assumptions,
particularly with respect to deployment configuration.

This project slims it down to the bare essentials. The following are required:

 * SQLAlchemy + postgres as the database, although postgres should not be a strict
   requirement in theory.

There are really no other assumptions made about your stack. If you are looking
for something that is full-featured and ready to deploy, please take a look at the
original full-stack cookie cutter.


## The API

### Configuration

Configurations are managed by a pydantic settings object in `config.configuration`.
In general, deployment specific parameters should be set as environment variables.
See the [pydantic docs](https://pydantic-docs.helpmanual.io/usage/settings/) for
specifics about how pydantic's settings work. If you don't already have a
mechanism for managing your environment, you might look at pydantic's builtin
dotenv support.

### Interactive docs

Redoc is set to the root path of the API. The interactive swagger docs are on
the /docs path. These are easily set by the `redoc_url` and `docs_url` parameters
respectively in the FastAPI instantiation in `app.main`.

### Email features

are untested.

I am not sure what the cookiecutter uses for building the email templates,
I just copied those from the template build directory for now until I actually
get a chance to test emailing to see if it all works.


## The dashboard

Is an unmodified copy of the frontend from the cookie cutter repo.

If you deploy the dashboard, you will need to set the CORS configuration
in the API accordingly. It is currently set to accept requests from a
local dashboard on :8080.

## About the refactorings

I found it a bit much to get my head around the original package structure at
first. For better or for worse, I have refactored it considerably into a
structure that makes more sense to me. In particular, the database stuff has
significantly changed. There does not seem to be a community consensus on how
SQLAlchemy projects should be structured. While renaming and moving things around
a bit, I have kept to the original concept of models (which are called mappings
in the SQLAlchemy docs) and a separate CRUD manager class which is essentially
all the model behavior.

In general, I am using a pattern of accessing the CRUD manager directly via the
`orm` package, while accessing the model (i.e. mapping) class via `orm.models`. I
also have a preference for pluralized object table names, and am leaning toward
using a matching pluralized name for the manager, as can be seen with the
handling of users.


I have moved to using relative imports almost everywhere, as this seems more
long-term manageble to me. The current package structure breaks down as:

 * `api`: API endpoints (i.e. the routes)
 * `auth`: auth and security stuff that was in core
 * `config`: configuration management with pydantic BaseSettings. Formerly also in core
 * `mail`: email handling
 * `orm`: All the databse stuff, consolidating what was in db, crud, and models
 * `schemas`: pydantic object schemata. See the FastAPI docs for more info on how these are used
