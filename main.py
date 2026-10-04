from fastapi import FastAPI

from config import setup_logging
from routes import ask, health

setup_logging()

app = FastAPI()

app.include_router(health.router)
app.include_router(ask.router)
