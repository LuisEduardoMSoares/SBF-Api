# Framework imports.
from fastapi import FastAPI

# Prefix Import
from .. import API_PREFIX


# Import Login Core
from .auth import route as auth_router

# Import Core Routes
from app.routes import route as core_router

# Import Project Info Routes
from app.modules.users.routes import route as user_router



def create_routes(app: FastAPI) -> None:
    """
    Include routes.
    """
    # Import Login Core
    app.include_router(auth_router, tags=['Authentication'], prefix=API_PREFIX)

    # Include Core Router
    app.include_router(core_router, tags=['Core'], prefix=API_PREFIX)

    # Include Project Info Router
    app.include_router(user_router, tags=['Users'], prefix=API_PREFIX)
