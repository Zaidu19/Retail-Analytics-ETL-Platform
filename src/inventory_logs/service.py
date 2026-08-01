
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException,status

from src.products.models import ProductModel
from src.inventory_logs.models import InventoryLogModel
from src.common.enum import InventoryReason
from src.inventory_logs.dtos import InventoryLogCreateSchema


def create_inventory_log(payload:InventoryLogCreateSchema,db:Session)->InventoryLogModel:
    product = db.get(ProductModel,payload.product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")

    if payload.reason == InventoryReason.sale:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Sale inventory logs are created automatically through order workflow.")

    elif payload.reason == InventoryReason.damage:

        if product.stock_qty < payload.change_qty:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Insufficient stock.")

        product.stock_qty -= payload.change_qty
        log_change = -payload.change_qty
    
    elif payload.reason in (
        InventoryReason.restock,
        InventoryReason.return_
    ):
        product.stock_qty += payload.change_qty
        log_change = payload.change_qty

    elif payload.reason == InventoryReason.adjustment:
        
        if product.stock_qty + payload.change_qty < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Adjustment would result in negative stock.")
        product.stock_qty += payload.change_qty
        log_change = payload.change_qty

    inventory_log = InventoryLogModel(
        product_id = payload.product_id,
        change_qty = log_change,
        reason = payload.reason
    )            

    db.add(inventory_log)
    db.commit()
    db.refresh(inventory_log)


    return inventory_log

def get_inventory_logs_by_id(inventory_log_id:UUID,db:Session)->InventoryLogModel:
    inventory_log = db.get(InventoryLogModel,inventory_log_id)
    if not inventory_log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Inventory not found")
    return inventory_log


def get_list_inventory_logs(db:Session,skip:int=0,limit:int=100)->list[InventoryLogModel]:
    inventory_logs = db.scalars(select(InventoryLogModel).offset(skip).limit(limit)).all()
    return inventory_logs

def get_inventory_logs_by_product(product_id:UUID,db:Session)->list[InventoryLogModel]:
    product = db.get(ProductModel,product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")
    inventory_logs = db.scalars(select(InventoryLogModel).where(InventoryLogModel.product_id == product_id)).all()

    return inventory_logs
