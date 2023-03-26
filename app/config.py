class Config:
    DEBUG: bool = True
    HOST: str = "localhost"
    PORT: int = 8000
    DATABASE_URI: str = "postgresql+asyncpg://user:password@localhost:5432/test"
