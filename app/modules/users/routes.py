# Standard Imports
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

# Database Import
from app.db.engine import get_db

# Typing Imports
from typing import List

# User Schemas
from .services import UserService
from .schemas import UserCreate
from .schemas import UserUpdate
from .schemas import UserResponse



route = APIRouter()
user_service = UserService()



@route.get("/users/", response_model=List[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    """
    ## Retrieve a list of users.

    ### Returns:  
      >  List[UserResponse]: A List of users response models.
    """
    users = await user_service.fetch_all(db)
    return users


@route.get("/users/{id}", response_model=UserResponse)
async def get_one_user(id: int, db: Session = Depends(get_db)):
    """
    ## Retrieve one user.

    ### Args:  
      >  id (int): The user ID.

    ### Raises:  
      >  HTTPException: Raises 404 if user was not found.

    ### Returns:  
      >  UserResponse: The user response model.
    """
    user = await user_service.fetch(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User was not found.")
    return user


@route.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    ## Creates an user.

    ### Args:  
      >  user (UserCreate): The user update model.

    ### Returns:  
      >  UserResponse: The user response model.
    """
    user = await user_service.create(db, user)
    return user


@route.patch("/users/{id}", response_model=UserResponse)
async def update_user(id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """
    ## Edits an user by id.

    ### Args:  
      >  id (int): The user ID.  
      >  user (UserUpdate): The user update model.

    ### Raises:  
      >  HTTPException: Raises 404 if user was not found.

    ### Returns:  
      >  UserResponse: The user response model.
    """
    user = await user_service.update(db, id, user)
    if not user:
        raise HTTPException(status_code=404, detail="User was not found.")
    return user


@route.delete("/users/{id}", response_model=UserResponse)
async def delete_user(id: int, db: Session = Depends(get_db)):
    """
    ## Deletes an user by id.

    ### Args:  
      >  id (int): The user ID.

    ### Raises:  
      >  HTTPException: Raises 404 if user was not found.

    ### Returns:  
      >  UserResponse: The user response model.
    """
    user = await user_service.delete(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User was not found.")
    return user