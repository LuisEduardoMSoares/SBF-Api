# Typing Imports
from typing import List
from sqlalchemy.orm import Session

# User Model and Schemas
from .models import User
from .schemas import UserCreate
from .schemas import UserUpdate
from .schemas import UserResponse


class UserService:
    def fetch_all(self, db: Session) -> List[UserResponse]:
        """
        Retrieve a list of users.

        Args:
            db (Session): The database session.

        Returns:
            List[UserResponse]: A List of users response models.
        """
        users = db.query(User).all()
        return users

    def fetch(self, db: Session, id: int) -> UserResponse:
        """
        Retrieve one user.

        Args:
            db (Session): The database session.
            id (int): The user ID.

        Raises:
            HTTPException: Raises 404 if user was not found.

        Returns:
            UserResponse: The user response model.
        """
        single_user = db.query(User).get(id)
        return single_user

    def create(self, db: Session, user: UserCreate) -> UserResponse:
        """
        Creates an user.

        Args:
            db (Session): The database session.
            user (UserCreate): The user create model.

        Returns:
            UserResponse: The user response model.
        """
        user_create = User(**user.dict())
        user_create.hash_password()
        user = user_create.insert(db)

        return UserResponse.from_orm(user)

    def update(self, db: Session, id: int, user: UserUpdate) -> UserResponse:
        """
        Edits an user by id.

        Args:
            db (Session): The database session.
            id (int): The user ID.
            user (UserUpdate): The user update model.

        Returns:
            UserResponse: The User Response model.
        """        
        original_user = db.query(User).get(id)
        if not original_user:
            return None

        if user.password != None:
            original_user.password = user.password
            original_user.hash_password()
            user.password = original_user.password
        original_user.update(db, **user.dict(exclude_unset=True))
        new_user = UserResponse.from_orm(original_user)
        return new_user

    def delete(self, db: Session, id: int) -> UserResponse:
        """
        Deletes an user by id.

        Args:
            id (int): The user ID.

        Returns:
            UserResponse: The User Response model.
        """        
        deleted_user = db.query(User).get(id)
        if not deleted_user:
            return None

        deleted_user.delete(db)
        return deleted_user