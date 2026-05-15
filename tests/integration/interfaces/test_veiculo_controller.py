import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session, sessionmaker

from app.domain.entities.veiculo import Veiculo
from app.infrastructure.database.config import Base, get_db
from app.infrastructure.database.repositories.sql_veiculo_repository import SQLVeiculoRepository
from app.main import app

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


class TestVeiculoController:
    def test_cadastrar_veiculo(self, client):
        response = client.post("/catalog/veiculos", json={
            "marca": "Fiat",
            "modelo": "Uno",
            "ano": 2020,
            "cor": "Branco",
            "preco": 45000.00,
        })
        assert response.status_code == 201
        data = response.json()
        assert data["marca"] == "Fiat"
        assert data["status"] == "DISPONIVEL"

    def test_listar_disponiveis(self, client, db_session):
        repo = SQLVeiculoRepository(db_session)
        repo.salvar(Veiculo(marca="VW", modelo="Gol", ano=2021, cor="Preto", preco=40000))
        
        response = client.get("/catalog/internal/veiculos/disponiveis")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_editar_veiculo(self, client, db_session):
        repo = SQLVeiculoRepository(db_session)
        veiculo = repo.salvar(Veiculo(marca="Ford", modelo="Ka", ano=2019, cor="Prata", preco=35000))
        
        response = client.put(f"/catalog/veiculos/{veiculo.id}", json={"cor": "Azul"})
        assert response.status_code == 200
        data = response.json()
        assert data["cor"] == "Azul"

    def test_marcar_vendido(self, client, db_session):
        repo = SQLVeiculoRepository(db_session)
        veiculo = repo.salvar(Veiculo(marca="Honda", modelo="Civic", ano=2022, cor="Preto", preco=90000))
        
        response = client.put(f"/catalog/internal/veiculos/{veiculo.id}/vender")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "VENDIDO"
