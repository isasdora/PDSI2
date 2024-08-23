from fastapi import FastAPI, status, Depends
from fastapi.params import Body
import classes
import model
from database import engine, get_db
from sqlalchemy.orm import Session
import os

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    secret_key = os.environ.get("SECRET_KEY")
    return {"Hello": "outra coisa 2.0"}

@app.post("/criar", status_code=status.HTTP_201_CREATED)
def criar_valores(nova_mensagem: classes.Mensagem, db: Session = Depends(get_db)):
    mensagem_criada = model.Model_Mensagem(**nova_mensagem.model_dump())
    db.add(mensagem_criada)
    db.commit()
    db.refresh(mensagem_criada)
    return {"Mensagem": mensagem_criada}

@app.get("/quadrado/{num}")
def square(num: int):
    return num ** 2