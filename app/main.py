from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

from app.api.endpoints import automovel_endpoints

app = FastAPI(
    title="API de Automóveis",
    description="Uma API para gerenciar informações de automóveis, seguindo princípios SOLID.",
)

app.include_router(
    automovel_endpoints.router, prefix="/automoveis", tags=["Automóveis"]
)

mcp = FastApiMCP(app, include_operations=["get_automoveis"])
mcp.mount()
mcp.setup_server()

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API de Automóveis!"}
