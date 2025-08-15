import os
import django
import random
from django.utils import timezone

# -------------------------
# Setup Django environment
# -------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql_crm.settings")
django.setup()

from crm.models import Customer, Product, Order

# -------------------------
# Seed Customers
# -------------------------
def seed_customers():
    customers_data = [
        {"name": "Alice Johnson", "email": "alice@example.com", "phone": "+1234567890"},
        {"name": "Bob Smith", "email": "bob@example.com", "phone": "123-456-7890"},
        {"name": "Carol Davis", "email": "carol@example.com", "phone": "+1987654321"},
        {"name": "David Brown", "email": "david@example.com", "phone": None},
    ]

    created = 0
    for c in customers_data:
        if not Customer.objects.filter(email=c["email"]).exists():
            Customer.objects.create(**c)
            created += 1

    print(f"{created} customers created.")

# -------------------------
# Seed Products
# -------------------------
def seed_products():
    products_data = [
        {"name": "Laptop", "price": 999.99, "stock": 10},
        {"name": "Smartphone", "price": 499.99, "stock": 20},
        {"name": "Tablet", "price": 299.99, "stock": 15},
        {"name": "Headphones", "price": 79.99, "stock": 50},
    ]

    created = 0
    for p in products_data:
        if not Product.objects.filter(name=p["name"]).exists():
            Product.objects.create(**p)
            created += 1

    print(f"{created} products created.")

# -------------------------
# Seed Orders
# -------------------------
def seed_orders():
    customers = list(Customer.objects.all())
    products = list(Product.objects.all())

    if not customers or not products:
        print("Cannot seed orders: no customers or products found.")
        return

    created = 0
    for _ in range(5):  # create 5 random orders
        customer = random.choice(customers)
        selected_products = random.sample(products, k=random.randint(1, len(products)))
        total_amount = sum(p.price for p in selected_products)
        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount,
            order_date=timezone.now()
        )
        order.products.set(selected_products)
        created += 1

    print(f"{created} orders created.")

# -------------------------
# Run all seeders
# -------------------------
if __name__ == "__main__":
    seed_customers()
    seed_products()
    seed_orders()
    print("Database seeding complete!")
