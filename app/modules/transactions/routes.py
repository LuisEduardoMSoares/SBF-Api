# Standard Imports
from datetime import date
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from fastapi import Path, Query

# Database Import
from app.db.engine import get_db

# Typing Imports
from typing import List
from typing import Optional
from sqlalchemy.orm import Session

# Exception Imports
from sqlalchemy_filters.exceptions import InvalidPage
from ...utils.exceptions import ProductsNotFound
from ...utils.exceptions import ItensNotFound
from ...utils.exceptions import InvalidStockQuantity
from ...utils.exceptions import NotEnoughStockQuantity
from ...utils.exceptions import ProviderNotFound
from ...utils.exceptions import InvalidPageItemsNumber
from ...utils.exceptions import InvalidRangeTime

# Authentication Imports
from ..users.models import User
from app.core.auth import manager

# User Schemas
from .services import TransactionService
from .schemas import IncomingTransactionCreate, OutgoingTransactionCreate
from .schemas import IncomingTransactionResponse, OutgoingTransactionResponse
from .schemas import TransactionResponse, TransactionsResponse
from .schemas import TransactionTypeEnum



route = APIRouter()
transaction_service = TransactionService()


@route.get("/transaction/", response_model_exclude_unset=True, response_model=List[TransactionResponse], response_model_exclude_none=True)
def get_all_transactions( product_name: Optional[str] = '', provider_name: Optional[str] = '',
    description: Optional[str] = '', transaction_type: Optional[TransactionTypeEnum] = '',
    start_date: Optional[date] = '' ,finish_date: Optional[date] = '',
    db: Session = Depends(get_db), auth_user: User=Depends(manager)):
    """
    ## Retrieve all transactions.

    ### Args:   
      >  product_name (str): Product name to filter.  
      >  provider_name (str): Provider name to filter.  
      >  description (str): Description to filter.  
      >  transaction_type (Enum): Transaction type to filter. (ENTRADA/SAIDA)  
      >  start_date (date): Start date to filter. (YYYY-MM-DD)  
      >  finish_date (date): Finish date to filter. (YYYY-MM-DD)

    ### Returns:  
      >  List[TransactionResponse]: A list of dicts with transactions records.
    """
    try:
        transactions = transaction_service.fetch_all(
            db,
            product_name,
            provider_name,
            description,
            transaction_type,
            start_date,
            finish_date
        )
        return transactions
    except ItensNotFound:
	      raise HTTPException(status_code=404, detail="Nenhuma movimentação foi encontrada.")
    except InvalidRangeTime:
	      raise HTTPException(status_code=400, detail=f"A data de inicio {start_date} deve ser menor que a data final {finish_date}.")



@route.get("/transaction/page/{page}", response_model=TransactionsResponse)
def get_all_transactions_in_current_page(page: int = Path(..., gt=0), per_page: int = Query(default=20, gt=0),
    product_name: Optional[str] = '', provider_name: Optional[str] = '',
    description: Optional[str] = '', transaction_type: Optional[TransactionTypeEnum] = '',
    start_date: Optional[date] = '' ,finish_date: Optional[date] = '',
    db: Session = Depends(get_db), auth_user: User=Depends(manager)):
    """
    ## Retrieve all transactions in current page.

    ### Args:  
      >  page (int): Page to fetch.  
      >  per_page (int): Amount of transactions per page.  
      >  product_name (str): Product name to filter.  
      >  provider_name (str): Provider name to filter.  
      >  description (str): Description to filter.  
      >  transaction_type (Enum): Transaction type to filter. (ENTRADA/SAIDA)  
      >  start_date (date): Start date to filter. (YYYY-MM-DD)  
      >  finish_date (date): Finish date to filter. (YYYY-MM-DD)

    ### Returns:  
      >  TransactionsResponse: A dict with transactions records and pagination metadata.
    """
    try:
        providers = transaction_service.fetch_all_with_pagination(
            db,
            page,
            per_page,
            product_name,
            provider_name,
            description,
            transaction_type,
            start_date,
            finish_date
        )
        return providers
    except InvalidPage:
	      raise HTTPException(status_code=400, detail="Não foi possivel recuperar os itens na página informada.")
    except InvalidPageItemsNumber:
	      raise HTTPException(status_code=400, detail="Quantidade de itens por pagina precisa ser maior que zero.")
    except ItensNotFound:
	      raise HTTPException(status_code=404, detail="Nenhuma movimentação encontrada.")
    except InvalidRangeTime:
	      raise HTTPException(status_code=400, detail=f"A data de inicio {start_date} deve ser menor que a data final {finish_date}.")


@route.get("/transaction/{id}", response_model_exclude_unset=True, response_model=TransactionResponse)
def get_one_transaction(id: int, db: Session = Depends(get_db), auth_user: User=Depends(manager)):
    """
    ## Retrieve one transaction by id.

    ### Args:  
      >  id (int): The transaction ID.   

    ### Returns:  
      >  TransactionsResponse: A dict with transaction record.
    """
    try:
        transaction = transaction_service.fetch_one(db, id)
        return transaction
    except ItensNotFound:
	      raise HTTPException(status_code=404, detail=f"Movimentação de id {id} não foi encontrada.")


@route.post("/incoming/transaction/", status_code=201, response_model=IncomingTransactionResponse, response_model_exclude_none=True)
def create_incoming_transaction(transaction: IncomingTransactionCreate, db: Session = Depends(get_db), auth_user: User=Depends(manager)):
    """
    ## Creates an incoming transaction.

    ### Args:  
      >  transaction (IncomingTransactionCreate): The incoming transaction create model.

    ### Returns:  
      >  IncomingTransactionResponse: The incoming transaction response model.
    """
    try:
        transaction = transaction_service.create(db, auth_user, transaction)
        return transaction
    except ProductsNotFound as err:
        raise HTTPException(status_code=400, detail="A movimentação a ser registrada deve conter no minimo um produto.")
    except ProviderNotFound as err:
	      raise HTTPException(status_code=404, detail=f"O fornecedor informado não foi encontrado: {str(err)}")
    except ItensNotFound as err:
	      raise HTTPException(status_code=404, detail=f"Os seguintes produtos não foram encontrados no sistema: {str(err)}")
    except InvalidStockQuantity as err:
	      raise HTTPException(status_code=400, detail=f"A quantidade de estoque para os seguintes produtos deve ser maior do que zero: {str(err)}")


@route.post("/outgoing/transaction/", status_code=201, response_model=OutgoingTransactionResponse, response_model_exclude_none=True)
def create_outgoing_transaction(transaction: OutgoingTransactionCreate, db: Session = Depends(get_db), auth_user: User=Depends(manager)):
    """
    ## Creates an outgoing transaction.

    ### Args:  
      >  transaction (OutgoingTransactionCreate): The outgoing transaction create model.

    ### Returns:  
      >  OutgoingTransactionResponse: The outgoing transaction response model.
    """
    try:
        transaction = transaction_service.create(db, auth_user, transaction)
        return transaction
    except ProductsNotFound as err:
        raise HTTPException(status_code=400, detail="A movimentação a ser registrada deve conter no minimo um produto.")
    except ItensNotFound as err:
	      raise HTTPException(status_code=404, detail=f"Os seguintes produtos não foram encontrados no sistema: {str(err)}")
    except InvalidStockQuantity as err:
	      raise HTTPException(status_code=400, detail=f"A quantidade informada para os seguintes produtos deve ser maior do que zero: {str(err)}")
    except NotEnoughStockQuantity as err:
	      raise HTTPException(status_code=422, detail=f"Os produtos informados não possuem quantidade em estoque suficiente para a saída: {str(err)}")
