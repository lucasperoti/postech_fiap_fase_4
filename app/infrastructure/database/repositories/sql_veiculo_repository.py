from decimal import Decimal
from uuid import UUID

from app.domain.entities.veiculo import Veiculo
from app.domain.enums.veiculo_status import VeiculoStatus
from app.domain.repositories.veiculo_repository import VeiculoRepository
from app.infrastructure.database.models.veiculo_model import VeiculoModel


class SQLVeiculoRepository(VeiculoRepository):
    def __init__(self, db_session):
        self._session = db_session

    def salvar(self, veiculo: Veiculo) -> Veiculo:
        model = VeiculoModel(
            id=str(veiculo.id),
            marca=veiculo.marca,
            modelo=veiculo.modelo,
            ano=veiculo.ano,
            cor=veiculo.cor,
            preco=veiculo.preco,
            status=veiculo.status,
        )
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)

    def buscar_por_id(self, veiculo_id: UUID) -> Veiculo | None:
        model = self._session.query(VeiculoModel).filter_by(id=str(veiculo_id)).first()
        if model:
            return self._to_entity(model)
        return None

    def listar_disponiveis(self) -> list[Veiculo]:
        models = (
            self._session.query(VeiculoModel)
            .filter_by(status=VeiculoStatus.DISPONIVEL)
            .order_by(VeiculoModel.preco.asc())
            .all()
        )
        return [self._to_entity(m) for m in models]

    def atualizar(self, veiculo: Veiculo) -> Veiculo:
        model = self._session.query(VeiculoModel).filter_by(id=str(veiculo.id)).first()
        if not model:
            return None
        model.marca = veiculo.marca
        model.modelo = veiculo.modelo
        model.ano = veiculo.ano
        model.cor = veiculo.cor
        model.preco = veiculo.preco
        model.status = veiculo.status
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)

    def _to_entity(self, model: VeiculoModel) -> Veiculo:
        from uuid import UUID
        return Veiculo(
            id=UUID(model.id),
            marca=model.marca,
            modelo=model.modelo,
            ano=model.ano,
            cor=model.cor,
            preco=Decimal(str(model.preco)),
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
