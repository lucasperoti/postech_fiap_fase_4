from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.veiculo import Veiculo


class VeiculoRepository(ABC):
    @abstractmethod
    def salvar(self, veiculo: Veiculo) -> Veiculo:
        pass

    @abstractmethod
    def buscar_por_id(self, veiculo_id: UUID) -> Veiculo | None:
        pass

    @abstractmethod
    def listar_disponiveis(self) -> list[Veiculo]:
        pass

    @abstractmethod
    def atualizar(self, veiculo: Veiculo) -> Veiculo:
        pass
