from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()  # Loads environment variables from .env file

# user = "postgres"
# password = "isadora"
# database = "pds"
# host = "localhost"

user = os.getenv("USER") 
password = os.getenv("PASSWORD")
host = os.getenv("HOST") 
database = os.getenv("NAME")
 

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}/{database}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()