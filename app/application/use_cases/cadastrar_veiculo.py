from uuid import UUID

from app.application.dto.veiculo_dto import CadastrarVeiculoInput, VeiculoOutput
from app.domain.entities.veiculo import Veiculo
from app.domain.repositories.veiculo_repository import VeiculoRepository


class CadastrarVeiculoUseCase:
    def __init__(self, repository: VeiculoRepository):
        self._repository = repository

    def execute(self, input_dto: CadastrarVeiculoInput) -> VeiculoOutput:
        veiculo = Veiculo(
            marca=input_dto.marca,
            modelo=input_dto.modelo,
            ano=input_dto.ano,
            cor=input_dto.cor,
            preco=input_dto.preco,
        )
        veiculo_salvo = self._repository.salvar(veiculo)
        return self._to_output(veiculo_salvo)

    def _to_output(self, veiculo: Veiculo) -> VeiculoOutput:
        return VeiculoOutput(
            id=veiculo.id,
            marca=veiculo.marca,
            modelo=veiculo.modelo,
            ano=veiculo.ano,
            cor=veiculo.cor,
            preco=veiculo.preco,
            status=veiculo.status,
            created_at=veiculo.created_at,
            updated_at=veiculo.updated_at,
        )
