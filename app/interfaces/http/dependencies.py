from fastapi import Depends
from sqlalchemy.orm import Session

from app.domain.repositories.veiculo_repository import VeiculoRepository
from app.infrastructure.database.config import get_db
from app.infrastructure.database.repositories.sql_veiculo_repository import SQLVeiculoRepository


def get_veiculo_repository(db: Session = Depends(get_db)) -> VeiculoRepository:
    return SQLVeiculoRepository(db)
