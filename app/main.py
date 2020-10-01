from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .config import settings
from .api.api_v1.api import api_router


app = FastAPI(
    title='BasicAPI',
    description='This is just a starter project',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/'
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(api_router, prefix=settings.API_V1_STR)
