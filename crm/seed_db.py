import os
import django
from datetime import datetime, timedelta
import random

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql_crm.settings")
django.setup()

from crm.models import Customer, Product, Order

# ---------- Seed Customers ----------
customers_data = [
    {"name": "Alice", "email": "alice@example.com", "phone": "+1234567890"},
    {"name": "Bob", "email": "bob@example.com", "phone": "123-456-7890"},
    {"name": "Carol", "email": "carol@example.com", "phone": "+1987654321"},
]

customers = []
for c in customers_data:
    cust, created = Customer.objects.get_or_create(email=c["email"], defaults=c)
    customers.append(cust)
print(f"Seeded {len(customers)} customers")

# ---------- Seed Products ----------
products_data = [
    {"name": "Laptop", "price": 999.99, "stock": 10},
    {"name": "Mouse", "price": 25.50, "stock": 50},
    {"name": "Keyboard", "price": 49.99, "stock": 30},
]

products = []
for p in products_data:
    prod, created = Product.objects.get_or_create(name=p["name"], defaults=p)
    products.append(prod)
print(f"Seeded {len(products)} products")

# ---------- Seed Orders ----------
for _ in range(5):
    customer = random.choice(customers)
    selected_products = random.sample(products, k=random.randint(1, len(products)))
    total_amount = sum(p.price for p in selected_products)
    order_date = datetime.now() - timedelta(days=random.randint(0, 30))
    order = Order.objects.create(customer=customer, total_amount=total_amount, order_date=order_date)
    order.products.set(selected_products)
print("Seeded 5 random orders")

print("Database seeding complete!")
