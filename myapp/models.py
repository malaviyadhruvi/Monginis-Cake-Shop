from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from PIL import Image,ImageDraw,ImageFont
import os
from django.utils.timezone import now 
from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen import canvas

class Registration(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)  # Link with Django's User model
    email = models.EmailField(max_length=50, unique=True)  # Email field stays here
    password = models.CharField(max_length=128)  # Password field stays here
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Other')
    mob_num = models.CharField(max_length=10, blank=True, default='0000000000')
    city = models.CharField(max_length=50, blank=True, null=True, default='Unknown')
    reg_date = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        """Hashes and sets the password."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Checks if the provided password matches the hashed password."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.user.username if self.user else "No User Linked"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        blank=True, 
        null=True
    )

    def __str__(self):
        return self.user.username

    def get_profile_picture(self):
        """Return the profile picture or generate a letter avatar."""
        if self.profile_picture:
            return self.profile_picture.url
        return f"/media/profile_pics/{self.user.username[0].upper()}.png"

class Category(models.Model):
    c_nm = models.CharField(max_length=100)  
    c_image = models.ImageField(upload_to='categories/', null=True, blank=True)

    def __str__(self):
        return self.c_nm 

class Product(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    

    def __str__(self):
        return self.name

class NewArrivals(models.Model):
    aname = models.CharField(max_length=50)
    aprice = models.IntegerField()
    aimage = models.ImageField(upload_to='new_arrivals/', null=True, blank=True)  # Add image field

    def __str__(self):
        return self.aname

class Cart(models.Model):
    pname = models.CharField(max_length=255)  # Increased max_length for flexibility
    pprice = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.pname

class Cake(models.Model):  # Renamed from 'cake' to 'Cake'
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cake/', null=True, blank=True)
    price = models.FloatField(max_length=10)

    def __str__(self):
        return self.name
    

class Pastry(models.Model):  # Renamed from 'pastry' to 'Pastry'
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pastry/', null=True, blank=True)
    price = models.FloatField(max_length=10)

    def __str__(self):
        return self.name
    
class Donut(models.Model):  # Renamed from 'pastry' to 'Pastry'
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='donut/', null=True, blank=True)
    price = models.FloatField(max_length=10)

    def __str__(self):
        return self.name
    
class Packaged_cake(models.Model):  # Renamed from 'pastry' to 'Pastry'
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='packaged_cake/', null=True, blank=True)
    price = models.FloatField(max_length=10)

    def __str__(self):
        return self.name
class Brownie(models.Model):  # Renamed from 'pastry' to 'Pastry'
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='brownie/', null=True, blank=True)
    price = models.FloatField(max_length=10)

    def __str__(self):
        return self.name
    
class Chocolate(models.Model):  # Renamed from 'pastry' to 'Pastry'
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='chocolate/', null=True, blank=True)
    price = models.FloatField(max_length=10)

    def __str__(self):
        return self.name
    
class Muffin(models.Model):  # Renamed from 'pastry' to 'Pastry'
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='muffin/', null=True, blank=True)
    price = models.FloatField(max_length=10)

    def __str__(self):
        return self.name
    
class Chocolate_bouquet(models.Model):  # Renamed from 'pastry' to 'Pastry'
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='chocolate_bouquet/', null=True, blank=True)
    price = models.FloatField(max_length=10)

    def __str__(self):
        return self.name
class OrderCart(models.Model):   
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    customer_name = models.CharField(max_length=255)
    address = models.TextField()
    pin = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    paymentMethod = models.CharField(max_length=50)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")  # ✅ Added order_status field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.customer_name} - ₹{self.totalAmount} - {self.get_order_status_display()}"

class OrderCartItem(models.Model):
    order = models.ForeignKey(OrderCart, on_delete=models.CASCADE, related_name="items")
    item_name = models.CharField(max_length=255)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    item_image = models.URLField()

    def __str__(self):
        return f"{self.item_name} ({self.quantity}x)"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Link order to user
    name = models.CharField(max_length=100, blank=True, default='')
    pnm = models.CharField(max_length=255, blank=True, default='', verbose_name="Product Name")
    prp = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Product Price")
    qty = models.PositiveIntegerField(default=1) 
    tp = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total Price")
    no = models.CharField(max_length=10, default='')
    pin = models.CharField(max_length=6, default='')
    city = models.CharField(max_length=10, blank=True, default='', null=True)
    address = models.CharField(max_length=255, blank=True, default='', null=True)
    created_at = models.DateTimeField(default=now)  
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Default status is "Pending"

    def generate_invoice(self):
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(200,1000,f"Monginis Invoice")
        p.drawString(100, 800, f"Invoice for Order ID: {self.id}")
        p.drawString(100, 780, f"Customer: {self.name}")
        p.drawString(100, 760, f"Product: {self.pnm}")
        p.drawString(100, 740, f"Quantity: {self.qty}")
        p.drawString(100, 720, f"Total Price: ₹{self.tp}")
        
        p.drawString(100, 680, "Thank you for your order!")

        p.showPage()
        p.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f"invoice_{self.id}.pdf")
    

    def __str__(self):
        return f"Order {self.id} - {self.pnm} - {self.get_order_status_display()}"
    


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('qr', 'QR Code'),
        ('cod', 'Cash on Delivery'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    order = models.OneToOneField('Order', on_delete=models.CASCADE,null=True,blank=True)  # Link to the order
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS,default='None')
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Payment of ₹{self.amount} by {self.user.username} via {self.get_payment_method_display()}"
