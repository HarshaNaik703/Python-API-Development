from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# DATABASE_URL = "postgresql://harsha:mypassword@localhost/fastapi"

# engine is responsible for establishing the connection
engine = create_engine(settings.DATABASE_URL)

# sessionmaker communicates with database
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base() 

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    print(settings.DATABASE_URL)
