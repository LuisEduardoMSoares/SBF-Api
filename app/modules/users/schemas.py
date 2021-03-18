from typing import Optional
from ...utils.helpers import BaseSchema, MetaDatetimeSchema


class UserCreate(BaseSchema):
    first_name: str
    last_name: str
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Luis",
                "last_name": "Eduardo",
                "email": "dudu@mail.com",
                "password": "mysecretpassword"
            }
        }
    
class UserUpdate(BaseSchema):
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Luis",
                "last_name": "Eduardo",
                "password": "mysecretpassword"
            }
        }

class UserResponse(BaseSchema):
    id: int
    first_name: str
    last_name: str
    email: str
    metadatetime: MetaDatetimeSchema

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "first_name": "Luis",
                "last_name": "Eduardo",
                "email": "dudu@mail.com",
                "metadatetime": {
                    "created_on": "2020-01-01T00:00:00.000001",
                    "updated_on": "2020-01-01T00:00:00.000001"
                }
            }
        }