# Vehicle Catalog API

Microsservico de catalogo de veiculos para a plataforma de revenda de veiculos (SOAT Fase 4).

**Repositorio:** https://github.com/lucasperoti/postech_fiap_fase_4.git

## Tecnologias

- Python 3.11
- FastAPI
- SQLAlchemy 2.0 + Alembic
- PostgreSQL
- pytest + pytest-asyncio

## Como rodar localmente

### Opcao 1: Docker Compose (recomendado)

```bash
# Na raiz do projeto
docker-compose up --build
```

A API estara disponivel em `http://localhost:18080`

### Opcao 2: Localmente com Python

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar banco de dados (PostgreSQL)
# Edite .env se necessario

# Rodar a aplicacao
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Documentacao da API

- Swagger UI: `http://localhost:18080/docs`
- ReDoc: `http://localhost:18080/redoc`

## Como testar

```bash
# Instalar dependencias
pip install -r requirements.txt

# Rodar testes com cobertura
pytest --cov=app --cov-report=term-missing --cov-fail-under=80
```

## Endpoints

| Metodo | Endpoint | Descricao |
|---|---|---|
| POST | `/catalog/veiculos` | Cadastrar veiculo |
| PUT | `/catalog/veiculos/{id}` | Editar veiculo |
| GET | `/catalog/internal/veiculos/disponiveis` | Listar disponiveis (interno) |
| PUT | `/catalog/internal/veiculos/{id}/vender` | Marcar como vendido (interno) |

## Arquitetura

Clean Architecture pragmatica:
- `domain/` - Entidades e regras de negocio puras
- `application/` - Casos de uso e DTOs
- `infrastructure/` - SQLAlchemy, banco de dados
- `interfaces/` - FastAPI controllers
