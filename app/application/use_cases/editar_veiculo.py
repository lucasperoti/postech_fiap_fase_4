from uuid import UUID

from app.application.dto.veiculo_dto import EditarVeiculoInput, VeiculoOutput
from app.core.exceptions import VeiculoNotFoundException
from app.domain.repositories.veiculo_repository import VeiculoRepository


class EditarVeiculoUseCase:
    def __init__(self, repository: VeiculoRepository):
        self._repository = repository

    def execute(self, veiculo_id: UUID, input_dto: EditarVeiculoInput) -> VeiculoOutput:
        veiculo = self._repository.buscar_por_id(veiculo_id)
        if not veiculo:
            raise VeiculoNotFoundException(f"Veículo {veiculo_id} não encontrado")

        if input_dto.marca is not None:
            veiculo.marca = input_dto.marca
        if input_dto.modelo is not None:
            veiculo.modelo = input_dto.modelo
        if input_dto.ano is not None:
            veiculo.ano = input_dto.ano
        if input_dto.cor is not None:
            veiculo.cor = input_dto.cor
        if input_dto.preco is not None:
            veiculo.preco = input_dto.preco

        veiculo_atualizado = self._repository.atualizar(veiculo)
        return self._to_output(veiculo_atualizado)

    def _to_output(self, veiculo) -> VeiculoOutput:
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
