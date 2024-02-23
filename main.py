from fastapi import FastAPI

from app.api.currency_api import router as currency_router

app = FastAPI()

app.include_router(currency_router)
