from typing import List
from pydantic import BaseModel
from enum import Enum
from datetime import datetime

from ...utils.helpers import BaseSchema, MetaDatetimeSchema


class TransactionTypeEnum(Enum):
    incoming = 'ENTRADA'
    outgoing = 'SAIDA'

class IncomingProductsData(BaseModel):
    product_id: int
    quantity: int

    class Config:
        schema_extra = {
            "example": {
                "product_id": 1,
                "quantity": 8
            }
        }

class IncomingTransactionCreate(BaseSchema):
    type: TransactionTypeEnum
    description: str
    date: datetime
    products: List[IncomingProductsData]

    class Config:
        schema_extra = {
            "example": {
                "type": "ENTRADA",
                "description": "Operação de teste de entrada de produtos",
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