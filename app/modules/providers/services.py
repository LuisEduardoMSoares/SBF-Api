# Standard Imports
from sqlalchemy import and_

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
    def fetch_all(self, db: Session) -> List[ProviderResponse]:
        """
        Retrieve a list of providers.

        Args:
            db (Session): The database session.

        Returns:
            List[ProviderResponse]: A List of providers response models.
        """
        providers = db.query(Provider).filter(
            Provider.is_deleted==False
        ).all()
        return providers

    def fetch(self, db: Session, id: int) -> ProviderResponse:
        """
        Retrieve one provider.

        Args:
            db (Session): The database session.
            id (int): The provider ID.

        Returns:
            ProviderResponse: The provider response model.
        """
        provider = db.query(Provider).filter(and_(
            Provider.id == id,
            Provider.is_deleted == False
        )).first()
        return provider

    def create(self, db: Session, user: User, provider: ProviderCreate) -> ProviderResponse:
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

    def update(self, db: Session, id: int, provider: ProviderUpdate) -> ProviderResponse:
        """
        Edits a provider by id.

        Args:
            db (Session): The database session.
            id (int): The provider ID.
            provider (ProviderUpdate): The provider update model.

        Returns:
            ProviderResponse: The provider response model.
        """
        original_provider = db.query(Provider).filter(and_(
            Provider.id == id,
            Provider.is_deleted == False
        )).first()
        if not original_provider:
            return None

        original_provider.update(db, **provider.dict(exclude_unset=True))
        updated_provider = ProviderResponse.from_orm(original_provider)
        return updated_provider

    def delete(self, db: Session, id: int) -> ProviderResponse:
        """
        Deletes a provider by id.

        Args:
            id (int): The provider ID.

        Returns:
            ProviderResponse: The provider response model.
        """
        original_provider = db.query(Provider).filter(and_(
            Provider.id == id,
            Provider.is_deleted == False
        )).first()
        if not original_provider:
            return None

        original_provider.is_deleted = True
        original_provider.update(db)
        disable_provider = ProviderResponse.from_orm(original_provider)
        return disable_provider