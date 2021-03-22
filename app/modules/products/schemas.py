from typing import Optional
from ...utils.helpers import BaseSchema, MetaDatetimeSchema


class ProductCreate(BaseSchema):
    name: str
    size: str
    inventory: int
    weight: float

    class Config:
        schema_extra = {
            "example": {
                "name": "Camisa Azul",
                "size": "P",
                "inventory": 10,
                "weight": 10.5
            }
        }
    
class ProductUpdate(BaseSchema):
    name: Optional[str]
    size: Optional[str]
    inventory: Optional[int]
    weight: Optional[float]

    class Config:
        schema_extra = {
            "example": {
                "name": "Camisa Azul",
                "size": "P",
                "inventory": 10,
                "weight": 10.5
            }
        }

class ProductResponse(BaseSchema):
    id: int
    name: str
    size: str
    inventory: int
    weight: float
    metadatetime: MetaDatetimeSchema

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Camisa Amarela",
                "size": "P",
                "inventory": 10,
                "weight": 10.5,
                "metadatetime": {
                    "created_on": "2020-01-01T00:00:00.000001",
                    "updated_on": "2020-01-01T00:00:00.000001"
                }
            }
        }