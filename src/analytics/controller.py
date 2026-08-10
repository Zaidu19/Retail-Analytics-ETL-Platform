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

@router.get("/dashboard",summary="Dashboard KPIs",
            description="Returns key buisness metrics such as revenue,orders,refunds, and inventory.",
            response_model=DashboardResponseSchema,status_code=status.HTTP_200_OK)
def dashboard_endpoint(db: Session = Depends(get_db)):
    return get_dashboard(db)

@router.get("/monthly-sales",response_model=list[MonthlySalesResponseSchema],status_code=status.HTTP_200_OK,
            summary="Monthly Sales Analytics",
            description="Returns monthly sales, average order value, highest order value,"
            " and lowest order value for completed orders.")
def monthly_sales_endpoint(db:Session=Depends(get_db),
                           _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST))):
    return get_monthly_sales(db)

@router.get("/top-products",response_model=list[TopProductResponseSchema],status_code=status.HTTP_200_OK,
            summary="Top Selling Products by Units Sold.",
            description="Returns the highest-selling products based on completed orders.")
def top_products_endpoint(db:Session=Depends(get_db),
                          _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST))):
    return get_top_products(db)

@router.get("/top-products-revenue",response_model=list[TopProductRevenueSchema],status_code=status.HTTP_200_OK,
            summary="Top Selling Products by Revenue.",
            description="Returns the highest-selling products based on completed orders.")
def top_products_revenue_endpoint(db:Session=Depends(get_db),
                                  _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST))):
    return get_top_products_revenue(db)

@router.get("/top-customers",response_model=list[TopCustomerResponseSchema],status_code=status.HTTP_200_OK,
            summary="Top Customers",
            description="Returns customers ranked by completed orders and total spending.")
def top_customers_endpoint(db:Session=Depends(get_db),
                           _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST))):
    return get_top_customers(db)


@router.get("/top-categories",response_model=list[TopCategoriesResponseSchema],status_code=status.HTTP_200_OK,
            summary="Category Sales Analytics",
            description="Returns sales performance grouped by product category.")
def top_categories_endpoint(db:Session=Depends(get_db),
                            _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST))):
    return get_top_categories(db)

@router.get("/profit-analytics",response_model=list[ProfitAnalyticsResponseSchema],status_code=status.HTTP_200_OK,
            summary="Profit Analytics",
            description="Returns profit of a products based on (unit_price - product_cost) * quantity.")
def profit_analytics_endpoint(db:Session=Depends(get_db),
                              _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST))):
    return get_profit_analytics(db)



@router.get("/refund-analytics",response_model=RefundAnalyticsResponseSchema,status_code=status.HTTP_200_OK,
            summary="Refund Analytics",
            description="Returns refund count, refund amount, and refund rate.")
def refund_analytics(db:Session=Depends(get_db),
                     _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.BUSINESS_ANALYST))):
    return get_refund_analytics(db)


@router.get("/low-stock-products",response_model=list[LowStockResponseSchema],status_code=status.HTTP_200_OK,
            summary="Low Stock Products",
            description="Returns products whose stock quantity is at or below the configured threshold.")
def low_stock_product_endpoint(db:Session=Depends(get_db),
                               _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.INVENTORY_MANAGER))):
    return get_low_stock_products(db)


@router.get("/out-of-stock-products",response_model=list[OutofStockProductsResponseSchema],status_code=status.HTTP_200_OK,
            summary="Out of Stock Products",
            description="Returns all products that are currently out of stock.")
def out_of_stock_products(db:Session=Depends(get_db),
                          _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.INVENTORY_MANAGER))):
    return get_outofstock_products(db)

@router.get("/inventory-value",response_model=InventoryValueResponseSchema,status_code=status.HTTP_200_OK,
            summary="Inventory Value",
            description="Returns the total monetary value of current inventory based on product cost and stock quantity.")
def inventory_value_endpoint(db:Session=Depends(get_db),
                             _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.INVENTORY_MANAGER))):
    return get_inventory_value(db)

@router.get("/inventory-movement",response_model=InventoryMovementResponseSchema,status_code=status.HTTP_200_OK,
            summary="Inventory Movements",
            description="Returns inventory movement statistics grouped by sales, returns, restocks, adjustments, and damaged items.")
def inventory_movement_enpoint(db:Session=Depends(get_db),
                               _:UserModel=Depends(require_roles(UserRole.ADMIN,UserRole.INVENTORY_MANAGER))):
    return get_inventory_movement(db)
