# Framework imports.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Database imports
from app.db import models

# Application imports
from . import __version__
from . import API_PREFIX
from app.core.views import create_routes


# Application factory
def create_app() -> FastAPI:
    """ Application factory. """

    # Application core
    application = FastAPI(
        title="SBF Estoque - API",
        version=__version__,
        # Docs prefix
        redoc_url=API_PREFIX+"/redoc",
        docs_url=API_PREFIX+"/docs",
        openapi_url=API_PREFIX+"/openapi.json"
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://sbf-frontend.herokuapp.com",
            "https://sbf-api.herokuapp.com",
            "http://localhost:3000",
            "http://127.0.0.1:3000"
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    # Create routes
    create_routes(application)

    # Make app
    return application