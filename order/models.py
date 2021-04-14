from django.db import models

STATUS_CHOICES = (
    # ('front-end', 'backend')
    ('Pending', 'Pending'),
    ('Out Of Delivery', 'Out Of Delivery'),
    ('Delivered', 'Delivered'),
)

# Create your models here.
class Order(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='INR Order Total')
    emailAddress = models.EmailField(max_length=250, blank=True, verbose_name = 'Email Address')
    created = models.DateTimeField(auto_now_add=True)
    billingName = models.CharField(max_length=250, blank=True)
    billingAddress1 = models.CharField(max_length=250, blank=True)
    billingCity = models.CharField(max_length=250, blank=True)
    billingPostcode = models.CharField(max_length=10, blank=True)
    billingCountry =  models.CharField(max_length=200, blank=True)
    shippingName =  models.CharField(max_length=250, blank=True)
    shippingAddress1 = models.CharField(max_length=250, blank=True)
    shippingCity = models.CharField(max_length=250, blank=True)
    shippingPostcode = models.CharField(max_length=10, blank=True)
    shippingCountry = models.CharField(max_length=200, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='Pending')
    # status and its category codes and show it on the order details.
    # check views to create a cancel order request

    class Meta:
        db_table = 'Order'
        ordering = ['-created'] #to show the latest post on the top

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.CharField(max_length=250)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='INR Order Total')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        db_table = 'OrderItem'

    def sub_total(self):
        return self.quantity * self.price
    def __str__(self):
        return self.product
