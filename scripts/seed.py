import src.db.models

from scripts.users import seed_users
from scripts.customers import seed_customers
from scripts.categories import seed_categories
from scripts.products import seed_products
from scripts.orders import seed_orders
from scripts.refunds import seed_refunds


def main():
    print("Starting database seeding...\n")

    #seed_users()
    #seed_customers()
    #seed_categories()
    #seed_products()
    #seed_orders()
    seed_refunds()

    print("\nDatabase seeded successfully!")


if __name__ == "__main__":
    main()