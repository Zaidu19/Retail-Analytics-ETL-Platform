
from fastapi import APIRouter,status,Depends
from sqlalchemy.orm import Session
from uuid import UUID
from src.db.database import get_db

from src.products.dtos import(
    ProductCreateSchema,
    ProductResponseSchema,
    ProductUpdateSchema,
)
from src.products.service import(
    create_product,
    get_all_products,
    get_product_by_id,
    update_product,
    delete_product,
)

router =APIRouter(prefix="/products",tags=["Products"])

@router.post("/",response_model=ProductResponseSchema,status_code=status.HTTP_201_CREATED)
def create_product_endpoint(payload:ProductCreateSchema,db:Session=Depends(get_db)):
    return create_product(payload,db)

@router.get("/",response_model=list[ProductResponseSchema],status_code=status.HTTP_200_OK)
def get_all_products_endpoint(db:Session=Depends(get_db)):
    return get_all_products(db)

@router.get("/{product_id}",response_model=ProductResponseSchema,status_code=status.HTTP_200_OK)
def get_product_by_id_endpoint(product_id:UUID,db:Session=Depends(get_db)):
    return get_product_by_id(product_id,db)

@router.put("/{product_id}",response_model=ProductResponseSchema,status_code=status.HTTP_200_OK)
def update_product_endpoint(product_id:UUID,payload:ProductUpdateSchema,db:Session=Depends(get_db)):
    return update_product(product_id,payload,db)

@router.delete("/{product_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_product_endpoint(product_id:UUID,db:Session=Depends(get_db)):
    return delete_product(product_id,db)