# database/__init__.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite in a local file named "emarpi.db"
DATABASE_URL = "sqlite:///emarpi.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
