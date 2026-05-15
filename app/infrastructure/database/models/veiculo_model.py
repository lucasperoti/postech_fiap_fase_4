from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, Integer, Numeric, String
from sqlalchemy.sql import func

from app.domain.enums.veiculo_status import VeiculoStatus
from app.infrastructure.database.config import Base


class VeiculoModel(Base):
    __tablename__ = "veiculos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    marca = Column(String(100), nullable=False)
    modelo = Column(String(100), nullable=False)
    ano = Column(Integer, nullable=False)
    cor = Column(String(50), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(VeiculoStatus), default=VeiculoStatus.DISPONIVEL, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
