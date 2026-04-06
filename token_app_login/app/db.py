# --------------------------- SQLAlchemy Imports -------------------------
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --------------------------- Database Configuration -------------------------
database_url = "sqlite:///./database.db"

# --------------------------- Database Engine Setup -------------------------
engine = create_engine(database_url)

# --------------------------- Database Session Setup -------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --------------------------- Base Class for Models -------------------------
Base = declarative_base()

