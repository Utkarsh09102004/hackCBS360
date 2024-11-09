from django.db import models


# Customer Model
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


# Order Model
class Order(models.Model):
    PENDING = 'Pending'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELED = 'Canceled'

    ORDER_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
    ]

    order_id = models.AutoField(primary_key=True)
    order_status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default=PENDING
    )
    expected_delivery_date = models.DateField()
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.order_id} - {self.order_status}"
