from fastapi import FastAPI

from app.interfaces.http.controllers.veiculo_controller import router as veiculo_router

app = FastAPI(title="Vehicle Catalog API", version="1.0.0")

app.include_router(veiculo_router, prefix="/catalog")


@app.get("/health")
def health():
    return {"status": "ok"}
