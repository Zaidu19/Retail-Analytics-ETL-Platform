from scripts.database import get_session
from scripts.utils import fake
from decimal import Decimal
from sqlalchemy import select

from src.categories.models import CategoryModel
from src.products.service import create_product
from src.products.dtos import ProductCreateSchema

def seed_products():
    db = get_session()

    print("Seeding products...")

    category_ids = db.scalars(
        select(CategoryModel.id)
    ).all()

    import random
    for _ in range(100):
        category_id = random.choice(category_ids)  
        create_product(
            ProductCreateSchema(
                name=fake.unique.word().title(),
                description=fake.text(max_nb_chars=100),
                category_id=category_id,
                price=Decimal(str(fake.random_int(500, 5000))),
                cost=Decimal(str(fake.random_int(200, 4000))),
                stock_qty=fake.random_int(300, 500),
            ),
            db,
        )              

        db.close()

        print("✅ Products seeded successfully.")    