# Standard Imports
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

# Database Import
from app.db.engine import get_db

# Typing Imports
from typing import List
from typing import Optional
from sqlalchemy.orm import Session

# Exception Imports
from ...utils.exceptions import ItensNotFound
from ...utils.exceptions import InvalidStockQuantity
from ...utils.exceptions import NotEnoughStockQuantity
from ...utils.exceptions import ProviderNotFound

# Authentication Imports
from ..users.models import User
from app.core.auth import manager

# User Schemas
from .services import TransactionService
from .schemas import IncomingTransactionCreate, OutgoingTransactionCreate
from .schemas import IncomingTransactionResponse, OutgoingTransactionResponse
from .schemas import TransactionResponse



route = APIRouter()
transaction_service = TransactionService()



@route.get("/transaction/", response_model_exclude_unset=True, response_model=List[TransactionResponse])
def get_all_transactions(db: Session = Depends(get_db), user: User=Depends(manager), name: Optional[str] = ''):
    """
    ## Retrieve all transactions.

    ### Args:  
      >  id (int): The transaction ID.   
      >  name (str): Transaction name to filter.

    ### Returns:  
      >  TransactionsResponse: A dict with transactions records.
    """
    try:
        providers = transaction_service.fetch_all(db, name)
        return providers
    except ItensNotFound:
	    raise HTTPException(status_code=404, detail="Nenhuma movimentação foi encontrada.")


# @route.get("/providers/page/{page}", response_model=TransactionsResponse)
# def get_all_providers_in_current_page(page: int = Path(..., gt=0), per_page: int = Query(default=20, gt=0),
#     name: Optional[str] = '', db: Session = Depends(get_db), user: User=Depends(manager)):
#     """
#     ## Retrieve all providers in current page.

#     ### Args:  
#       >  id (int): The provider ID.  
#       >  page (int): Page to fetch.  
#       >  per_page (int): Amount of providers per page.  
#       >  name (str): Transaction name to filter.

#     ### Returns:  
#       >  TransactionsResponse: A dict with providers records and pagination metadata.
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


# @route.get("/providers/{id}", response_model=TransactionResponse)
# def get_one_provider(id: int, db: Session = Depends(get_db), user: User=Depends(manager)):
#     """
#     ## Retrieve one provider.

#     ### Args:  
#       >  id (int): The provider ID.

#     ### Raises:  
#       >  HTTPException: Raises 404 if provider was not found.

#     ### Returns:  
#       >  TransactionResponse: The provider response model.
#     """
#     provider = provider_service.fetch(db, id)
#     if not provider:
#         raise HTTPException(status_code=404, detail=f"Fornecedor de id {id} não foi encontrado.")
#     return provider


# @route.post("/transaction/", status_code=201, response_model=TransactionResponse, response_model_exclude_none=True)
# def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db), user: User=Depends(manager)):
#     """
#     ## Creates a transaction.

#     ### Args:  
#       >  transaction (TransactionCreate): The transaction create model.

#     ### Returns:  
#       >  TransactionResponse: The transaction response model.
#     """
#     try:
#         transaction = transaction_service.create(db, user, transaction)
#         return transaction
#     except ItensNotFound as err:
# 	    raise HTTPException(status_code=400, detail=f"Os seguintes produtos não foram encontrados no sistema: {str(err)}")
#     except InvalidStockQuantity as err:
# 	    raise HTTPException(status_code=400, detail=f"Quantidade de estoque para os seguintes produtos deve ser maior do que zero: {str(err)}")
#     except NotEnoughStockQuantity as err:
# 	    raise HTTPException(status_code=400, detail=f"Quantidade de estoque para os seguintes produtos não possuem quantidade suficiente para a saída: {str(err)}")


@route.post("/incoming/transaction/", status_code=201, response_model=IncomingTransactionResponse, response_model_exclude_none=True)
def create_incoming_transaction(transaction: IncomingTransactionCreate, db: Session = Depends(get_db), user: User=Depends(manager)):
    """
    ## Creates an incoming transaction.

    ### Args:  
      >  transaction (IncomingTransactionCreate): The incoming transaction create model.

    ### Returns:  
      >  IncomingTransactionResponse: The incoming transaction response model.
    """
    try:
        transaction = transaction_service.create(db, user, transaction)
        return transaction
    except ProviderNotFound as err:
	    raise HTTPException(status_code=404, detail=f"O fornecedor informado não foi encontrado: {str(err)}")
    except ItensNotFound as err:
	    raise HTTPException(status_code=404, detail=f"Os seguintes produtos não foram encontrados no sistema: {str(err)}")
    except InvalidStockQuantity as err:
	    raise HTTPException(status_code=400, detail=f"A quantidade de estoque para os seguintes produtos deve ser maior do que zero: {str(err)}")


@route.post("/outgoing/transaction/", status_code=201, response_model=OutgoingTransactionResponse, response_model_exclude_none=True)
def create_outgoing_transaction(transaction: OutgoingTransactionCreate, db: Session = Depends(get_db), user: User=Depends(manager)):
    """
    ## Creates an outgoing transaction.

    ### Args:  
      >  transaction (OutgoingTransactionCreate): The outgoing transaction create model.

    ### Returns:  
      >  OutgoingTransactionResponse: The outgoing transaction response model.
    """
    try:
        transaction = transaction_service.create(db, user, transaction)
        return transaction
    except ItensNotFound as err:
	    raise HTTPException(status_code=404, detail=f"Os seguintes produtos não foram encontrados no sistema: {str(err)}")
    except InvalidStockQuantity as err:
	    raise HTTPException(status_code=400, detail=f"A quantidade informada para os seguintes produtos deve ser maior do que zero: {str(err)}")
    except NotEnoughStockQuantity as err:
	    raise HTTPException(status_code=422, detail=f"Os produtos informados não possuem quantidade em estoque suficiente para a saída: {str(err)}")
