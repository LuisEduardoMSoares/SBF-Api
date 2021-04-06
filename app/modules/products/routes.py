# Standard Imports
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

# Database Import
from app.db.engine import get_db

# Typing Imports
from sqlalchemy.orm import Session
from typing import Optional

# Exception Imports
from sqlalchemy_filters.exceptions import InvalidPage
from ...utils.exceptions import ItensNotFound
from ...utils.exceptions import InvalidPageItemsNumber

# Authentication Imports
from ..users.models import User
from app.core.auth import manager

# Product Schemas
from .services import ProductService
from .schemas import ProductCreate
from .schemas import ProductUpdate
from .schemas import ProductResponse
from .schemas import ProductsResponse



route = APIRouter()
product_service = ProductService()



@route.get("/products/", response_model_exclude_unset=True, response_model=ProductsResponse)
def get_all_products(db: Session = Depends(get_db), user: User=Depends(manager), name: Optional[str] = ''):
    """
    ## Retrieve all products.

    ### Args:  
      >  id (int): The product ID.   
      >  name (str): Product name to filter.

    ### Returns:  
      >  ProductsResponse: A dict with products records.
    """
    try:
        products = product_service.fetch_all(db, name)
        return products
    except ItensNotFound:
	      raise HTTPException(status_code=404, detail="Nenhum produto foi encontrado.")


@route.get("/products/page/{page}", response_model=ProductsResponse)
def get_all_products_in_current_page(page: int, db: Session = Depends(get_db), user: User=Depends(manager), 
    per_page: Optional[int] = 20, name: Optional[str] = ''):
    """
    ## Retrieve all products in current page.

    ### Args:  
      >  id (int): The product ID.  
      >  page (int): Page to fetch.  
      >  per_page (int): Amount of products per page.  
      >  name (str): Product name to filter.

    ### Returns:  
      >  ProductsResponse: A dict with products records and pagination metadata.
    """
    try:
        products = product_service.fetch_all_with_pagination(db, page, per_page, name)
        return products
    except InvalidPage:
	      raise HTTPException(status_code=400, detail="Não foi possivel recuperar os itens na página informada.")
    except InvalidPageItemsNumber:
	      raise HTTPException(status_code=400, detail="Quantidade de itens por pagina precisa ser maior que zero.")
    except ItensNotFound:
	      raise HTTPException(status_code=404, detail="Nenhum produto foi encontrado.")


@route.get("/products/{id}", response_model=ProductResponse)
def get_one_product(id: int, db: Session = Depends(get_db), user: User=Depends(manager)):
    """
    ## Retrieve one product.

    ### Args:  
      >  id (int): The product ID.

    ### Raises:  
      >  HTTPException: Raises 404 if product was not found.

    ### Returns:  
      >  ProductResponse: The product response model.
    """
    product = product_service.fetch(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return product


@route.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db), user: User=Depends(manager)):
    """
    ## Creates a product.

    ### Args:  
      >  product (ProductCreate): The product update model.

    ### Returns:  
      >  ProductResponse: The product response model.
    """
    product = product_service.create(db, product, user)
    return product


@route.patch("/products/{id}", response_model=ProductResponse)
def update_product(id: int, product: ProductUpdate, db: Session = Depends(get_db), user: User=Depends(manager)):
    """
    ## Edits a product by id.

    ### Args:  
      >  id (int): The product ID.  
      >  product (ProductUpdate): The product update model.

    ### Raises:  
      >  HTTPException: Raises 404 if product was not found.

    ### Returns:  
      >  ProductResponse: The product response model.
    """
    product = product_service.update(db, id, product)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return product


@route.delete("/products/{id}", response_model=ProductResponse)
def delete_product(id: int, db: Session = Depends(get_db), user: User=Depends(manager)):
    """
    ## Deletes a product by id.

    ### Args:  
      >  id (int): The product ID.

    ### Raises:  
      >  HTTPException: Raises 404 if product was not found.

    ### Returns:  
      >  ProductResponse: The product response model.
    """
    product = product_service.delete(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return product