# Standard Imports
from time import time as timestamp
from sqlalchemy.sql.expression import and_

# Typing Imports
from typing import List
from sqlalchemy.orm import Session

# User Model and Schemas
from .models import User
from .schemas import UserCreate
from .schemas import UserUpdate
from .schemas import UserResponse


class UserService:
    def fetch_all(self, db: Session, only_admin=False) -> List[UserResponse]:
        """
        Retrieve a list of users.

        Args:
            db (Session): The database session.

        Returns:
            List[UserResponse]: A List of users response models.
        """
        users = db.query(User).filter(
            User.is_deleted == False
        )

        if only_admin == True:
            users = users.filter(User.admin == True)

        return users.all()

    def fetch(self, db: Session, id: int) -> UserResponse:
        """
        Retrieve one user.

        Args:
            db (Session): The database session.
            id (int): The user ID.

        Returns:
            UserResponse: The user response model.
        """
        single_user = db.query(User).filter(and_(
            User.id == id,
            User.is_deleted == False
        )).first()
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
        db_user = db.query(User).filter(and_(
            User.id == id,
            User.is_deleted == False
        )).first()
        if not db_user:
            return None

        if user.password != None:
            db_user.password = user.password
            db_user.hash_password()
            user.password = db_user.password

        db_user.update(db, **user.dict(exclude_unset=True))
        new_user = UserResponse.from_orm(db_user)
        return new_user

    def delete(self, db: Session, id: int) -> UserResponse:
        """
        Deletes an user by id.

        Args:
            id (int): The user ID.

        Returns:
            UserResponse: The User Response model.
        """        
        db_user = db.query(User).filter(and_(
            User.id == id,
            User.is_deleted == False
        )).first()
        if not db_user:
            return None

        db_user.update(db, is_deleted=True, email=f'{timestamp()}_{db_user.email}')
        db_user = UserResponse.from_orm(db_user)
        return db_user