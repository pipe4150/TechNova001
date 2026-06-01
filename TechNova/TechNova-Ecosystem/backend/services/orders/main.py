from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="TechNova Orders Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# También corregido: usar variable de entorno como los otros servicios
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client.technova_db
orders_collection = db.orders

class Order(BaseModel):
    product_id: str
    quantity: int
    total: float

class OrderResponse(Order):
    id: str

# BUG CORREGIDO #4 (en orders):
# Los endpoints eran /orders/ pero el gateway llama a / (sin repetir el prefijo).
# Ahora las rutas son / y /{order_id}
@app.get("/", response_model=List[OrderResponse])
async def get_orders():
    orders = []
    async for doc in orders_collection.find():
        orders.append({**doc, "id": str(doc["_id"])})
    return orders

@app.post("/", response_model=OrderResponse, status_code=201)
async def create_order(order: Order):
    new_order = await orders_collection.insert_one(order.dict())
    created_order = await orders_collection.find_one({"_id": new_order.inserted_id})
    return {**created_order, "id": str(created_order["_id"])}

@app.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str):
    if not ObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="ID no válido")
    doc = await orders_collection.find_one({"_id": ObjectId(order_id)})
    if doc:
        return {**doc, "id": str(doc["_id"])}
    raise HTTPException(status_code=404, detail="Orden no encontrada")
