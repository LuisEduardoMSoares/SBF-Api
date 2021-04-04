# Standard Import
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

# Product Model and Schemas
from .models import Product
from .schemas import ProductCreate
from .schemas import ProductUpdate
from .schemas import ProductResponse
from .schemas import ProductsResponse

# Pagination Metadata Schema
from ...utils.pagination import make_pagination_metadata


class ProductService:
    def fetch_all(self, db: Session, page: int = 0, per_page: PositiveInt = 20, name: str = '') -> ProductsResponse:
        """
        Retrieve a list of products, if the page argument is setted
        to 0, the function returns will contains all data, filtered
        by name if setted though.

        Args:
            db (Session): The database session.
            page (int): Page to fetch.
            per_page (int): Quantity of products per page.
            name (str): Product name.

        Raises:
            InvalidPage: If the page informed is invalid.
            ItensNotFound: If no item was found.
            InvalidPageItemsNumber: Numbers of items per page must be greater than 0.

        Returns:
            List[ProductResponse]: A List of products response models.
        """
        if page == 0:
            products = db.query(Product).filter(
                Product.is_deleted == False,
                func.lower(Product.name).contains(name.lower(), autoescape=True)
            ).order_by(Product.id).all()
            products = parse_obj_as(List[ProductResponse], products)

            if len(products) == 0:
                raise ItensNotFound("No products found")

            response = ProductsResponse(
                records = products
            )

        else:
            if page < 0:
                raise InvalidPage(f"Page number should be positive: {page}")
            if per_page <= 0:
                raise InvalidPageItemsNumber(f"Numbers of items per page must be greater than 0")

            query = db.query(Product).filter(
                Product.is_deleted == False,
                func.lower(Product.name).contains(name.lower(), autoescape=True)
            ).order_by(Product.id)

            query, pagination = apply_pagination(query, page_number=page, page_size=per_page)
            products = parse_obj_as(List[ProductResponse], query.all())

            if len(products) == 0:
                raise ItensNotFound("No products found")
            if page > pagination.num_pages:
                raise InvalidPage(f"Page number invalid, the total of pages is {pagination.num_pages}: {page}")

            pagination_metadata = make_pagination_metadata(
                current_page=page,
                total_pages=pagination.num_pages,
                per_page=per_page,
                total_items=pagination.total_results,
                name_filter=name
            )
            response = ProductsResponse(
                pagination_metadata = pagination_metadata,
                records = products
            )

        return response

    def fetch(self, db: Session, id: int) -> ProductResponse:
        """
        Retrieve one product.

        Args:
            db (Session): The database session.
            id (int): The product ID.

        Raises:
            HTTPException: Raises 404 if product was not found.

        Returns:
            ProductResponse: The product response model.
        """
        single_product = db.query(Product).filter(and_(
            Product.id == id,
            Product.is_deleted == False
        )).first()
        return single_product

    def create(self, db: Session, product: ProductCreate, user: User) -> ProductResponse:
        """
        Creates a product.

        Args:
            db (Session): The database session.
            product (ProductCreate): The product create model.

        Returns:
            ProductResponse: The product response model.
        """
        product_create = Product(**product.dict())
        product_create.created_by = user.id
        product = product_create.insert(db)

        return ProductResponse.from_orm(product)

    def update(self, db: Session, id: int, product: ProductUpdate) -> ProductResponse:
        """
        Edits a product by id.

        Args:
            db (Session): The database session.
            id (int): The product ID.
            product (ProductUpdate): The product update model.

        Returns:
            ProductResponse: The Product Response model.
        """        
        original_product = db.query(Product).filter(and_(
            Product.id == id,
            Product.is_deleted == False
        )).first()
        if not original_product:
            return None

        original_product.update(db, **product.dict(exclude_unset=True))
        new_product = ProductResponse.from_orm(original_product)
        return new_product

    def delete(self, db: Session, id: int) -> ProductResponse:
        """
        Deletes a product by id.

        Args:
            id (int): The product ID.

        Returns:
            ProductResponse: The Product Response model.
        """        
        deleted_product = db.query(Product).filter(and_(
            Product.id == id,
            Product.is_deleted == False
        )).first()
        if not deleted_product:
            return None

        deleted_product.is_deleted = True
        deleted_product.update(db)
        return deleted_product