
from uuid import UUID
from fastapi import Depends,status,APIRouter,Query
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.orderitems.dtos import(
    OrderItemCreateSchema,
    OrderItemUpdateSchema,
    OrderItemResponseSchema,
)

from src.orderitems.service import(
    create_orderitem,
    get_order_item_by_id,
    get_list_order_items,
    update_order_items,
    delete_order_item,
)

router = APIRouter(prefix="/order-items",tags=["Order Items"])

@router.post("/",response_model=OrderItemResponseSchema,status_code=status.HTTP_201_CREATED)
def create_order_item_endpoint(payload:OrderItemCreateSchema,db:Session=Depends(get_db)):
    return create_orderitem(payload,db)

@router.get("/{order_item_id}",response_model=OrderItemResponseSchema,status_code=status.HTTP_200_OK)
def get_order_item_by_id_endpoint(order_item_id:UUID,db:Session=Depends(get_db)):
    return get_order_item_by_id(order_item_id,db)

@router.get("/",response_model=list[OrderItemResponseSchema],status_code=status.HTTP_200_OK)
def get_list_order_items_endpoint(db:Session=Depends(get_db),skip:int=Query(0,ge=0),limit:int=Query(50,ge=1,le=100)):
    return get_list_order_items(db,skip,limit)

@router.patch("/{order_item_id}",response_model=OrderItemResponseSchema,status_code=status.HTTP_200_OK)
def update_order_items_endpoint(order_item_id:UUID,payload:OrderItemUpdateSchema,db:Session=Depends(get_db)):
    return update_order_items(order_item_id,payload,db)

@router.delete("/{order_item_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_order_item_endpoint(order_item_id:UUID,db:Session=Depends(get_db)):
    return delete_order_item(order_item_id,db)