from src.db import models
from fastapi import FastAPI

from src.api.router import api_router

app = FastAPI(title="Retail Analytics & ETL Platform",
              version="1.0.0")

app.include_router(api_router)