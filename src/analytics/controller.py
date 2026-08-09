from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.users.models import UserModel
from src.common.enum import UserRole
from src.auth.service import require_roles
from src.analytics.dtos import (
    DashboardResponseSchema,
    MonthlySalesResponseSchema,
    TopProductResponseSchema,
    TopProductRevenueSchema,
    TopCustomerResponseSchema,
    TopCategoriesResponseSchema,
    ProfitAnalyticsResponseSchema,
    RefundAnalyticsResponseSchema,
    LowStockResponseSchema,
    OutofStockProductsResponseSchema,
    InventoryValueResponseSchema,
    InventoryMovementResponseSchema,

)
from src.analytics.service import(
    get_dashboard,
    get_monthly_sales,
    get_top_products,
    get_top_products_revenue,
    get_top_customers,
    get_top_categories,
    get_profit_analytics,
    get_refund_analytics,
    get_low_stock_products,
    get_outofstock_products,
    get_inventory_value,
    get_inventory_movement,
)

router = APIRouter(prefix="/analytics",tags=["Analytics"])

@router.get("/ping")
def ping():
    return {
        "msg":"Analytics module is working"
    }

@router.get("/dashboard",response_model=DashboardResponseSchema,status_code=status.HTTP_200_OK)
def dashboard_endpoint(db: Session = Depends(get_db)):
    return get_dashboard(db)

@router.get("/monthly-sales",response_model=list[MonthlySalesResponseSchema],status_code=status.HTTP_200_OK)
def monthly_sales_endpoint(db:Session=Depends(get_db),
                           _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST))):
    return get_monthly_sales(db)

@router.get("/top-products",response_model=list[TopProductResponseSchema],status_code=status.HTTP_200_OK)
def top_products_endpoint(db:Session=Depends(get_db),
                          _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST))):
    return get_top_products(db)

@router.get("/top-products-revenue",response_model=list[TopProductRevenueSchema],status_code=status.HTTP_200_OK)
def top_products_revenue_endpoint(db:Session=Depends(get_db),
                                  _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST))):
    return get_top_products_revenue(db)

@router.get("/top-customers",response_model=list[TopCustomerResponseSchema],status_code=status.HTTP_200_OK)
def top_customers_endpoint(db:Session=Depends(get_db),
                           _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST))):
    return get_top_customers(db)


@router.get("/top-categories",response_model=list[TopCategoriesResponseSchema],status_code=status.HTTP_200_OK)
def top_categories_endpoint(db:Session=Depends(get_db),
                            _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST))):
    return get_top_categories(db)

@router.get("/profit-analytics",response_model=list[ProfitAnalyticsResponseSchema],status_code=status.HTTP_200_OK)
def profit_analytics_endpoint(db:Session=Depends(get_db),
                              _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST))):
    return get_profit_analytics(db)



@router.get("/refund-analytics",response_model=RefundAnalyticsResponseSchema,status_code=status.HTTP_200_OK)
def refund_analytics(db:Session=Depends(get_db),
                     _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST))):
    return get_refund_analytics(db)


@router.get("/low-stock-products",response_model=list[LowStockResponseSchema],status_code=status.HTTP_200_OK)
def low_stock_product_endpoint(db:Session=Depends(get_db),
                               _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.INVENTORY_MANAGER))):
    return get_low_stock_products(db)


@router.get("/out-of-stock-products",response_model=list[OutofStockProductsResponseSchema],status_code=status.HTTP_200_OK)
def out_of_stock_products(db:Session=Depends(get_db),
                          _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.INVENTORY_MANAGER))):
    return get_outofstock_products(db)

@router.get("/inventory-value",response_model=InventoryValueResponseSchema,status_code=status.HTTP_200_OK)
def inventory_value_endpoint(db:Session=Depends(get_db),
                             _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.INVENTORY_MANAGER))):
    return get_inventory_value(db)

@router.get("/inventory-movement",response_model=InventoryMovementResponseSchema,status_code=status.HTTP_200_OK)
def inventory_movement_enpoint(db:Session=Depends(get_db),
                               _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.INVENTORY_MANAGER))):
    return get_inventory_movement(db)
