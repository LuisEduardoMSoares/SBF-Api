# Typing Imports
from typing import List
from sqlalchemy.orm import Session

# User Model
from app.modules.users.models import User

# Provider Model and Schemas
from .models import Provider
from .schemas import ProviderCreate
from .schemas import ProviderUpdate
from .schemas import ProviderResponse


class ProviderService:
    # async def fetch_all(self, db: Session) -> List[UserResponse]:
    #     """
    #     Retrieve a list of users.

    #     Args:
    #         db (Session): The database session.

    #     Returns:
    #         List[UserResponse]: A List of users response models.
    #     """
    #     users = db.query(User).all()
    #     return users

    # async def fetch(self, db: Session, id: int) -> UserResponse:
    #     """
    #     Retrieve one user.

    #     Args:
    #         db (Session): The database session.
    #         id (int): The user ID.

    #     Raises:
    #         HTTPException: Raises 404 if user was not found.

    #     Returns:
    #         UserResponse: The user response model.
    #     """
    #     single_user = db.query(User).get(id)
    #     return single_user

    async def create(self, db: Session, user: User, provider: ProviderCreate) -> ProviderResponse:
        """
        Creates a provider.

        Args:
            db (Session): The database session.
            user (User): The user model.
            provider (ProviderCreate): The provider create model.

        Returns:
            ProviderResponse: The provider response model.
        """
        provider_create = Provider(**provider.dict())
        provider_create.created_by = user.id
        provider = provider_create.insert(db)

        return ProviderResponse.from_orm(provider)

    # async def update(self, db: Session, id: int, user: UserUpdate) -> UserResponse:
    #     """
    #     Edits an user by id.

    #     Args:
    #         db (Session): The database session.
    #         id (int): The user ID.
    #         user (UserUpdate): The user update model.

    #     Returns:
    #         UserResponse: The User Response model.
    #     """        
    #     original_user = db.query(User).get(id)
    #     if not original_user:
    #         return None

    #     original_user.update(db, **user.dict(exclude_unset=True))
    #     new_user = UserResponse.from_orm(original_user)
    #     return new_user

    # async def delete(self, db: Session, id: int) -> UserResponse:
    #     """
    #     Deletes an user by id.

    #     Args:
    #         id (int): The user ID.

    #     Returns:
    #         UserResponse: The User Response model.
    #     """        
    #     deleted_user = db.query(User).get(id)
    #     if not deleted_user:
    #         return None

    #     deleted_user.delete(db)
    #     return deleted_user