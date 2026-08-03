from enum import Enum

class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"
    completed = "completed"

class InventoryReason(str,Enum):
    sale = "sale"
    restock = "restock"
    return_ = "return"
    adjustment = "adjustment"
    damage = "damage"

class PaymentMethod(str,Enum):
    card = "card"
    upi = "upi"
    net_banking = "net_banking"
    cash ="cash"
    wallet ="wallet"

class PaymentStatus(str,Enum):
    pending = "pending"
    success = "success"
    failed = "failed"
    refunded = "refunded"

class UserRole(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    INVENTORY_MANAGER = "inventory_manager"
    BUSINESS_ANALYST = "business_analyst"   
        
    