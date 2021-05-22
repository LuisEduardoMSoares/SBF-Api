from typing import Optional
from ...utils.helpers import BaseSchema, MetaDatetimeSchema


class UserCreate(BaseSchema):
    first_name: str
    last_name: str
    email: str
    password: str
    admin: Optional[bool] = False

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Joao",
                "last_name": "Antonio",
                "email": "joao.antonio@sbf.com",
                "password": "mysecretpassword",
                "admin": "false"
            }
        }
    
class UserUpdate(BaseSchema):
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]
    admin: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Joao",
                "last_name": "Antonio",
                "password": "mysecretpassword",
                "admin": "false"
            }
        }

class UserResponse(BaseSchema):
    id: int
    first_name: str
    last_name: str
    email: str
    admin: Optional[bool]
    metadatetime: MetaDatetimeSchema

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "first_name": "Joao",
                "last_name": "Antonio",
                "email": "joao.antonio@sbf.com",
                "admin": "false",
                "metadatetime": {
                    "created_on": "2020-01-01T00:00:00.000001",
                    "updated_on": "2020-01-01T00:00:00.000001"
                }
            }
        }