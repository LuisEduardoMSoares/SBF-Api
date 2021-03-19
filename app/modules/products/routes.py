# Standard Imports
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

# Database Import
from app.db.engine import get_db

# Typing Imports
from typing import List

# Authentication Imports
from ..users.models import User
from app.core.auth import manager

# Product Schemas
from .services import ProductService
from .schemas import ProductCreate
from .schemas import ProductUpdate
from .schemas import ProductResponse



route = APIRouter()
product_service = ProductService()



@route.get("/products/", response_model=List[ProductResponse])
async def get_all_products(db: Session = Depends(get_db), user: User=Depends(manager)):
    """
    ## Retrieve a list of products.

    ### Returns:  
      >  List[ProductResponse]: A List of products response models.
    """
    products = await product_service.fetch_all(db)
    return products


@route.get("/products/{id}", response_model=ProductResponse)
async def get_one_product(id: int, db: Session = Depends(get_db), user: User=Depends(manager)):
    """
    ## Retrieve one product.

    ### Args:  
      >  id (int): The product ID.

    ### Raises:  
      >  HTTPException: Raises 404 if product was not found.

    ### Returns:  
      >  ProductResponse: The product response model.
    """
    product = await product_service.fetch(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return product


@route.post("/products/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: Session = Depends(get_db), user: User=Depends(manager)):
    """
    ## Creates an product.

    ### Args:  
      >  product (ProductCreate): The product update model.

    ### Returns:  
      >  ProductResponse: The product response model.
    """
    product = await product_service.create(db, product, user)
    return product


@route.patch("/products/{id}", response_model=ProductResponse)
async def update_product(id: int, product: ProductUpdate, db: Session = Depends(get_db), user: User=Depends(manager)):
    """
    ## Edits an product by id.

    ### Args:  
      >  id (int): The product ID.  
      >  product (ProductUpdate): The product update model.

    ### Raises:  
      >  HTTPException: Raises 404 if product was not found.

    ### Returns:  
      >  ProductResponse: The product response model.
    """
    product = await product_service.update(db, id, product)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return product


@route.delete("/products/{id}", response_model=ProductResponse)
async def delete_product(id: int, db: Session = Depends(get_db), user: User=Depends(manager)):
    """
    ## Deletes an product by id.

    ### Args:  
      >  id (int): The product ID.

    ### Raises:  
      >  HTTPException: Raises 404 if product was not found.

    ### Returns:  
      >  ProductResponse: The product response model.
    """
    product = await product_service.delete(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return product