from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.infrastructure.config import settings
import uvicorn
from app.api.routers import api_router
from fastapi.middleware.cors import CORSMiddleware
from app.exceptions import CustomHTTPException
from app.schemas.response import ErrorResponse
from app.etl.scheduler import EtlJob
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

etl_job = EtlJob()

@asynccontextmanager
async def start_shutdown_lifespan(app: FastAPI): 
    # Startup
    await etl_job.start()

    # Shutdown
    yield
    await etl_job.stop()

app = FastAPI(title="Kukar Geoform Dashboard Backend", lifespan= start_shutdown_lifespan)  

app.include_router(api_router)

app.mount("/excel-exports", StaticFiles(directory=settings.EXCEL_EXPORTS_DIR_PATH), name="excel-exports")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

@app.exception_handler(CustomHTTPException)

async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status_code=exc.status_code,
            message=exc.message
        ).model_dump(by_alias=True)
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status_code=exc.status_code,
            message=exc.detail
        ).model_dump(by_alias=True)
    )

@app.get("/") 
async def main_route():     
    return {"message": f"The server is running on {settings.PORT}..."}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
