# Standard Imports
from sqlalchemy import and_, func
from pydantic import parse_obj_as
from sqlalchemy_filters import apply_pagination

# Typing Imports
from typing import List
from sqlalchemy.orm import Session
from pydantic.types import PositiveInt

# Exception Imports
from sqlalchemy_filters.exceptions import InvalidPage
from ...utils.exceptions import ItensNotFound
from ...utils.exceptions import InvalidPageItemsNumber

# User Model
from app.modules.users.models import User

# Provider Model and Schemas
from .models import Provider
from .schemas import ProviderCreate
from .schemas import ProviderUpdate
from .schemas import ProviderResponse
from .schemas import ProvidersResponse

# Pagination Metadata Schema
from ...utils.pagination import make_pagination_metadata


class ProviderService:
    def fetch_all(self, db: Session, page: int = 0, per_page: PositiveInt = 20, name: str = '') -> ProvidersResponse:
        """
        Retrieve a list of providers, if the page argument is setted
        to 0, the function returns will contains all data, filtered
        by name if setted though.

        Args:
            db (Session): The database session.
            page (int): Page to fetch.
            per_page (int): Quantity of providers per page.
            name (str): Provider name.

        Raises:
            InvalidPage: If the page informed is invalid.
            ItensNotFound: If no item was found.
            InvalidPageItemsNumber: Numbers of items per page must be greater than 0.

        Returns:
            List[ProviderResponse]: A List of providers response models.
        """
        if page == 0:
            providers = db.query(Provider).filter(
                Provider.is_deleted == False,
                func.lower(Provider.name).contains(name.lower(), autoescape=True)
            ).order_by(Provider.id).all()
            providers = parse_obj_as(List[ProviderResponse], providers)

            if len(providers) == 0:
                raise ItensNotFound("No providers found")

            response = ProvidersResponse(
                records = providers
            )

        else:
            if page < 0:
                raise InvalidPage(f"Page number should be positive: {page}")
            if per_page <= 0:
                raise InvalidPageItemsNumber(f"Numbers of items per page must be greater than 0")

            query = db.query(Provider).filter(
                Provider.is_deleted == False,
                func.lower(Provider.name).contains(name.lower(), autoescape=True)
            ).order_by(Provider.id)

            query, pagination = apply_pagination(query, page_number=page, page_size=per_page)
            providers = parse_obj_as(List[ProviderResponse], query.all())

            if len(providers) == 0:
                raise ItensNotFound("No providers found")
            if page > pagination.num_pages:
                raise InvalidPage(f"Page number invalid, the total of pages is {pagination.num_pages}: {page}")

            pagination_metadata = make_pagination_metadata(
                current_page=page,
                total_pages=pagination.num_pages,
                per_page=per_page,
                total_items=pagination.total_results,
                name_filter=name
            )
            response = ProvidersResponse(
                pagination_metadata = pagination_metadata,
                records = providers
            )

        return response

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