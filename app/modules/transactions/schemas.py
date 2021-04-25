from pydantic import BaseModel
from pydantic import PositiveInt
from typing import List, Optional
from enum import Enum
from datetime import datetime

from ...utils.helpers import BaseSchema, MetaDatetimeSchema


class TransactionTypeEnum(Enum):
    incoming = 'ENTRADA'
    outgoing = 'SAIDA'

class TransactionProductsData(BaseModel):
    product_id: PositiveInt
    quantity: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "product_id": 1,
                "quantity": 8
            }
        }


class IncomingTransactionCreate(BaseSchema):
    type: TransactionTypeEnum
    description: Optional[str]
    date: datetime
    provider_id: Optional[int]
    products: List[TransactionProductsData]

    class Config:
        schema_extra = {
            "example": {
                "type": "ENTRADA",
                "description": "Operação de teste de entrada de produtos",
                "date": "2020-01-01T00:00:00.000001",
                "provider_id": 1,
                "products": [{
                    "product_id": 1,
                    "quantity": 8
                },{
                    "product_id": 3,
                    "quantity": 15
                },{
                    "product_id": 5,
                    "quantity": 22
                }]
            }
        }

class IncomingTransactionResponse(BaseSchema):
    id: int
    type: TransactionTypeEnum
    description: Optional[str]
    date: datetime
    provider_id: int
    products: List[TransactionProductsData]
    metadatetime: MetaDatetimeSchema

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "type": "ENTRADA",
                "description": "Operação de teste de entrada de produtos",
                "date": "2020-01-01T00:00:00.000001",
                "provider_id": 1,
                "products": [{
                    "product_id": 1,
                    "quantity": 8
                },{
                    "product_id": 3,
                    "quantity": 15
                },{
                    "product_id": 5,
                    "quantity": 22
                }],
                "metadatetime": {
                    "created_on": "2020-01-01T00:00:00.000001",
                    "updated_on": "2020-01-01T00:00:00.000001"
                }
            }
        }


class OutgoingTransactionCreate(BaseSchema):
    type: TransactionTypeEnum
    description: Optional[str]
    date: datetime
    products: List[TransactionProductsData]

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "type": "SAIDA",
                "description": "Operação de teste de saida de produtos",
                "date": "2020-01-01T00:00:00.000001",
                "products": [{
                    "product_id": 1,
                    "quantity": 8
                },{
                    "product_id": 3,
                    "quantity": 15
                },{
                    "product_id": 5,
                    "quantity": 22
                }]
            }
        }

class OutgoingTransactionResponse(BaseSchema):
    id: int
    type: TransactionTypeEnum
    description: Optional[str]
    date: datetime
    products: List[TransactionProductsData]
    metadatetime: MetaDatetimeSchema

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "type": "SAIDA",
                "description": "Operação de teste de saida de produtos",
                "date": "2020-01-01T00:00:00.000001",
                "products": [{
                    "product_id": 1,
                    "quantity": 8
                },{
                    "product_id": 3,
                    "quantity": 15
                },{
                    "product_id": 5,
                    "quantity": 22
                }],
                "metadatetime": {
                    "created_on": "2020-01-01T00:00:00.000001",
                    "updated_on": "2020-01-01T00:00:00.000001"
                }
            }
        }


class TransactionResponse(BaseSchema):
    id: int
    type: TransactionTypeEnum
    description: Optional[str]
    date: datetime
    provider_id: Optional[int]
    products: List[TransactionProductsData]
    metadatetime: MetaDatetimeSchema

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "type": "ENTRADA/SAIDA",
                "description": "Operação de teste de entrada ou de saida de produtos",
                "date": "2020-01-01T00:00:00.000001",
                "provider_id": 1,
                "products": [{
                    "product_id": 1,
                    "quantity": 8
                },{
                    "product_id": 3,
                    "quantity": 15
                },{
                    "product_id": 5,
                    "quantity": 22
                }],
                "metadatetime": {
                    "created_on": "2020-01-01T00:00:00.000001",
                    "updated_on": "2020-01-01T00:00:00.000001"
                }
            }
        }