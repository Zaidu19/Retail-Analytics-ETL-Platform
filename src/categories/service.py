
from uuid import UUID
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.categories.models import CategoryModel
from src.categories.dtos import(
    CategoryCreateSchema,
    CategoryUpdateSchema,
)

def create_category(payload:CategoryCreateSchema,db:Session)->CategoryModel:
    existing_category =db.scalar(
        select(CategoryModel).where(
            CategoryModel.name == payload.name
        )
    )

    if existing_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Category with this name already exists")
    category = CategoryModel(
        **payload.model_dump()
    )
    db.add(category)
    db.commit()
    db.refresh(category)

    return category

def get_all_categories(db:Session)->list[CategoryModel]:
    categories= db.scalars(select(CategoryModel)).all()
    return categories

def get_category_by_id(category_id:UUID,db:Session)->CategoryModel:
    category =db.get(CategoryModel,category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Category not found")
    return category

def update_category(category_id:UUID,payload:CategoryUpdateSchema,db:Session)->CategoryModel:
    category=db.get(CategoryModel,category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Category not found")

    update_data=payload.model_dump(exclude_unset=True,exclude_none=True)
    for key,value in update_data.items():
        setattr(category,key,value)

    db.commit()
    db.refresh(category)

    return category

def delete_category(category_id:UUID,db:Session)->None:
    category = db.get(CategoryModel,category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Category not found")
    db.delete(category)
    db.commit()
