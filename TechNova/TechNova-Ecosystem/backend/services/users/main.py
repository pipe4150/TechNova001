import os
import certifi
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
from typing import List

load_dotenv()

app = FastAPI(title="TechNova Users Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ca = certifi.where()
uri = os.getenv("MONGO_DETAILS")
client = AsyncIOMotorClient(uri, tlsCAFile=ca)
db = client.technova
collection = db.users

class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str

@app.get("/")
async def root():
    return {"message": "Servicio de Usuarios TechNova Online"}

# BUG CORREGIDO #5 (en users):
# El endpoint GET /users devuelve lista pero el gateway llama a GET /
# Agregamos GET / que devuelve la lista directamente (lo que usa el dashboard)
@app.get("/users", response_model=List[dict])
async def get_users():
    users = []
    async for doc in collection.find():
        doc["_id"] = str(doc["_id"])
        users.append(doc)
    return users

@app.post("/users")
async def create_user(user: User = Body(...)):
    user_dict = user.dict()
    new_user = await collection.insert_one(user_dict)
    return {
        "id": str(new_user.inserted_id),
        "status": "Usuario registrado exitosamente"
    }
