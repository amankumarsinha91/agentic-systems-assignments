from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

@app.get("/hello")
async def hello():
    return {"message": "Hello, Welcome to FastAPI!"}


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Before request is processed
        print(f"➡️ Incoming Request: {request.method} {request.url.path}")
        print("🌐 Processing request...")

        response = await call_next(request)

        # After response is sent
        print("✅ Response completed.")
        return response

app.add_middleware(LoggingMiddleware)


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=404,
        content={"message": "The requested resource was not found"}
    )