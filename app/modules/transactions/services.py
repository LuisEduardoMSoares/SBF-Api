# Standard Imports
from sqlalchemy import and_, func
from pydantic import parse_obj_as
from sqlalchemy_filters import apply_pagination

# Typing Imports
from typing import List
from sqlalchemy.orm import Session

# Exception Imports
from ...utils.exceptions import ItensNotFound

# User Model
from app.modules.users.models import User

# Product Model
from app.modules.products.models import Product

# Provider Model
from app.modules.providers.models import Provider

# Transaction Model and Schemas
from .models import Transaction
from .schemas import TransactionTypeEnum
from .schemas import TransactionProductsData
from .schemas import TransactionCreate
from .schemas import TransactionResponse

# Transaction Products Model
from ..transactions_products.models import TransactionProduct

# Pagination Metadata Schema
from ...utils.pagination import make_pagination_metadata


class TransactionService:
    def fetch_all(self, db: Session, name: str = '') -> TransactionResponse:
        """
        Retrieve all transactions records.

        Args:
            db (Session): The database session.
            name (str): Transaction name to filter.

        Raises:
            ItensNotFound: If no item was found.

        Returns:
            TransactionsResponse: A dict with transactions records.
        """
        query_result = db.query(Transaction).order_by(Transaction.id).all()
        transactions = parse_obj_as(List[TransactionResponse], query_result)

        if len(transactions) == 0:
            raise ItensNotFound("No transactions found")

        return transactions

    # def fetch_all_with_pagination(self, db: Session, page: int, per_page: int = 20, name: str = '') -> TransactionsResponse:
    #     """
    #     Retrieve all providers records listed by page argument and pagination metadata.

    #     Args:
    #         db (Session): The database session.
    #         page (int): Page to fetch.
    #         per_page (int): Amount of providers per page.
    #         name (str): Transaction name to filter.

    #     Raises:
    #         InvalidPage: If the page informed is invalid.
    #         ItensNotFound: If no item was found.
    #         InvalidPageItemsNumber: Numbers of items per page must be greater than 0.

    #     Returns:
    #         TransactionsResponse: A dict with providers records and pagination metadata.
    #     """
    #     if page <= 0:
    #         raise InvalidPage(f"Page number should be positive and greater than zero: {page}")
    #     if per_page <= 0:
    #         raise InvalidPageItemsNumber(f"Numbers of items per page must be greater than zero")

    #     query = db.query(Transaction).filter(
    #         Transaction.is_deleted == False,
    #         func.lower(Transaction.name).contains(name.lower(), autoescape=True)
    #     ).order_by(Transaction.id)

    #     query, pagination = apply_pagination(query, page_number=page, page_size=per_page)
    #     providers = parse_obj_as(List[TransactionResponse], query.all())

    #     if page > pagination.num_pages and pagination.num_pages > 0:
    #         raise InvalidPage(f"Page number invalid, the total of pages is {pagination.num_pages}: {page}")
    #     if len(providers) == 0:
    #         raise ItensNotFound("No providers found")

    #     pagination_metadata = make_pagination_metadata(
    #         current_page=page,
    #         total_pages=pagination.num_pages,
    #         per_page=per_page,
    #         total_items=pagination.total_results,
    #         name_filter=name
    #     )
    #     response = TransactionsResponse(
    #         pagination_metadata = pagination_metadata,
    #         records = providers
    #     )
    #     return response

    # def fetch(self, db: Session, id: int) -> TransactionResponse:
    #     """
    #     Retrieve one transaction.

    #     Args:
    #         db (Session): The database session.
    #         id (int): The provider ID.

    #     Returns:
    #         TransactionResponse: The provider response model.
    #     """
    #     provider = db.query(Transaction).filter(and_(
    #         Transaction.id == id,
    #         Transaction.is_deleted == False
    #     )).first()
    #     return provider

    def _sort_by_id_check_and_sum_duplicates(self, payload: List[TransactionProductsData]) -> List[TransactionProductsData]:
        already_added = []
        checked_payload = []

        sorted_payload = sorted(payload, key=lambda v: v.product_id) 
        for value in sorted_payload:
            if value.product_id not in already_added:
                already_added.append(value.product_id)
                checked_payload.append(value)

            else:
                checked_payload[-1].quantity += value.quantity
        
        return checked_payload
    
    def _extract_product_id(self, payload: List[TransactionProductsData]) -> List[int]:
        return [value.product_id for value in payload]

    def _check_provider_existence(self, db: Session, provider_id) -> None:
        provider = db.query(Provider).filter(Provider.id == provider_id).first()
        if provider == None:
            raise ItensNotFound('Provider not found')

    def _check_products_existence_and_increment_inventory(self, db: Session, payload: List[TransactionProductsData]) -> None:
        products_ids = [value.product_id for value in payload]
        products = db.query(Product).filter(Product.id.in_(products_ids)).all()

        for product in products:
            if product.id in products_ids:
                products_ids.remove(product.id)
        if len(products_ids) > 0:
            raise ItensNotFound( str(products_ids).replace('[','').replace(']','') )

        # TODO: adicionar feature para incrementar estoque dos produtos
        


    def create(self, db: Session, user: User, transaction: TransactionCreate) -> TransactionResponse:
        """
        Creates a transaction.

        Args:
            db (Session): The database session.
            user (User): The user model.
            transaction (TransactionCreate): The transaction create model.

        Returns:
            TransactionResponse: The provider response model.
        """
        if transaction.type == TransactionTypeEnum.incoming:
            checked_products = self._sort_by_id_check_and_sum_duplicates(transaction.products)
            self._check_provider_existence(db, transaction.provider_id)
            self._check_products_existence_and_increment_inventory(db, checked_products)
            
            transaction_create = Transaction(
                **transaction.dict(exclude_unset=True, exclude={'products'})
            )
            transaction_create.created_by = user.id

            products_transaction = [
                TransactionProduct(
                    quantity = product.quantity,
                    product_id = product.product_id
                ) 
                for product in checked_products
            ]
            transaction_create.products_transaction = products_transaction
            transaction = transaction_create.insert(db)
            
            return TransactionResponse.from_orm(transaction)
        
        else:
            raise NotImplementedError()


    # def update(self, db: Session, id: int, provider: TransactionUpdate) -> TransactionResponse:
    #     """
    #     Edits a provider by id.

    #     Args:
    #         db (Session): The database session.
    #         id (int): The provider ID.
    #         provider (TransactionUpdate): The provider update model.

    #     Returns:
    #         TransactionResponse: The provider response model.
    #     """
    #     original_provider = db.query(Transaction).filter(and_(
    #         Transaction.id == id,
    #         Transaction.is_deleted == False
    #     )).first()
    #     if not original_provider:
    #         return None

    #     original_provider.update(db, **provider.dict(exclude_unset=True))
    #     updated_provider = TransactionResponse.from_orm(original_provider)
    #     return updated_provider

    # def delete(self, db: Session, id: int) -> TransactionResponse:
    #     """
    #     Deletes a provider by id.

    #     Args:
    #         id (int): The provider ID.

    #     Returns:
    #         TransactionResponse: The provider response model.
    #     """
    #     original_provider = db.query(Transaction).filter(and_(
    #         Transaction.id == id,
    #         Transaction.is_deleted == False
    #     )).first()
    #     if not original_provider:
    #         return None

    #     original_provider.is_deleted = True
    #     original_provider.update(db)
    #     disable_provider = TransactionResponse.from_orm(original_provider)
    #     return disable_provider