class Config:
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DATABASE_URI: str = "postgresql+asyncpg://user:password@db:5432/test"
