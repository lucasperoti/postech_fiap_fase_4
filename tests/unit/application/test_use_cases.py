import pytest
from decimal import Decimal
from uuid import uuid4
from unittest.mock import Mock

from app.application.dto.veiculo_dto import CadastrarVeiculoInput, EditarVeiculoInput
from app.application.use_cases.cadastrar_veiculo import CadastrarVeiculoUseCase
from app.application.use_cases.editar_veiculo import EditarVeiculoUseCase
from app.application.use_cases.listar_veiculos_disponiveis import ListarVeiculosDisponiveisUseCase
from app.application.use_cases.marcar_veiculo_vendido import MarcarVeiculoVendidoUseCase
from app.core.exceptions import VeiculoNotFoundException
from app.domain.entities.veiculo import Veiculo
from app.domain.enums.veiculo_status import VeiculoStatus


class TestCadastrarVeiculoUseCase:
    def test_execute(self):
        repo = Mock()
        veiculo = Veiculo(marca="Fiat", modelo="Uno", ano=2020, cor="Branco", preco=Decimal("45000"))
        repo.salvar.return_value = veiculo
        
        use_case = CadastrarVeiculoUseCase(repo)
        input_dto = CadastrarVeiculoInput(marca="Fiat", modelo="Uno", ano=2020, cor="Branco", preco=Decimal("45000"))
        
        result = use_case.execute(input_dto)
        
        repo.salvar.assert_called_once()
        assert result.marca == "Fiat"


class TestEditarVeiculoUseCase:
    def test_execute_sucesso(self):
        repo = Mock()
        veiculo = Veiculo(marca="Fiat", modelo="Uno", ano=2020, cor="Branco", preco=Decimal("45000"))
        repo.buscar_por_id.return_value = veiculo
        repo.atualizar.return_value = veiculo
        
        use_case = EditarVeiculoUseCase(repo)
        result = use_case.execute(veiculo.id, EditarVeiculoInput(preco=Decimal("46000")))
        
        assert repo.atualizar.called

    def test_execute_nao_encontrado(self):
        repo = Mock()
        repo.buscar_por_id.return_value = None
        
        use_case = EditarVeiculoUseCase(repo)
        with pytest.raises(VeiculoNotFoundException):
            use_case.execute(uuid4(), EditarVeiculoInput())


class TestListarVeiculosDisponiveisUseCase:
    def test_execute(self):
        repo = Mock()
        veiculos = [
            Veiculo(marca="Fiat", modelo="Uno", ano=2020, cor="Branco", preco=Decimal("30000")),
            Veiculo(marca="VW", modelo="Gol", ano=2021, cor="Preto", preco=Decimal("40000")),
        ]
        repo.listar_disponiveis.return_value = veiculos
        
        use_case = ListarVeiculosDisponiveisUseCase(repo)
        result = use_case.execute()
        
        assert len(result) == 2


class TestMarcarVeiculoVendidoUseCase:
    def test_execute_sucesso(self):
        repo = Mock()
        veiculo = Veiculo(marca="Fiat", modelo="Uno", ano=2020, cor="Branco", preco=Decimal("45000"))
        repo.buscar_por_id.return_value = veiculo
        repo.atualizar.return_value = veiculo
        
        use_case = MarcarVeiculoVendidoUseCase(repo)
        result = use_case.execute(veiculo.id)
        
        assert result.status == VeiculoStatus.VENDIDO
