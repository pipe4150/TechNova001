# TechNova Ecosystem — Guía de Arranque

## Bugs corregidos
1. **Gateway duplicaba el nombre del servicio en la URL** → `/products/products/` en vez de `/products/`
2. **Gateway reenviaba el header `host` del browser** → causaba el error 307 Temporary Redirect
3. **Products usaba `mongodb://localhost` hardcodeado** → ignoraba el .env con Atlas
4. **Orders tenía rutas `/orders/` en vez de `/`** → el gateway nunca las encontraba
5. **Users: GET / devolvía un mensaje de texto**, no la lista → el dashboard no podía renderizar

## Cómo arrancar (en Codespaces o local)

Abre **4 terminales** y ejecuta uno en cada una:

### Terminal 1 — Products (puerto 8001)
```bash
cd backend/services/products
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### Terminal 2 — Orders (puerto 8002)
```bash
cd backend/services/orders
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

### Terminal 3 — Users (puerto 8003)
```bash
cd backend/services/users
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8003 --reload
```

### Terminal 4 — Gateway (puerto 8000)
```bash
cd backend/services/gateway
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend
Abre `frontend/index.html` en el navegador o con Live Server en VS Code.
