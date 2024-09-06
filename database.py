from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

# user = os.getenv("USER") 
# password = os.getenv("PASSWORD")
# host = os.getenv("HOST") 
# database = os.getenv("NAME")
 

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class MenuItem(Base):
    _tablename_ = 'menu'  # Dois underscores antes e depois de "tablename"
   
    id = Column(Integer, primary_key=True, index=True)
    menuNav = Column(String, nullable=False)
    link = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
 
Base.metadata.create_all(bind=engine)