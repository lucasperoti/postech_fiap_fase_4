from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Vehicle Catalog API"
    debug: bool = False
    database_url: str = "postgresql+psycopg2://postgres:postgres@catalog-db:5432/catalog_db"
    
    class Config:
        env_file = ".env"


settings = Settings()
