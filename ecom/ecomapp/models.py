from django.db import models
from django.contrib.auth.models import  AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone




class CustomUser(AbstractUser):
    is_seller=models.BooleanField(default=False)
    is_customer=models.BooleanField(default=False)
    

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category/', blank=True, null=True)

    def __str__(self):
        return self.name
    


class Sellerdetails(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Cancelled', 'Cancelled'),
    ]
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    user=models.OneToOneField('CustomUser',on_delete=models.CASCADE,related_name='seller')
    username=models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    email=models.EmailField(max_length=100)
    Logo = models.ImageField(upload_to='seller_logo/', blank=True, null=True)
    password=models.CharField(max_length=8)
    application_date= models.DateTimeField(default=timezone.now)

    

    def __str__(self):
        return self.name


# Product Model
class Product(models.Model):
    seller=models.ForeignKey(Sellerdetails,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    is_sale=models.BooleanField(default=False)
    sale_price=models.DecimalField(max_digits=10, decimal_places=2 ,null=True,blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    

    def __str__(self):
        return self.name
    



# Customer Model
class Customer(models.Model):
    user=models.OneToOneField('CustomUser',on_delete=models.CASCADE,related_name='customer')
    Name=models.CharField(max_length=100)
    Age=models.IntegerField()
    Phone=models.IntegerField()
    Email=models.EmailField(max_length=100)
    Image = models.ImageField(upload_to='customer/', blank=True, null=True)
    



    def __str__(self):
        return self.user.username

# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     address = models.CharField(max_length=255)
#     phone = models.CharField(max_length=15, blank=True)

#     def __str__(self):
#         return self.user.username


# Cart Model
# class Cart(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Cart for {self.customer.user.username}"


# CartItem Model
class Cart(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    totalprice = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart"


# Order Model

class Order(models.Model):
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Orderplaced', 'Orderplaced'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='order')
    shipping_address=models.TextField()
    post=models.CharField(max_length=50)
    pincode= models.IntegerField()
    district=models.CharField(max_length=100)
    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    grand_total=models.PositiveIntegerField()
    is_paid=models.BooleanField(default=False)
    is_cod=models.BooleanField(default=False)
    is_cancelled=models.BooleanField(default=False)
    is_shipped=models.BooleanField(default=False)
    is_delivered=models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.customer.user.username}"


# OrderItem Model

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='orderitem')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    totalprice=models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order {self.order.id}"
    


class Review(models.Model):
    STATUS_CHOICES = [
        
        ('Excellent', 'Excellent'),
        ('Verygood', 'Verygood'),
        ('Average', 'Average'),
        ('Below Average', 'Below Average'),
        ('Poor', 'Poor'),

    ]
    user=models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status=models.CharField(max_length=30, choices=STATUS_CHOICES, default='Poor')
    review=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    rating=models.IntegerField()





