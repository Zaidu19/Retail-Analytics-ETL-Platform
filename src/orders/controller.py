from uuid import UUID
from fastapi import APIRouter,status,Depends,Query
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.orders.dtos import(
    OrderCreateSchema,
    OrderUpdateSchema,
    OrderResponseSchema,
)

from src.orders.service import(
    create_order,
    get_all_orders,
    get_order_by_id,
    update_order,
    cancel_order
)
from src.orderitems.service import( 
    get_order_items_by_order,
    get_order_item_by_id,
    get_list_order_items,
)
from src.orderitems.dtos import OrderItemResponseSchema
from src.payments.service import get_payment_by_order
from src.payments.dtos import PaymentResponseSchema

router = APIRouter(prefix="/orders",tags=["Orders"])

@router.post("/",response_model=OrderResponseSchema,status_code=status.HTTP_201_CREATED)
def create_order_endpoint(payload:OrderCreateSchema,db:Session=Depends(get_db)):
    return create_order(payload,db)

@router.get("/",response_model=list[OrderResponseSchema],status_code=status.HTTP_200_OK)
def get_all_orders_endpoint(skip:int=Query(0,ge=0),limit:int=Query(50,ge=1,le=100),db:Session=Depends(get_db)):
    return get_all_orders(db,skip,limit)

@router.get("/{order_id}",response_model=OrderResponseSchema,status_code=status.HTTP_200_OK)
def get_order_by_id_endpoint(order_id:UUID,db:Session=Depends(get_db)):
    return get_order_by_id(order_id,db)

@router.patch("/{order_id}/status",response_model=OrderResponseSchema,status_code=status.HTTP_200_OK)
def update_order_endpoint(order_id:UUID,payload:OrderUpdateSchema,db:Session=Depends(get_db)):
    return update_order(order_id,payload,db)

@router.patch("/{order_id}/cancel")
def cancel_order_endpoint(order_id:UUID,db:Session=Depends(get_db)):
    return cancel_order(order_id,db)




@router.get("/{order_id}/items",response_model=list[OrderItemResponseSchema],status_code=status.HTTP_200_OK)
def get_order_items_by_order_endpoint(order_id:UUID,db:Session=Depends(get_db)):
    return get_order_items_by_order(order_id,db)

@router.get("/items",response_model=list[OrderItemResponseSchema],status_code=status.HTTP_200_OK)
def get_list_order_items_endpoint(db:Session=Depends(get_db),skip:int=Query(0,ge=0),limit:int=Query(100,ge=1,le=100)):
    return get_list_order_items(db,skip,limit)

@router.get("/items/{order_item_id}",response_model =OrderItemResponseSchema,status_code=status.HTTP_200_OK)
def get_order_item_by_id_endpoint(db:Session=Depends(get_db),skip:int=Query(0,ge=0),limit:int=Query(100,gt=0,le=100)):
    return get_order_item_by_id(db,skip,limit)



@router.get("/{order_id}/payments",response_model=list[PaymentResponseSchema],status_code=status.HTTP_200_OK)
def get_payment_by_order_endpoint(order_id:UUID,db:Session=Depends(get_db)):
    return get_payment_by_order(order_id,db)