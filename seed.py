from faker import Faker
import uuid
import random
from datetime import datetime, timedelta
from database import SessionLocal, engine, Base
from models.category import Category
from models.product import Product
from models.supplier import Supplier
from models.inventory import Inventory
from models.sales import Sales

fake = Faker()
Base.metadata.create_all(bind=engine)

def generate_categories(count=12):
    categories = []
    category_types = [
        "Electronics", "Clothing", "Books", "Home & Garden", "Sports",
        "Toys & Games", "Beauty", "Automotive", "Food & Beverage", 
        "Health", "Office Supplies", "Pet Supplies"
    ]
    
    for name in category_types[:count]:
        categories.append(
            Category(
                id=uuid.uuid4(),
                name=name,
                descrition=fake.paragraph(nb_sentences=2)
            )
        )
    return categories

def generate_suppliers(count=40):
    return [
        Supplier(
            id=uuid.uuid4(),
            name=fake.company(),
            address=fake.address(),
            phone=fake.phone_number()
        ) for _ in range(count)
    ]

def generate_product_name():
    adjectives = ['Premium', 'Deluxe', 'Professional', 'Classic', 'Ultra', 'Smart', 'Eco', 'Pro', 'Elite', 'Advanced']
    product_types = {
        "Electronics": ['Laptop', 'Headphones', 'Smartphone', 'Tablet', 'Camera', 'Speaker', 'Monitor', 'Keyboard', 'Mouse'],
        "Clothing": ['T-Shirt', 'Jeans', 'Jacket', 'Shoes', 'Hat', 'Dress', 'Sweater', 'Socks', 'Belt'],
        "Books": ['Novel', 'Textbook', 'Magazine', 'Journal', 'Guide', 'Manual', 'Dictionary', 'Encyclopedia'],
        "Home & Garden": ['Lamp', 'Chair', 'Table', 'Pillow', 'Plant', 'Vase', 'Rug', 'Mirror', 'Clock'],
        "Sports": ['Ball', 'Racket', 'Shoes', 'Jersey', 'Equipment', 'Gloves', 'Helmet', 'Bag'],
        "Toys": ['Action Figure', 'Board Game', 'Puzzle', 'Doll', 'Car', 'Building Blocks', 'Robot'],
        "Beauty": ['Cream', 'Lotion', 'Shampoo', 'Perfume', 'Makeup', 'Brush', 'Mirror'],
        "Office": ['Pen', 'Notebook', 'Stapler', 'Calculator', 'Desk', 'Chair', 'Lamp']
    }
    
    adj = random.choice(adjectives)
    category = random.choice(list(product_types.keys()))
    item = random.choice(product_types[category])
    return f"{adj} {item}"

def generate_products(categories, count=100):
    products = []
    for _ in range(count):
        unit_price = round(random.uniform(10, 1000), 2)
        markup = random.uniform(1.1, 1.5)  # 10-50% markup
        category = random.choice(categories)
        
        products.append(
            Product(
                id=uuid.uuid4(),
                name=generate_product_name(),  # Using our custom function
                descrition=fake.text(max_nb_chars=200),
                unit_price=unit_price,
                sale_price=round(unit_price * markup, 2),
                category_id=category.id
            )
        )
    return products

def generate_inventory_records(products, suppliers, sales_data):
    inventory_records = []
    
    # Generate purchase records
    for product in products:
        total_sales_quantity = sum(
            sale.quantity_sold for sale in sales_data 
            if sale.product_id == product.id
        )
        
        # Calculate required purchase quantity (sales + buffer)
        # Ensure minimum purchase quantity is at least 10
        required_purchase = max(abs(total_sales_quantity) + random.randint(10, 50), 10)
        
        # Split into multiple purchase records
        while required_purchase > 0:
            # Ensure minimum purchase quantity is 1
            max_purchase = max(min(required_purchase, 100), 1)
            purchase_qty = random.randint(1, max_purchase)
            
            inventory_records.append(
                Inventory(
                    id=uuid.uuid4(),
                    date_purchased=fake.date_time_between(
                        start_date='-60d',
                        end_date='-30d'
                    ),
                    quantity=purchase_qty,
                    supplier_id=random.choice(suppliers).id,
                    product_id=product.id
                )
            )
            required_purchase -= purchase_qty
    
    # Generate sale records (negative quantities)
    for sale in sales_data:
        inventory_records.append(
            Inventory(
                id=uuid.uuid4(),
                date_purchased=sale.date_created,
                quantity=-sale.quantity_sold,
                product_id=sale.product_id
            )
        )
    
    return inventory_records

def generate_sales(products, count=300):
    sales = []
    for _ in range(count):
        product = random.choice(products)
        quantity = random.randint(1, 5)
        sales.append(
            Sales(
                id=uuid.uuid4(),
                date_created=fake.date_time_between(
                    start_date='-30d',
                    end_date='now'
                ),
                quantity_sold=quantity,
                totalBill=round(product.sale_price * quantity, 2),
                product_id=product.id
            )
        )
    return sales

def seed_database():
    db = SessionLocal()
    try:
        print("Starting database seeding...")
        
        # Generate and save categories
        print("Generating categories...")
        categories = generate_categories()
        db.bulk_save_objects(categories)
        db.commit()
        
        # Generate and save suppliers
        print("Generating suppliers...")
        suppliers = generate_suppliers()
        db.bulk_save_objects(suppliers)
        db.commit()
        
        # Generate and save products
        print("Generating products...")
        products = generate_products(categories)
        db.bulk_save_objects(products)
        db.commit()
        
        # Generate and save sales
        print("Generating sales...")
        sales = generate_sales(products)
        db.bulk_save_objects(sales)
        db.commit()
        
        # Generate and save inventory records
        print("Generating inventory records...")
        inventory = generate_inventory_records(products, suppliers, sales)
        db.bulk_save_objects(inventory)
        db.commit()
        
        print(f"""
Database seeded successfully!
Created:
- {len(categories)} categories
- {len(suppliers)} suppliers
- {len(products)} products
- {len(sales)} sales records
- {len(inventory)} inventory records
        """)

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()