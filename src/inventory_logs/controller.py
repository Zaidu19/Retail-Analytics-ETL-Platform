
from fastapi import APIRouter,status,Depends,Query
from sqlalchemy.orm import Session
from uuid import UUID

from src.db.database import get_db
from src.inventory_logs.dtos import InventoryLogCreateSchema,InventoryLogResponseSchema
from src.inventory_logs.service import(
    create_inventory_log,
    get_inventory_logs_by_id,
    get_list_inventory_logs,
)
from src.users.models import UserModel
from src.common.enum import UserRole
from src.auth.service import require_roles
router = APIRouter(prefix="/inventory_logs",tags=["Inventory Logs"])

@router.post("/",response_model=InventoryLogResponseSchema,status_code=status.HTTP_201_CREATED)
def create_inventory_logs_endpoint(payload:InventoryLogCreateSchema,
                                   db:Session=Depends(get_db),
                                   _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.INVENTORY_MANAGER))):
    return create_inventory_log(payload,db)

@router.get("/{inventory_log_id}",response_model=InventoryLogResponseSchema,status_code=status.HTTP_200_OK)
def get_inventory_log_by_id_endpoint(inventory_log_id:UUID,
                                     db:Session=Depends(get_db),
                                     _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST,UserRole.INVENTORY_MANAGER))):
    return get_inventory_logs_by_id(inventory_log_id,db)

@router.get("/",response_model=list[InventoryLogResponseSchema],status_code=status.HTTP_200_OK)
def get_list_inventory_logs_endpoint(db:Session=Depends(get_db),
                                     skip:int= Query(0,ge=0),limit:int=Query(100,ge=1,le=100),
                                     _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST,UserRole.INVENTORY_MANAGER))):
    return get_list_inventory_logs(db,skip,limit)