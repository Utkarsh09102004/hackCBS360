# import os
# import django
# from datetime import date, timedelta
#
# # Set up Django environment
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hacksCBSproject.settings")
# django.setup()
#
# # Import models
# from api.models import Customer, Order
#
# # Populate data
# customer1 = Customer.objects.create(name="John Doe", email="johndoe@example.com", phone_number="1234567890")
# customer2 = Customer.objects.create(name="Jane Smith", email="janesmith@example.com", phone_number="0987654321")
# customer3 = Customer.objects.create(name="Alice Johnson", email="alicej@example.com", phone_number="5555555555")
#
# Order.objects.create(
#     order_status=Order.PENDING,
#     expected_delivery_date=date.today() + timedelta(days=7),
#     customer=customer1
# )
#
# Order.objects.create(
#     order_status=Order.SHIPPED,
#     expected_delivery_date=date.today() + timedelta(days=3),
#     customer=customer2
# )
#
# Order.objects.create(
#     order_status=Order.DELIVERED,
#     expected_delivery_date=date.today(),
#     customer=customer3
# )
#
# Order.objects.create(
#     order_status=Order.CANCELED,
#     expected_delivery_date=date.today() + timedelta(days=5),
#     customer=customer1
# )
#
# print("Data populated successfully.")


import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hacksCBSproject.settings")
django.setup()

# Import models
from api.models import Customer, Order

# Retrieve and display all Customer records
print("Customers:")
for customer in Customer.objects.all():
    print(f"ID: {customer.customer_id}, Name: {customer.name}, Email: {customer.email}, Phone: {customer.phone_number}")

# Retrieve and display all Order records
print("\nOrders:")
for order in Order.objects.all():
    print(f"Order ID: {order.order_id}, Status: {order.order_status}, Expected Delivery: {order.expected_delivery_date}, Customer: {order.customer.name}")
