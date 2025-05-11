from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database.database import get_db, Base, engine
from schemas.item import Item, ItemCreate, ItemUpdate
from services.item_service import ItemService

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item_service = ItemService(db)
    db_item = item_service.get_item(item_id)
    if db_item is None:
        # Puedes personalizar la excepción
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/items/", response_model=list[Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    item_service = ItemService(db)
    items = item_service.get_items(skip=skip, limit=limit)
    return items

@app.post("/items/", response_model=Item)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    item_service = ItemService(db)
    return item_service.create_item(item)

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    item_service = ItemService(db)
    updated_item = item_service.update_item(item_id, item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@app.delete("/items/{item_id}", response_model=dict)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item_service = ItemService(db)
    if item_service.delete_item(item_id):
        return {"message": "Item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

from fastapi import HTTPException # Importa HTTPException aquí