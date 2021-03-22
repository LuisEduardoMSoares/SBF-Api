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
                "first_name": "Fulano",
                "last_name": "Beltrano",
                "email": "fulano@sbf.com",
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
                "first_name": "Fulano",
                "last_name": "Beltrano",
                "password": "mysecretpassword"
            }
        }

class UserResponse(BaseSchema):
    id: int
    first_name: str
    last_name: str
    email: str
    password: Optional[str]
    metadatetime: MetaDatetimeSchema

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "first_name": "Fulano",
                "last_name": "Beltrano",
                "email": "fulano@sbf.com",
                "metadatetime": {
                    "created_on": "2020-01-01T00:00:00.000001",
                    "updated_on": "2020-01-01T00:00:00.000001"
                }
            }
        }