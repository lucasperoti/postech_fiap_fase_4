from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.domain.enums.veiculo_status import VeiculoStatus


class CadastrarVeiculoInput(BaseModel):
    marca: str = Field(..., min_length=1, max_length=100)
    modelo: str = Field(..., min_length=1, max_length=100)
    ano: int = Field(..., ge=1900, le=2100)
    cor: str = Field(..., min_length=1, max_length=50)
    preco: Decimal = Field(..., gt=0)


class EditarVeiculoInput(BaseModel):
    marca: str | None = Field(None, min_length=1, max_length=100)
    modelo: str | None = Field(None, min_length=1, max_length=100)
    ano: int | None = Field(None, ge=1900, le=2100)
    cor: str | None = Field(None, min_length=1, max_length=50)
    preco: Decimal | None = Field(None, gt=0)


class VeiculoOutput(BaseModel):
    id: UUID
    marca: str
    modelo: str
    ano: int
    cor: str
    preco: Decimal
    status: VeiculoStatus
    created_at: datetime
    updated_at: datetime
