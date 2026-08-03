from uuid import UUID

from fastapi import APIRouter,status,Depends
from sqlalchemy.orm import Session

from src.users.models import UserModel
from src.auth.service import(
    get_current_admin,
    get_current_user,
   
)
from src.categories.dtos import(
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
)

from src.categories.service import(
    create_category,
    get_all_categories,
    get_category_by_id,
    update_category,
    delete_category,
)
from src.db.database import get_db

router = APIRouter(prefix="/categories",tags=["Categories"])

@router.post("/",response_model=CategoryResponseSchema,status_code=status.HTTP_201_CREATED)
def create_category_endpoint(payload:CategoryCreateSchema,db:Session=Depends(get_db),_:UserModel=Depends(get_current_admin)):
    return create_category(payload,db)

@router.get("/",response_model=list[CategoryResponseSchema],status_code=status.HTTP_200_OK)
def get_all_categories_endpoint(db:Session=Depends(get_db),_:UserModel=Depends(get_current_user)):
    return get_all_categories(db)

@router.get("/{category_id}",response_model=CategoryResponseSchema,status_code=status.HTTP_200_OK)
def get_category_by_id_endpoint(category_id:UUID,db:Session=Depends(get_db),_:UserModel=Depends(get_current_user)):
    return get_category_by_id(category_id,db)

@router.put("/{category_id}",response_model=CategoryResponseSchema,status_code=status.HTTP_200_OK)
def update_category_endpoint(category_id:UUID,payload:CategoryUpdateSchema,db:Session=Depends(get_db),_:UserModel=Depends(get_current_admin)):
    return update_category(category_id,payload,db)

@router.delete("/{category_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_category_endpoint(category_id:UUID,db:Session=Depends(get_db),_:UserModel=Depends(get_current_admin)):
    return delete_category(category_id,db)