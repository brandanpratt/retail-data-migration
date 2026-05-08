import random
import time
from faker import Faker
from sqlalchemy import create_engine, text

fake = Faker()

# SQL Server connection
DB_USER = "sa"
DB_PASSWORD = "YourStrongPassword123!"
DB_HOST = "localhost"
DB_PORT = "1433"
DB_NAME = "RetailDB"

connection_string = (
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    "?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
)

engine = create_engine(connection_string)

# Static stores
stores = [
    ("CBS Nassau", "Nassau"),
    ("CBS Freeport", "Freeport"),
    ("CBS Abaco", "Abaco"),
]

# Static products
products = [
    ("HP Laptop", "Electronics", 1200.00),
    ("Wireless Mouse", "Accessories", 45.99),
    ("Mechanical Keyboard", "Accessories", 129.99),
    ("Samsung Monitor", "Electronics", 399.99),
    ("USB-C Dock", "Accessories", 89.99),
    ("Office Chair", "Furniture", 249.99),
]

with engine.begin() as conn:

    print("Inserting stores...")

    for store in stores:
        conn.execute(
            text("""
                INSERT INTO stores (store_name, city)
                VALUES (:store_name, :city)
            """),
            {
                "store_name": store[0],
                "city": store[1]
            }
        )

    print("Inserting products...")

    for product in products:
        conn.execute(
            text("""
                INSERT INTO products (product_name, category, price)
                VALUES (:product_name, :category, :price)
            """),
            {
                "product_name": product[0],
                "category": product[1],
                "price": product[2]
            }
        )

    print("Generating customers and orders...")

    for i in range(1, 1001):

        first_name = fake.first_name()
        last_name = fake.last_name()

        conn.execute(
            text("""
                INSERT INTO customers (
                    first_name,
                    last_name,
                    email,
                    city
                )
                VALUES (
                    :first_name,
                    :last_name,
                    :email,
                    :city
                )
            """),
            {
                "first_name": first_name,
                "last_name": last_name,
                "email": fake.email(),
                "city": fake.city()
            }
        )

        # Create random order
        customer_id = i
        store_id = random.randint(1, 3)

        total_amount = round(random.uniform(50, 2500), 2)

        result = conn.execute(
            text("""
                INSERT INTO orders (
                    customer_id,
                    store_id,
                    total_amount
                )
                OUTPUT INSERTED.order_id
                VALUES (
                    :customer_id,
                    :store_id,
                    :total_amount
                )
            """),
            {
                "customer_id": customer_id,
                "store_id": store_id,
                "total_amount": total_amount
            }
        )

        order_id = result.scalar()

        # Add order items
        item_count = random.randint(1, 4)

        for _ in range(item_count):

            product_id = random.randint(1, 6)
            quantity = random.randint(1, 3)
            unit_price = round(random.uniform(20, 1500), 2)

            conn.execute(
                text("""
                    INSERT INTO order_items (
                        order_id,
                        product_id,
                        quantity,
                        unit_price
                    )
                    VALUES (
                        :order_id,
                        :product_id,
                        :quantity,
                        :unit_price
                    )
                """),
                {
                    "order_id": order_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": unit_price
                }
            )

        # Add payment
        conn.execute(
            text("""
                INSERT INTO payments (
                    order_id,
                    payment_method,
                    payment_amount
                )
                VALUES (
                    :order_id,
                    :payment_method,
                    :payment_amount
                )
            """),
            {
                "order_id": order_id,
                "payment_method": random.choice([
                    "Credit Card",
                    "Debit Card",
                    "Cash"
                ]),
                "payment_amount": total_amount
            }
        )

        # Batch pause every 100
        if i % 100 == 0:
            print(f"Inserted {i} customers/orders...")
            time.sleep(2)

print("Seed generation complete.")