from decimal import Decimal

from pydantic import BaseModel


class DashboardResponseSchema(BaseModel):
    total_customers: int
    total_products: int
    total_orders: int

    completed_orders: int
    refunded_orders: int

    total_revenue: Decimal
    total_refund_amount: Decimal

    low_stock_products: int

class MonthlySalesResponseSchema(BaseModel):
    month:str
    total_orders:int
    total_revenue:Decimal  

class TopProductResponseSchema(BaseModel):
    product_name:str
    units_sold:int    

class TopProductRevenueSchema(BaseModel):
    product_name:str
    reveue :Decimal

class TopCustomerResponseSchema(BaseModel):
    name:str
    total_orders:int
    total_spent:Decimal 


class TopCategoriesResponseSchema(BaseModel):
    category_name:str
    units_sold:int
    revenue:Decimal 

class ProfitAnalyticsResponseSchema(BaseModel):
    product_name:str
    profit:Decimal

class RefundAnalyticsResponseSchema(BaseModel):
    total_refunds:int
    refund_amounts:Decimal
    refund_rate:float
    avg_refund_amount:Decimal

class LowStockResponseSchema(BaseModel):
    product_name:str
    category_name:str
    stock_qty:int    

class OutofStockProductsResponseSchema(BaseModel):
    product_name:str
    category_name:str

class InventoryValueResponseSchema(BaseModel):
    inventory_value:Decimal    

class InventoryMovementResponseSchema(BaseModel):
    sale:int
    restock:int
    return_:int
    adjustment:int
    damage:int