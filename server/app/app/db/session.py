import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_USER=os.environ.get("DB_USER")
DB_HOST=os.environ.get("DB_HOST")
DB_PASSWORD=os.environ.get("DB_PASSWORD")
DB_PORT=os.environ.get("DB_PORT")
DB_DATABASE=os.environ.get("DB_DATABASE")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker (autocommit=False,autoflush=False, bind=engine)
