from decimal import Decimal

def calculate_subtotal(items:list[tuple[Decimal,int]]) -> Decimal:
    subtotal = Decimal("0")

    for price,quantity in items:
        subtotal += price * quantity

    return subtotal

def calculate_discount(subtotal:Decimal,discount_percent:Decimal = Decimal("0"))->Decimal:
    return   (subtotal * discount_percent) / Decimal("100")

TAX_RATE = Decimal("18")

def calculate_tax(taxable_amount:Decimal)->Decimal:
    return (taxable_amount * TAX_RATE)/Decimal("100")

def calculate_grand_total(subtotal:Decimal,discount:Decimal,tax:Decimal):
    return (subtotal - discount) + tax 

def calculate_order_total(items:list[tuple[Decimal,int]],discount_percent:Decimal=Decimal("0"))->dict[str,Decimal]:

            subtotal = calculate_subtotal(items)

            discount = calculate_discount(subtotal=subtotal,discount_percent=discount_percent)

            taxable_amount = subtotal - discount

            tax = calculate_tax(taxable_amount)

            grand_total = calculate_grand_total(subtotal=subtotal,discount=discount,tax=tax)

            return {
                "subtotal":subtotal,
                "discount":discount,
                "tax":tax,
                "grand_total":grand_total
            }