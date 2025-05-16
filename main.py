from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Credenciales de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Crear cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Crear instancia de FastAPI
app = FastAPI()

# Modelo Pydantic
class Item(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str] = None

# Ruta de bienvenida
@app.get("/")
async def root():
    return {"message": "Hello from Supabase backend"}

# Obtener todos los items
@app.get("/items/", response_model=List[Item])
def read_items():
    response = supabase.table("items").select("*").execute()
    return response.data

# Obtener un item por ID
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    response = supabase.table("items").select("*").eq("id", item_id).single().execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Item not found")
    return response.data

# Crear un nuevo item
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    response = supabase.table("items").insert(item.dict(exclude_unset=True)).execute()
    if response.status_code != 201:
        raise HTTPException(status_code=500, detail="Error creating item")
    return response.data[0]

# Actualizar un item existente
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    response = supabase.table("items").update(item.dict(exclude_unset=True)).eq("id", item_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Item not found or not updated")
    return response.data[0]