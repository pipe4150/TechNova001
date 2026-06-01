from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="TechNova API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERVICES = {
    "products": "http://127.0.0.1:8001",
    "orders":   "http://127.0.0.1:8002",
    "users":    "http://127.0.0.1:8003"
}

@app.get("/")
async def root():
    return {"message": "Gateway de TechNova funcionando. Usa /products, /users o /orders"}

# BUG CORREGIDO #1:
# El gateway armaba la URL como /products/products/  (duplicaba el nombre del servicio).
# Ahora construye correctamente: http://127.0.0.1:8001/{path}
@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway(service: str, path: str, request: Request):
    if service not in SERVICES:
        return {"error": "Servicio no encontrado"}

    # Ruta correcta: base_url + "/" + path (sin repetir el nombre del servicio)
    base = SERVICES[service]
    target_path = path if path else ""
    url = f"{base}/{target_path}"
    if not url.endswith("/"):
        url += "/"

    body = await request.body()

    # BUG CORREGIDO #2:
    # Se pasaban los headers del browser al microservicio interno,
    # incluyendo el header "host" del dominio externo, lo que causaba
    # que el microservicio rechazara o redirigiera la petición (307).
    # Solución: solo pasar Content-Type si existe, nunca el header "host".
    forward_headers = {}
    if request.headers.get("content-type"):
        forward_headers["content-type"] = request.headers["content-type"]

    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            resp = await client.request(
                method=request.method,
                url=url,
                content=body,
                headers=forward_headers,
                timeout=10.0
            )
            return resp.json()
        except Exception as e:
            return {"error": f"Error conectando a {service}", "details": str(e)}
