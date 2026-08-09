from decimal import Decimal

from sqlalchemy import func, select,case
from sqlalchemy.orm import Session

from src.categories.models import CategoryModel
from src.customers.models import CustomerModel
from src.products.models import ProductModel
from src.orders.models import OrderModel
from src.orderitems.models import OrderItemModel
from src.refund.models import RefundModel
from src.inventory_logs.models import InventoryLogModel
from src.common.enum import OrderStatus, RefundStatus,InventoryReason
from src.analytics.dtos import(
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


def get_dashboard(db: Session):
    total_customers = db.scalar(
    select(func.count(CustomerModel.id))
    )
    total_products= db.scalar(
        select(func.count(ProductModel.id))
    )
    total_orders = db.scalar(
        select(func.count(OrderModel.id))
    )
    completed_orders = db.scalar(
        select(func.count(OrderModel.id)).where(
            OrderModel.status == OrderStatus.completed
        )
    )
    refunded_orders = db.scalar(
        select(func.count(OrderModel.id)).where(
            OrderModel.status == OrderStatus.refunded
        )
    )
    total_revenue =db.scalar(
        select(func.sum(OrderModel.grand_total)).where(
            OrderModel.status == OrderStatus.completed
        )
    ) or Decimal("0.00")

    total_refund_amount=db.scalar(
        select(func.sum(RefundModel.amount)).where(
            RefundModel.status == RefundStatus.approved
        )
    )or Decimal("0.00")

    low_stock_products = db.scalar(
        select(func.count(ProductModel.id)).where(
            ProductModel.stock_qty <= 10
        )
    )


    return DashboardResponseSchema (
        total_customers     = total_customers,
        total_products      = total_products,
        total_orders        = total_orders,
        completed_orders    = completed_orders,
        refunded_orders     = refunded_orders,
        total_revenue       = total_revenue,
        total_refund_amount = total_refund_amount,
        low_stock_products  = low_stock_products
    )

def get_monthly_sales(db:Session):
    monthly_sales = db.execute(
        select(
            func.to_char(OrderModel.order_date,"YYYY-MM").label("month"),
            func.count(OrderModel.id).label("total_orders"),
            func.sum(OrderModel.grand_total).label("total_revenue"),
        ).where(
            OrderModel.status == OrderStatus.completed

        ).group_by(
            func.to_char(
                OrderModel.order_date,"YYYY-MM"
            )
        ).order_by(
            func.to_char(OrderModel.order_date,"YYYY-MM")
        )
    ).all()

    return [
        MonthlySalesResponseSchema(
            month = row.month,
            total_orders= row.total_orders,
            total_revenue=row.total_revenue
        )
        for row in monthly_sales
    ]

def get_top_products(db:Session):
    units_sold = func.sum(OrderItemModel.quantity).label("units_sold")

    products = db.execute(
        select(ProductModel.name.label("product_name"),
               units_sold
        )
        .join(OrderItemModel.product)
        .join(OrderItemModel.order)
        .where(
            OrderModel.status == OrderStatus.completed
        )
        .group_by(
            ProductModel.id,
            ProductModel.name
        )
        .order_by(
            units_sold.desc()
        )
        .limit(10)
    ).all()

    return [
        TopProductResponseSchema(
            product_name=row.product_name,
            units_sold=row.units_sold
        )
        for row in products
    ]

def get_top_products_revenue(db:Session):
    revenue = func.sum(OrderItemModel.unit_price * OrderItemModel.quantity).label("revenue")

    products=db.execute(
        select(ProductModel.name.label("product_name"),
               revenue)
               .join(OrderItemModel.product)
               .join(OrderItemModel.order)
               .where(
                   OrderModel.status == OrderStatus.completed
               )
               .group_by(
                   ProductModel.id,
                   ProductModel.name
               ).
               order_by(
                   revenue.desc()
               ).
               limit(10)
    ).all()

    return [
        TopProductRevenueSchema(
            product_name=row.product_name,
            reveue= row.revenue
        )
    for row in products
    ]

def get_top_customers(db:Session):
    total_orders = func.count(OrderModel.id).label("total_orders") 
    total_spent = func.sum(OrderModel.grand_total).label("total_spent")

    customers = db.execute(
        select(CustomerModel.full_name.label("name"),
               total_orders,
               total_spent,
               ).join(
                     OrderModel
               ).where(
                   OrderModel.status == OrderStatus.completed
               ).group_by(
                   CustomerModel.id,CustomerModel.full_name
               ).order_by(
                total_spent.desc()
               ).limit(10)
    ).all()

    return [
        TopCustomerResponseSchema(
            name=row.name,
            total_orders=row.total_orders,
            total_spent=row.total_spent
        )
        for row in customers
    ]

def get_top_categories(db:Session):
    units_sold = func.sum(OrderItemModel.quantity).label("units_sold")
    revenue = func.sum(
        OrderItemModel.quantity * OrderItemModel.unit_price
    ).label("revenue")

    categories = db.execute(
        select(CategoryModel.name.label("name"),
               units_sold,
               revenue,
               )
               .join(CategoryModel.products)
               .join(ProductModel.order_items)
               .join(OrderItemModel.order)
               .where(OrderModel.status == OrderStatus.completed)
               .group_by(
                   CategoryModel.id,
                   CategoryModel.name,)
                .order_by(
                    revenue.desc()
                ).limit(10)   
    ).all()


    return [
        TopCategoriesResponseSchema(
            category_name=row.name,
            units_sold=row.units_sold,
            revenue=row.revenue
        )
        for row in categories
    ] 

def get_profit_analytics(db:Session):

    profit = (
        OrderItemModel.quantity * (OrderItemModel.unit_price - ProductModel.cost)
        ).label("profit")

    details = db.execute(
        select(ProductModel.name.label("product_name"),
               profit,
               )
               .join(ProductModel.order_items)
               .join(OrderItemModel.order)
               .where(OrderModel.status == OrderStatus.completed)
               .order_by(
                   profit.desc()
               )
               .limit(10)
    ).all() 

    return [
        ProfitAnalyticsResponseSchema(
            product_name=row.product_name,
            profit=row.profit
        )
        for row in details
    ] 

def get_refund_analytics(db:Session):
    total_refunds = db.scalar(
        select(func.count(RefundModel.id)
            ).where(
                RefundModel.status == RefundStatus.approved
            )
    )

    refund_amounts = db.scalar(
        select(func.sum(RefundModel.amount)
            ).where(
                RefundModel.status == RefundStatus.approved
            )
    )

    completed_orders = db.scalar(
        select(func.count(OrderModel.id)
            ).where(
                OrderModel.status == OrderStatus.completed
        )        
    )

    refund_rate = 0.0

    if completed_orders:
        refund_rate = round(
            (total_refunds/completed_orders) * 100,
            2
        )

    avg_refund_rate = round(db.scalar(
        select(func.avg(RefundModel.amount)
            ).where(
                RefundModel.status == RefundStatus.approved
            ),
        ),2
    )    

    return RefundAnalyticsResponseSchema(
        total_refunds=total_refunds,
        refund_amounts=refund_amounts,
        refund_rate=refund_rate,
        avg_refund_amount=avg_refund_rate
    )    

def get_low_stock_products(db:Session):

    products = db.scalars(
        select(ProductModel)
        .where(ProductModel.stock_qty <= 10)
        .order_by(ProductModel.stock_qty.asc())
    ).all()

    return [
        LowStockResponseSchema(
            product_name=product.name,
            category_name=product.category.name,
            stock_qty=product.stock_qty
        )
        for product in products
    ]

def get_outofstock_products(db:Session):
    products = db.scalars(
        select(ProductModel.id)
        .where(ProductModel.stock_qty == 0)
        .order_by(ProductModel.name.asc())
    ).all()

    return [
        OutofStockProductsResponseSchema(
            product_name=product.name,
            category_name=product.category.name
        )
        for product in products
    ]

def get_inventory_value(db:Session):

    inventory_value = db.scalar(
        select(
            func.sum(
                ProductModel.cost * ProductModel.stock_qty
            )
        )
    )or Decimal("0.00")

    return InventoryValueResponseSchema(
        inventory_value=inventory_value
    )

def get_inventory_movement(db:Session):

    result = db.execute(
        select(
            func.sum(
                case(
                    (InventoryLogModel.reason == InventoryReason.sale,func.abs(InventoryLogModel.change_qty),
                    ),
                    else_=0,
                )
            ).label("sales"),
            func.sum(
                case(
                    (InventoryLogModel.reason == InventoryReason.restock,func.abs(InventoryLogModel.change_qty),
                    ),
                    else_=0
                )
            ).label("restocks"),
            func.sum(
                case(
                    (InventoryLogModel.reason == InventoryReason.return_,func.abs(InventoryLogModel.change_qty),
                    ),
                    else_=0,
                )
            ).label("returns"),
            func.sum(
                case(
                    (InventoryLogModel.reason == InventoryReason.adjustment,func.abs(InventoryLogModel.change_qty),
                    ),
                    else_=0,
                )
            ).label("adjustments"),
            func.sum(
                case(
                    (InventoryLogModel.reason == InventoryReason.damage,func.abs(InventoryLogModel.change_qty),
                    ),
                    else_=0
                )
            ).label("damages"),
        )
    ).one()

    return InventoryMovementResponseSchema(
        sale=result.sales or 0,
        restock= result.restocks or 0,
        return_=result.returns or 0,
        adjustment=result.adjustments or 0,
        damage=result.damages or 0
    )

