# TechNova Ecosystem 🚀

Sistema de microservicios para gestión de productos, usuarios y órdenes.

## Estructura del proyecto
TechNova-Ecosystem/
├── backend/
│   └── services/
│       ├── gateway/     → Puerto 8000
│       ├── products/    → Puerto 8001
│       ├── orders/      → Puerto 8002
│       └── users/       → Puerto 8003
└── frontend/
└── index.html

## Cómo ejecutar

Abre 4 terminales y corre un servicio en cada una:

```bash
# Terminal 1 - Products
cd backend/services/products
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Terminal 2 - Orders
cd backend/services/orders
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8002 --reload

# Terminal 3 - Users
cd backend/services/users
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8003 --reload

# Terminal 4 - Gateway
cd backend/services/gateway
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Tecnologías

- **Backend:** Python + FastAPI + MongoDB Atlas
- **Frontend:** HTML + Tailwind CSS
- **Arquitectura:** Microservicios con API Gateway
