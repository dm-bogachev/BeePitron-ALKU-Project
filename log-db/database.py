from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

if os.getenv('DOCKER', 'false').lower() == 'true':
    DB_NAME = "log.db"
    DB_PATH = os.path.join('/', 'app', 'config', DB_NAME)
    SQLALCHEMY_DATABASE_URL = "sqlite:///" + DB_PATH
else:
    DB_NAME = "log_local.db"
    DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)
    SQLALCHEMY_DATABASE_URL = "sqlite:///" + DB_PATH

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
