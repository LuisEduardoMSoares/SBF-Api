from typing import Optional
from ...utils.helpers import BaseSchema, MetaDatetimeSchema


class ProductCreate(BaseSchema):
    name: str
    size: str
    inventory: int
    weight: float
    is_deleted: bool

    class Config:
        schema_extra = {
            "example": {
                "name": "Camisa Azul",
                "size": "P",
                "inventory": 10,
                "weight": 10.5,
                "is_deleted": False
            }
        }
    
class ProductUpdate(BaseSchema):
    name: Optional[str]
    size: Optional[str]
    inventory: Optional[int]
    weight: Optional[float]
    is_deleted: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "name": "Camisa Azul",
                "size": "P",
                "inventory": 10,
                "weight": 10.5,
                "is_deleted": False,
            }
        }

class ProductResponse(BaseSchema):
    id: int
    name: str
    size: str
    inventory: int
    weight: float
    is_deleted: bool
    created_by: int
    metadatetime: MetaDatetimeSchema

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Camisa Amarela",
                "size": "P",
                "inventory": 10,
                "weight": 10.5,
                "is_deleted": False,
                "created_by": 1,
                "metadatetime": {
                    "created_on": "2020-01-01T00:00:00.000001",
                    "updated_on": "2020-01-01T00:00:00.000001"
                }
            }
        }