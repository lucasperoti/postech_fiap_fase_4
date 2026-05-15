from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.application.dto.veiculo_dto import CadastrarVeiculoInput, EditarVeiculoInput, VeiculoOutput
from app.application.use_cases.buscar_veiculo_por_id import BuscarVeiculoPorIdUseCase
from app.application.use_cases.cadastrar_veiculo import CadastrarVeiculoUseCase
from app.application.use_cases.editar_veiculo import EditarVeiculoUseCase
from app.application.use_cases.listar_veiculos_disponiveis import ListarVeiculosDisponiveisUseCase
from app.application.use_cases.marcar_veiculo_vendido import MarcarVeiculoVendidoUseCase
from app.core.exceptions import DomainException, VeiculoNotFoundException
from app.domain.repositories.veiculo_repository import VeiculoRepository
from app.interfaces.http.dependencies import get_veiculo_repository

router = APIRouter()


@router.post("/veiculos", response_model=VeiculoOutput, status_code=201)
def cadastrar(
    input_dto: CadastrarVeiculoInput,
    repository: VeiculoRepository = Depends(get_veiculo_repository),
):
    use_case = CadastrarVeiculoUseCase(repository)
    try:
        return use_case.execute(input_dto)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.put("/veiculos/{veiculo_id}", response_model=VeiculoOutput)
def editar(
    veiculo_id: UUID,
    input_dto: EditarVeiculoInput,
    repository: VeiculoRepository = Depends(get_veiculo_repository),
):
    use_case = EditarVeiculoUseCase(repository)
    try:
        return use_case.execute(veiculo_id, input_dto)
    except VeiculoNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/internal/veiculos/disponiveis", response_model=list[VeiculoOutput])
def listar_disponiveis(
    repository: VeiculoRepository = Depends(get_veiculo_repository),
):
    use_case = ListarVeiculosDisponiveisUseCase(repository)
    return use_case.execute()


@router.get("/internal/veiculos/{veiculo_id}", response_model=VeiculoOutput)
def buscar_por_id(
    veiculo_id: UUID,
    repository: VeiculoRepository = Depends(get_veiculo_repository),
):
    use_case = BuscarVeiculoPorIdUseCase(repository)
    try:
        return use_case.execute(veiculo_id)
    except VeiculoNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/internal/veiculos/{veiculo_id}/vender", response_model=VeiculoOutput)
def marcar_vendido(
    veiculo_id: UUID,
    repository: VeiculoRepository = Depends(get_veiculo_repository),
):
    use_case = MarcarVeiculoVendidoUseCase(repository)
    try:
        return use_case.execute(veiculo_id)
    except VeiculoNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DomainException as e:
        raise HTTPException(status_code=422, detail=str(e))
