from fastapi import HTTPException,status

from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

from src.products.models import ProductModel
from src.products.dtos import(
    ProductCreateSchema,
    ProductUpdateSchema,
)
from src.categories.models import CategoryModel

def create_product(payload:ProductCreateSchema,db:Session)->ProductModel:
    existing_product=db.scalar(
        select(ProductModel).where(
            ProductModel.name == payload.name,
            ProductModel.category_id == payload.category_id,
        )
    )
    if existing_product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Product already exists")

    category = db.get(CategoryModel,payload.category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Category not found")
    
    product=ProductModel(
        **payload.model_dump()
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product

def get_all_products(db:Session)->list[ProductModel]:
    products = db.scalars(select(ProductModel)).all()
    return products

def get_product_by_id(product_id:UUID,db:Session)->ProductModel:
    product = db.get(ProductModel,product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")
    return product

def update_product(product_id:UUID,payload:ProductUpdateSchema,db:Session)->ProductModel:
    product = db.get(ProductModel,product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")
    
    update_data = payload.model_dump(exclude_unset=True,exclude_none=True)

    if "category_id" in update_data:
        category = db.get(CategoryModel,update_data["category_id"])
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Category not found")
        
    category_id = update_data.get("category_id",product.category_id)    

    if "name" in update_data:
        existing_product = db.scalar(select(ProductModel).where(
            ProductModel.name == update_data["name"],
            ProductModel.category_id == category_id,
            ProductModel.id != product_id
        ))    
        if existing_product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Product already exist in this category")
        
    for key,value in update_data.items():
        setattr(product,key,value)
    db.commit()
    db.refresh(product) 

    return product   

def delete_product(product_id:UUID,db:Session)->None:
    product = db.get(ProductModel,product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")
    db.delete(product)
    db.commit()    

