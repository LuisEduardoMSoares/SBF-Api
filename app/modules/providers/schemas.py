from typing import Optional
from pydantic import EmailStr
from ...utils.helpers import BaseSchema, MetaDatetimeSchema


class ProviderCreate(BaseSchema):
    name: str
    cnpj: str
    phone_number: str
    email: EmailStr
    contact_name: str

    class Config:
        schema_extra = {
            "example": {
                "name": "FornecedorA",
                "cnpj": "00000000000000",
                "phone_number": "00111115555",
                "email": "fornecedor@sbf.com",
                "contact_name": "Ciclano"
            }
        }
    
class ProviderUpdate(BaseSchema):
    name: Optional[str]
    cnpj: Optional[str]
    phone_number: Optional[str]
    email: Optional[EmailStr]
    contact_name: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "FornecedorA",
                "cnpj": "00000000000000",
                "phone_number": "00111115555",
                "email": "fornecedor@sbf.com",
                "contact_name": "Ciclano"
            }
        }

class ProviderResponse(BaseSchema):
    id: int
    name: Optional[str]
    cnpj: Optional[str]
    phone_number: Optional[str]
    email: Optional[EmailStr]
    contact_name: Optional[str]
    metadatetime: MetaDatetimeSchema

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "FornecedorA",
                "cnpj": "00000000000000",
                "phone_number": "00111115555",
                "email": "fornecedor@sbf.com",
                "contact_name": "Ciclano"
            }
        }