from fastapi import APIRouter

from src.customer.controller import router as customer_router

api_router = APIRouter()

api_router.include_router(customer_router)