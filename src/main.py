from src.db import models
from fastapi import FastAPI

from src.core.config import settings
from src.api.router import api_router


app = FastAPI(title=settings.APP_NAME,
              version=settings.APP_VERSION,
              description="""
              "A production-ready Retail Analytics platform built with FastAPI and PostgreSQL"
              ## Features

                - JWT Authentication
                - Role-Based Access Control (RBAC)
                - Customer, Product & Category Management
                - Order & Payment Workflow
                - Refund Management
                - Inventory Tracking
                - Business Analytics APIs
                - Swagger Documentation
                """,
            )


app.include_router(api_router)