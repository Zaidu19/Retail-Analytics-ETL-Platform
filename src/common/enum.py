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
    