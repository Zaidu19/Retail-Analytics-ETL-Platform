from fastapi import APIRouter

from src.customers.controller import router as customer_router
from src.categories.controller import router as categories_router
from src.products.controller import router as product_router
from src.orders.controller import router as order_router
from src.orderitems.controller import router as order_items_router
from src.inventory_logs.controller import router as inventory_logs_router
from src.payments.controller import router as payment_router

api_router = APIRouter()

api_router.include_router(customer_router)
api_router.include_router(categories_router)
api_router.include_router(product_router)
api_router.include_router(order_router)
api_router.include_router(order_items_router)
api_router.include_router(inventory_logs_router)
api_router.include_router(payment_router)