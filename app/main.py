from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.infrastructure.config import settings
import uvicorn
from app.api.routers import api_router
from fastapi.middleware.cors import CORSMiddleware
from app.exceptions import CustomHTTPException
from app.schemas.response import ErrorResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(title="Auth Service")  

app.include_router(api_router)

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
