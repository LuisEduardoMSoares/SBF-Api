# Standard Imports
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

# Database Import
from app.db.engine import get_db

# Typing Imports
from typing import List

# Exception imports
from sqlalchemy.exc import IntegrityError

# Authentication Imports
from ..users.models import User
from app.core.auth import manager

# User Schemas
from .services import UserService
from .schemas import UserCreate
from .schemas import UserUpdate
from .schemas import UserResponse



route = APIRouter()
user_service = UserService()



@route.get("/users/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db), auth_user: User=Depends(manager)):
    """
    ## Retrieve a list of users.

    ### Raises:  
      >  HTTPException: Raises 401 is the user is not an admin.

    ### Returns:  
      >  List[UserResponse]: A List of users response models.
    """
    if auth_user.admin == False:
        raise HTTPException(status_code=401, detail="Access permitted only for admins")

    users = user_service.fetch_all(db)
    return users


@route.get("/users/{id}", response_model=UserResponse)
def get_one_user(id: int, db: Session = Depends(get_db), auth_user: User=Depends(manager)):
    """
    ## Retrieve one user.

    ### Args:  
      >  id (int): The user ID.

    ### Raises:  
      >  HTTPException: Raises 404 if user was not found.  
      >  HTTPException: Raises 401 is the user is not an admin.

    ### Returns:  
      >  UserResponse: The user response model.
    """
    if auth_user.admin == False:
        raise HTTPException(status_code=401, detail="Access permitted only for admins")

    user = user_service.fetch(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User was not found.")
    return user


@route.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db), auth_user: User=Depends(manager)):
    """
    ## Creates an user.

    ### Args:  
      >  user (UserCreate): The user model.

    ### Raises:  
      >  HTTPException: Raises 401 is the user is not an admin.  
      >  HTTPException: Raises 422 if the email is already in use.  

    ### Returns:  
      >  UserResponse: The user response model.
    """
    if auth_user.admin == False:
        raise HTTPException(status_code=401, detail="Access permitted only for admins")

    try:
        user = user_service.create(db, user)
        return user
    except IntegrityError as err:
        if "email" in repr(err):
            raise HTTPException(status_code=422, detail="Já existe um usuário com este email cadastrado.")


@route.patch("/users/{id}", response_model=UserResponse)
def update_user(id: int, user: UserUpdate, db: Session = Depends(get_db), auth_user: User=Depends(manager)):
    """
    ## Edits an user by id.

    ### Args:  
      >  id (int): The user ID.  
      >  user (UserUpdate): The user model.

    ### Raises:  
      >  HTTPException: Raises 404 if user was not found.  
      >  HTTPException: Raises 401 is the user is not an admin.

    ### Returns:  
      >  UserResponse: The user response model.
    """
    if auth_user.admin == False:
        raise HTTPException(status_code=401, detail="Access permitted only for admins")

    user = user_service.update(db, id, user)
    if not user:
        raise HTTPException(status_code=404, detail="User was not found.")
    return user


@route.delete("/users/{id}", response_model=UserResponse)
def delete_user(id: int, db: Session = Depends(get_db), auth_user: User=Depends(manager)):
    """
    ## Deletes an user by id.

    ### Args:  
      >  id (int): The user ID.

    ### Raises:  
      >  HTTPException: Raises 404 if user was not found.  
      >  HTTPException: Raises 401 is the user is not an admin.

    ### Returns:  
      >  UserResponse: The user response model.
    """
    if auth_user.admin == False:
        raise HTTPException(status_code=401, detail="Access permitted only for admins")

    user = user_service.delete(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User was not found.")
    return user