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
    def fetch_all(self, db: Session, name: str = '') -> ProvidersResponse:
        """
        Retrieve all providers records.

        Args:
            db (Session): The database session.
            name (str): Provider name to filter.

        Raises:
            ItensNotFound: If no item was found.

        Returns:
            ProvidersResponse: A dict with providers records.
        """
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
        return response

    def fetch_all_with_pagination(self, db: Session, page: int, per_page: int = 20, name: str = '') -> ProvidersResponse:
        """
        Retrieve all providers records listed by page argument and pagination metadata.

        Args:
            db (Session): The database session.
            page (int): Page to fetch.
            per_page (int): Amount of providers per page.
            name (str): Provider name to filter.

        Raises:
            InvalidPage: If the page informed is invalid.
            ItensNotFound: If no item was found.
            InvalidPageItemsNumber: Numbers of items per page must be greater than 0.

        Returns:
            ProvidersResponse: A dict with providers records and pagination metadata.
        """
        if page <= 0:
            raise InvalidPage(f"Page number should be positive and greater than zero: {page}")
        if per_page <= 0:
            raise InvalidPageItemsNumber(f"Numbers of items per page must be greater than zero")

        query = db.query(Provider).filter(
            Provider.is_deleted == False,
            func.lower(Provider.name).contains(name.lower(), autoescape=True)
        ).order_by(Provider.id)

        query, pagination = apply_pagination(query, page_number=page, page_size=per_page)
        providers = parse_obj_as(List[ProviderResponse], query.all())

        if page > pagination.num_pages and pagination.num_pages > 0:
            raise InvalidPage(f"Page number invalid, the total of pages is {pagination.num_pages}: {page}")
        if len(providers) == 0:
            raise ItensNotFound("No providers found")

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