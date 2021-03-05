from typing import Optional
from pydantic import BaseModel
from datetime import datetime



class MetaDatetimeSchema(BaseModel):
    created_on: Optional[datetime]
    updated_on: Optional[datetime]

    class Config:
        orm_mode = True


class BaseSchema(BaseModel):

    class Config:
        orm_mode = True
