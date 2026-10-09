from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime

class ClienteCreate(BaseModel):
    razaoSocial: str = Field(min_length = 1, max_length = 150)
    nomeFantasia: str = Field(min_length = 1, max_length = 100)
    cnpj: str | none = Field(min_lenght = 14, max_lenght=14)

class ClienteUpdate(BaseModel):
    razaoSocial: str | none = Field(min_length = 1, max_length = 150)
    nomeFantasia: str | none = Field(min_length = 1, mas_length = 100)
    cnpj: str | none = Field(min_lenght = 14, max_lenght = 14)

class ClienteRead(BaseModel):
    id: uuid
    razaoSocial: str = Field(min_lenght = 1, max_length = 150)
    nomeFantasia: str = Field(min_length = 1, max_length = 100)
    cnpj: str = Field(min_length=14, max_length= 14)
    ativo: bool 
    created_at: datetime
