# Framework imports.
from fastapi import FastAPI

# Prefix Import
from .. import API_PREFIX


# Import Core Routes
from app.routes import router as core_router

# Import Project Info Routes
from app.modules.users.routes import route as user_router



def create_routes(app: FastAPI) -> None:
    """
    Include routes.
    """
    # Include Core Router
    app.include_router(core_router, tags=['Core'], prefix=API_PREFIX)

    # Include Project Info Router
    app.include_router(user_router, tags=['Users'], prefix=API_PREFIX)
