from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from paystackease import PayStackBase

# Create your models here.

# Instantiate PayStackBase
paystack_sync = PayStackBase()


STATE_CHOICES = (
    ('Abia','Abia'),
    ('Anambra','Anambra'),
    ('Adamawa','Adamawa'),
    ('Abuja','Abuja'),
    ('Akwa-ibom','Akwa-ibom'),
    ('Benue','Benue'),
    ('Bauchi','Bauchi'),
    ('Calabar','Calabar'),
    ('Delta','Delta'),
    ('Edo','Edo'),
    ('Enugu','Enugu'),
    ('Ebonyi','Ebonyi'),
    ('Imo','Imo'),
    ('Lagos','Lagos'),
    ('Oyo','Oyo'),
    ('Jos','Jos'),
    ('Ogun','Ogun'),
    ('Osun','Osun'),
    ('Kebbi','Kebbi'),
    ('Kogi','Kogi'),
    ('Rivers','Rivers'),
    ('Borno','Borno'),
    ('Gombe','Gombe'),
    ('Taraba','Taraba'),
    ('Ondo','Ondo'),
)


CATEGORY_CHOICES=(
    ('EL','Electronics'),
    ('PH','Phone'),
    ('LP','Laptop'),
    ('FE','FemaleWear'),
    ('MW','MaleWear'),
    ('FW','FootWear'),
    ('AC','Accessory'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.title


class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=100)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


class OrderPlaced(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, null=True, blank=True)
    order_code = models.CharField(max_length=255, unique=True, blank=True, null=True)
    payment_completed = models.BooleanField(default=False)
    total_amount = models.PositiveIntegerField(default=0)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

    def save(self, *args, **kwargs):
        if not self.order_code and self.payment and self.payment.verified:
            self.order_code = f"ORD-{self.payment.ref}"
        super().save(*args, **kwargs)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(OrderPlaced, on_delete=models.CASCADE, null=True, blank=True, related_name='payments')
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=255, null=True, blank=True, unique=True)
    email = models.EmailField(default='')
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - Payment {self.id}"

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = paystack_sync.utils.generate_reference()
        super().save(*args, **kwargs)

    def verify_payment(self):
        status, result = paystack_sync.transactions.verify(self.ref)
        if status and result['status']:
            self.verified = True
            self.save()

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)