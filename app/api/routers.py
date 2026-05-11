from fastapi import APIRouter
import importlib
from app.api.endpoints import __all__ as endpoints

api_router = APIRouter()

for endpoint in endpoints:
    module = importlib.import_module(f"app.api.endpoints.{endpoint}")
    prefix = endpoint if '_' not in endpoint else endpoint.replace('_', '-')
    api_router.include_router(module.router, prefix=f"/api/auth/{prefix}", tags=[prefix])
