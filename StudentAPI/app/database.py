from sqlmodel import create_engine, SQLModel, Session
from dotenv import load_dotenv
import os

load_dotenv()

# SQLite database
SQLITE_DATABASE = os.getenv("SQLITE_DATABASE")

engine = create_engine(f"sqlite:///{SQLITE_DATABASE}", echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
