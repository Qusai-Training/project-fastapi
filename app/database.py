from sqlalchemy import create_engine, MetaData

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost:5432/project_fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
metadata = MetaData()

def get_db():
    with engine.connect() as connection:
        yield connection