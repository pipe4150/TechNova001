from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="TechNova - Products Microservice",
    version="1.0.0"
)

# CORS también en el microservicio (necesario para llamadas directas en dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# BUG CORREGIDO #3:
# El servicio usaba mongodb://localhost:27017 (sin credenciales),
# pero el .env tiene la URI de Atlas (MongoDB en la nube).
# Ahora lee MONGO_DETAILS del .env igual que users/orders.
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.technova_db
product_collection = database.get_collection("products")


# ---- MODELOS ----
class ProductModel(BaseModel):
    name: str = Field(..., example="Laptop TechNova Pro")
    description: str = Field(..., example="Laptop de alta gama para desarrollo")
    price: float = Field(..., gt=0, example=1299.99)
    stock: int = Field(..., ge=0, example=50)
    category: str = Field(..., example="Electronics")

class ProductResponseModel(ProductModel):
    id: Optional[str] = Field(None, alias="_id")

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


# ---- ENDPOINTS ----

# Raíz del servicio (el gateway llama a GET /products/ → aquí llega como GET /)
@app.get("/", response_description="Listar todos los productos", response_model=List[ProductResponseModel])
async def list_products():
    products = []
    async for product in product_collection.find(limit=100):
        product["_id"] = str(product["_id"])
        products.append(product)
    return products

@app.post("/", response_description="Agregar nuevo producto",
          response_model=ProductResponseModel, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductModel):
    product_dict = product.model_dump()
    new_product = await product_collection.insert_one(product_dict)
    created_product = await product_collection.find_one({"_id": new_product.inserted_id})
    created_product["_id"] = str(created_product["_id"])
    return created_product

@app.get("/{id}", response_description="Obtener un producto por ID", response_model=ProductResponseModel)
async def show_product(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de producto inválido")
    product = await product_collection.find_one({"_id": ObjectId(id)})
    if product:
        product["_id"] = str(product["_id"])
        return product
    raise HTTPException(status_code=404, detail=f"Producto con ID {id} no encontrado")

@app.delete("/{id}", response_description="Eliminar un producto")
async def delete_product(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de producto inválido")
    delete_result = await product_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "Producto eliminado exitosamente"}
    raise HTTPException(status_code=404, detail=f"Producto con ID {id} no encontrado")
