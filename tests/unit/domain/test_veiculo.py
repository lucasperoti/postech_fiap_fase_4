import pytest
from decimal import Decimal
from uuid import uuid4

from app.domain.entities.veiculo import Veiculo
from app.domain.enums.veiculo_status import VeiculoStatus
from app.core.exceptions import VeiculoJaVendidoError


class TestVeiculoEntity:
    def test_criar_veiculo_com_sucesso(self):
        veiculo = Veiculo(
            marca="Fiat",
            modelo="Uno",
            ano=2020,
            cor="Branco",
            preco=Decimal("45000.00"),
        )
        assert veiculo.marca == "Fiat"
        assert veiculo.status == VeiculoStatus.DISPONIVEL
        assert veiculo.id is not None

    def test_criar_veiculo_preco_invalido(self):
        with pytest.raises(ValueError, match="Preço deve ser maior que zero"):
            Veiculo(marca="Fiat", modelo="Uno", ano=2020, cor="Branco", preco=Decimal("0"))

    def test_criar_veiculo_ano_invalido(self):
        with pytest.raises(ValueError, match="Ano inválido"):
            Veiculo(marca="Fiat", modelo="Uno", ano=1800, cor="Branco", preco=Decimal("45000"))

    def test_vender_veiculo_disponivel(self):
        veiculo = Veiculo(marca="Fiat", modelo="Uno", ano=2020, cor="Branco", preco=Decimal("45000"))
        veiculo.vender()
        assert veiculo.status == VeiculoStatus.VENDIDO

    def test_vender_veiculo_ja_vendido(self):
        veiculo = Veiculo(marca="Fiat", modelo="Uno", ano=2020, cor="Branco", preco=Decimal("45000"))
        veiculo.vender()
        with pytest.raises(VeiculoJaVendidoError):
            veiculo.vender()
