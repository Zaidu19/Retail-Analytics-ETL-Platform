from scripts.database import get_session

from src.categories.service import create_category
from src.categories.dtos import CategoryCreateSchema

def seed_categories():
    db = get_session()

    print("Seeding categories...")

    categories = [
        "Electronics",
        "Fashion",
        "Home & Kitchen",
        "Beauty",
        "Sports",
        "Books",
        "Toys",
        "Groceries",
        "Furniture",
        "Automotive",
    ]
    for category in categories:
        create_category(
            CategoryCreateSchema(
                name=category,
                description=f"Products related to {category.lower()}.",
            ),
            db,
        )        

        db.close()

    print("✅ Categories seeded successfully.")    