# Standard Imports
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from fastapi import Path, Query

# Database Import
from app.db.engine import get_db

# Typing Imports
from sqlalchemy.orm import Session
from typing import Optional

# Exception Imports
from sqlalchemy.exc import IntegrityError
from sqlalchemy_filters.exceptions import InvalidPage
from ...utils.exceptions import ItensNotFound
from ...utils.exceptions import InvalidPageItemsNumber

# Authentication Imports
from ..users.models import User
from app.core.auth import manager

# User Schemas
from .services import ProviderService
from .schemas import TransactionTypeEnum
from .schemas import IncomingProductsData
from .schemas import IncomingTransactionCreate



route = APIRouter()
provider_service = ProviderService()



# @route.get("/providers/", response_model_exclude_unset=True, response_model=ProvidersResponse)
# def get_all_providers(db: Session = Depends(get_db), user: User=Depends(manager), name: Optional[str] = ''):
#     """
#     ## Retrieve all providers.

#     ### Args:  
#       >  id (int): The provider ID.   
#       >  name (str): Provider name to filter.

#     ### Returns:  
#       >  ProvidersResponse: A dict with providers records.
#     """
#     try:
#         providers = provider_service.fetch_all(db, name)
#         return providers
#     except ItensNotFound:
# 	      raise HTTPException(status_code=404, detail="Nenhum fornecedor foi encontrado.")


# @route.get("/providers/page/{page}", response_model=ProvidersResponse)
# def get_all_providers_in_current_page(page: int = Path(..., gt=0), per_page: int = Query(default=20, gt=0),
#     name: Optional[str] = '', db: Session = Depends(get_db), user: User=Depends(manager)):
#     """
#     ## Retrieve all providers in current page.

#     ### Args:  
#       >  id (int): The provider ID.  
#       >  page (int): Page to fetch.  
#       >  per_page (int): Amount of providers per page.  
#       >  name (str): Provider name to filter.

#     ### Returns:  
#       >  ProvidersResponse: A dict with providers records and pagination metadata.
#     """
#     try:
#         providers = provider_service.fetch_all_with_pagination(db, page, per_page, name)
#         return providers
#     except InvalidPage:
# 	      raise HTTPException(status_code=400, detail="Não foi possivel recuperar os itens na página informada.")
#     except InvalidPageItemsNumber:
# 	      raise HTTPException(status_code=400, detail="Quantidade de itens por pagina precisa ser maior que zero.")
#     except ItensNotFound:
# 	      raise HTTPException(status_code=404, detail="Nenhum fornecedor foi encontrado.")


# @route.get("/providers/{id}", response_model=ProviderResponse)
# def get_one_provider(id: int, db: Session = Depends(get_db), user: User=Depends(manager)):
#     """
#     ## Retrieve one provider.

#     ### Args:  
#       >  id (int): The provider ID.

#     ### Raises:  
#       >  HTTPException: Raises 404 if provider was not found.

#     ### Returns:  
#       >  ProviderResponse: The provider response model.
#     """
#     provider = provider_service.fetch(db, id)
#     if not provider:
#         raise HTTPException(status_code=404, detail=f"Fornecedor de id {id} não foi encontrado.")
#     return provider


@route.post("/providers/", status_code=201, response_model=ProviderResponse)
def create_provider(provider: IncomingTransactionCreate, db: Session = Depends(get_db), user: User=Depends(manager)):
    """
    ## Creates a provider.

    ### Args:  
      >  provider (ProviderCreate): The provider create model.

    ### Returns:  
      >  ProviderResponse: The provider response model.
    """
    try:
        provider = provider_service.create(db, user, provider)
        return provider
    except IntegrityError as err:
        if "base_providers_cnpj_key" in repr(err):
            raise HTTPException(status_code=422, detail="Já existe um fornecedor com o CNPJ informado cadastrado.")


# @route.patch("/providers/{id}", response_model=ProviderResponse)
# def update_provider(id: int, provider: ProviderUpdate, db: Session = Depends(get_db), user: User=Depends(manager)):
#     """
#     ## Edits a provider by id.

#     ### Args:  
#       >  id (int): The provider ID.  
#       >  provider (ProviderUpdate): The provider update model.

#     ### Raises:  
#       >  HTTPException: Raises 404 if provider was not found.

#     ### Returns:  
#       >  ProviderResponse: The provider response model.
#     """
#     provider = provider_service.update(db, id, provider)
#     if not provider:
#         raise HTTPException(status_code=404, detail=f"Fornecedor de id {id} não foi encontrado.")
#     return provider


# @route.delete("/providers/{id}", response_model=ProviderResponse)
# def delete_provider(id: int, db: Session = Depends(get_db), user: User=Depends(manager)):
    """
    ## Deletes a provider by id.

    ### Args:  
      >  id (int): The provider ID.

    ### Raises:  
      >  HTTPException: Raises 404 if provider was not found.

    ### Returns:  
      >  UserResponse: The user response model.
    """
    provider = provider_service.delete(db, id)
    if not provider:
        raise HTTPException(status_code=404, detail=f"Fornecedor de id {id} não foi encontrado.")
    return provider