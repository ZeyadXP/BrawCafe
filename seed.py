"""
Run once to seed the database with default menu items.
Usage: python seed.py
"""
from database import SessionLocal, engine, Base
from models import MenuItem

Base.metadata.create_all(bind=engine)

DEFAULT_MENU = [
    {"name": "Espresso",          "emoji": "☕", "category": "Coffee",      "price": 3.50, "description": "Rich double shot, velvety crema",           "is_new": False},
    {"name": "Flat White",        "emoji": "🥛", "category": "Coffee",      "price": 4.75, "description": "Silky micro-foam with espresso",             "is_new": False},
    {"name": "Iced Matcha Latte", "emoji": "🍵", "category": "Tea",         "price": 5.50, "description": "Ceremonial grade matcha, oat milk",          "is_new": True },
    {"name": "Croissant",         "emoji": "🥐", "category": "Pastries",    "price": 3.25, "description": "Butter-laminated, flaky layers",             "is_new": False},
    {"name": "Avocado Toast",     "emoji": "🥑", "category": "Food",        "price": 8.50, "description": "Sourdough, smashed avo, chili flakes",       "is_new": False},
    {"name": "Cold Brew",         "emoji": "🧊", "category": "Cold Drinks", "price": 5.00, "description": "18-hour steep, smooth & bold",               "is_new": True },
    {"name": "Almond Croissant",  "emoji": "🍮", "category": "Pastries",    "price": 4.00, "description": "Filled with frangipane, toasted almonds",    "is_new": False},
    {"name": "Cappuccino",        "emoji": "☕", "category": "Coffee",      "price": 4.50, "description": "Equal parts espresso, milk, foam",           "is_new": False},
    {"name": "Acai Bowl",         "emoji": "🍇", "category": "Food",        "price": 10.00,"description": "Blended acai, granola, fresh fruit",         "is_new": True },
    {"name": "Lemonade",          "emoji": "🍋", "category": "Cold Drinks", "price": 4.00, "description": "Freshly squeezed, hint of mint",             "is_new": False},
    {"name": "Earl Grey",         "emoji": "🫖", "category": "Tea",         "price": 3.50, "description": "Loose leaf, bergamot, served hot",           "is_new": False},
    {"name": "Banana Bread",      "emoji": "🍌", "category": "Pastries",    "price": 3.75, "description": "Moist, walnuts, hint of cinnamon",           "is_new": False},
]

def seed():
    db = SessionLocal()
    existing = db.query(MenuItem).count()
    if existing > 0:
        print(f"Database already has {existing} menu items — skipping seed.")
        db.close()
        return

    for item_data in DEFAULT_MENU:
        db.add(MenuItem(**item_data))
    db.commit()
    print(f"✅ Seeded {len(DEFAULT_MENU)} menu items into the database.")
    db.close()

if __name__ == "__main__":
    seed()
