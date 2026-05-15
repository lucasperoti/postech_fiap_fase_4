from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from app.core.exceptions import VeiculoJaVendidoError
from app.domain.enums.veiculo_status import VeiculoStatus


@dataclass
class Veiculo:
    marca: str
    modelo: str
    ano: int
    cor: str
    preco: Decimal
    id: UUID = field(default_factory=uuid4)
    status: VeiculoStatus = field(default=VeiculoStatus.DISPONIVEL)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if self.preco <= 0:
            raise ValueError("Preço deve ser maior que zero")
        if self.ano < 1900 or self.ano > 2100:
            raise ValueError("Ano inválido")
        if not self.marca or not self.modelo:
            raise ValueError("Marca e modelo são obrigatórios")

    def vender(self) -> None:
        if self.status == VeiculoStatus.VENDIDO:
            raise VeiculoJaVendidoError("Veículo já foi vendido")
        self.status = VeiculoStatus.VENDIDO
