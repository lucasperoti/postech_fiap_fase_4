from app.application.dto.veiculo_dto import VeiculoOutput
from app.domain.repositories.veiculo_repository import VeiculoRepository


class ListarVeiculosDisponiveisUseCase:
    def __init__(self, repository: VeiculoRepository):
        self._repository = repository

    def execute(self) -> list[VeiculoOutput]:
        veiculos = self._repository.listar_disponiveis()
        return [self._to_output(v) for v in veiculos]

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
