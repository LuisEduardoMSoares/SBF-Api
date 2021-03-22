# Standard Imports
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

# Database Import
from app.db.engine import get_db

# Typing Imports
from typing import List

# Authentication Imports
from ..users.models import User
from app.core.auth import manager

# User Schemas
from .services import ProviderService
from .schemas import ProviderCreate
from .schemas import ProviderUpdate
from .schemas import ProviderResponse



route = APIRouter()
provider_service = ProviderService()



@route.get("/providers/", response_model=List[ProviderResponse])
def get_all_providers(db: Session = Depends(get_db), user: User=Depends(manager)):
    """
    ## Retrieve a list of providers.

    ### Returns:  
      >  List[ProviderResponse]: A List of providers response models.
    """
    providers = provider_service.fetch_all(db)
    return providers


@route.get("/providers/{id}", response_model=ProviderResponse)
def get_one_provider(id: int, db: Session = Depends(get_db), user: User=Depends(manager)):
    """
    ## Retrieve one provider.

    ### Args:  
      >  id (int): The provider ID.

    ### Raises:  
      >  HTTPException: Raises 404 if provider was not found.

    ### Returns:  
      >  ProviderResponse: The provider response model.
    """
    provider = provider_service.fetch(db, id)
    if not provider:
        raise HTTPException(status_code=404, detail=f"Fornecedor de id {id} não foi encontrado.")
    return provider


@route.post("/providers/", status_code=201, response_model=ProviderResponse)
def create_provider(provider: ProviderCreate, db: Session = Depends(get_db), user: User=Depends(manager)):
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


@route.patch("/providers/{id}", response_model=ProviderResponse)
def update_provider(id: int, provider: ProviderUpdate, db: Session = Depends(get_db), user: User=Depends(manager)):
    """
    ## Edits a provider by id.

    ### Args:  
      >  id (int): The provider ID.  
      >  provider (ProviderUpdate): The provider update model.

    ### Raises:  
      >  HTTPException: Raises 404 if provider was not found.

    ### Returns:  
      >  ProviderResponse: The provider response model.
    """
    provider = provider_service.update(db, id, provider)
    if not provider:
        raise HTTPException(status_code=404, detail=f"Fornecedor de id {id} não foi encontrado.")
    return provider


@route.delete("/providers/{id}", response_model=ProviderResponse)
def delete_provider(id: int, db: Session = Depends(get_db), user: User=Depends(manager)):
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