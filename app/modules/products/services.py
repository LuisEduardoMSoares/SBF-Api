# Typing Imports
from typing import List
from sqlalchemy.orm import Session

# User Model
from app.modules.users.models import User

# Product Model and Schemas
from .models import Product
from .schemas import ProductCreate
from .schemas import ProductUpdate
from .schemas import ProductResponse


class ProductService:
    async def fetch_all(self, db: Session) -> List[ProductResponse]:
        """
        Retrieve a list of products.

        Args:
            db (Session): The database session.

        Returns:
            List[ProductResponse]: A List of products response models.
        """
        products = db.query(Product).all()
        return products

    async def fetch(self, db: Session, id: int) -> ProductResponse:
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
        single_product = db.query(Product).get(id)
        return single_product

    async def create(self, db: Session, product: ProductCreate, user: User) -> ProductResponse:
        """
        Creates an product.

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

    async def update(self, db: Session, id: int, product: ProductUpdate) -> ProductResponse:
        """
        Edits an product by id.

        Args:
            db (Session): The database session.
            id (int): The product ID.
            product (ProductUpdate): The product update model.

        Returns:
            ProductResponse: The Product Response model.
        """        
        original_product = db.query(Product).get(id)
        if not original_product:
            return None

        original_product.update(db, **product.dict(exclude_unset=True))
        new_product = ProductResponse.from_orm(original_product)
        return new_product

    async def delete(self, db: Session, id: int) -> ProductResponse:
        """
        Deletes an product by id.

        Args:
            id (int): The product ID.

        Returns:
            ProductResponse: The Product Response model.
        """        
        deleted_product = db.query(Product).get(id)
        if not deleted_product:
            return None

        deleted_product.is_deleted = True
        deleted_product.update(db, **deleted_product.__dict__)
        return deleted_product