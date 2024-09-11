from fastapi import FastAPI, status, Depends
from sqlalchemy.orm import Session
import classes
from database import engine, get_db, MenuItem
from model import Base
import model
from webscraping import scrape_menu
from datetime import datetime
from typing import List
from fastapi.middleware.cors import CORSMiddleware

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

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

@app.get("/menu", status_code=status.HTTP_201_CREATED)
def get_menu_data(db: Session = Depends(get_db)):
    url = "https://ufu.br"
    lista_textos, lista_links = scrape_menu(url)

    print("Textos:", lista_textos)
    print("Links:", lista_links)

    try:
        for texto, link in zip(lista_textos, lista_links):
            print(f"Inserindo: Texto='{texto}', Link='{link}'")
            new_menu_item = MenuItem(menuNav=texto, link=link, created_at=datetime.utcnow())
            db.add(new_menu_item)
        db.commit()
        return {"message": "Dados inseridos com sucesso!"}
    except Exception as e:
        db.rollback()  # Reverte a transação em caso de erro
        print(f"Erro ao inserir dados: {e}")
        return {"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
    
origins = [
 'http://localhost:3000'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get("/mensagens", response_model=List[classes.Mensagem], status_code=status.HTTP_200_OK)
async def buscar_valores(db: Session = Depends(get_db), skip: int = 0, limit: int=100):
    mensagens = db.query(model.Model_Mensagem).offset(skip).limit(limit).all()
    return mensagens