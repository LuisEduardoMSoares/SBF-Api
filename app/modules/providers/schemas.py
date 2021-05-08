from validate_docbr import CNPJ

from typing import List, Optional
from pydantic import EmailStr, validator

from ...utils.helpers import BaseSchema, MetaDatetimeSchema
from ...utils.pagination import PaginationMetadataSchema


class ProviderCreate(BaseSchema):
    name: str
    cnpj: str
    phone_number: str
    email: EmailStr
    contact_name: str

    @validator('cnpj')
    def cnpj_validation(cls, field_value):
        if CNPJ().validate(field_value) == False:
            raise ValueError('Invalid CNPJ')
        return field_value

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

    @validator('cnpj')
    def cnpj_validation(cls, field_value):
        if CNPJ().validate(field_value) == False:
            raise ValueError('Invalid CNPJ')
        return field_value

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
                "contact_name": "Ciclano",
                "metadatetime": {
                    "created_on": "2020-01-01T00:00:00.000001",
                    "updated_on": "2020-01-01T00:00:00.000001"
                }
            }
        }

class ProvidersResponse(BaseSchema):
    pagination_metadata: Optional[PaginationMetadataSchema]
    records: List[ProviderResponse]