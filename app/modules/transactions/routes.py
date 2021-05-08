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


#TODO: filtro pelo tipo, nome do produto, nome do fornecedor, range de datas e paginação
@route.get("/transaction/", response_model_exclude_unset=True, response_model=List[TransactionResponse], response_model_exclude_none=True)
def get_all_transactions(db: Session = Depends(get_db), user: User=Depends(manager)):
    """
    ## Retrieve all transactions.

    ### Returns:  
      >  List[TransactionResponse]: A list of dicts with transactions records.
    """
    try:
        transactions = transaction_service.fetch_all(db)
        return transactions
    except ItensNotFound:
	    raise HTTPException(status_code=404, detail="Nenhuma movimentação foi encontrada.")


@route.get("/transaction/{id}", response_model_exclude_unset=True, response_model=TransactionResponse)
def get_one_transaction(id: int, db: Session = Depends(get_db), user: User=Depends(manager)):
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
