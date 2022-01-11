from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_AQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost/fastapi"

engine = create_engine(SQL_AQLALCHEMY_DATABASE_URL)

SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()