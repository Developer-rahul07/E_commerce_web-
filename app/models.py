from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator,MinLengthValidator

# Create your models here.
STATE_CHOICES = (
   ("AN","Andaman and Nicobar Islands"),
   ("AP","Andhra Pradesh"),
   ("AR","Arunachal Pradesh"),
   ("AS","Assam"),
   ("BR","Bihar"),
   ("CG","Chhattisgarh"),
   ("CH","Chandigarh"),
   ("DN","Dadra and Nagar Haveli"),
   ("DD","Daman and Diu"),
   ("DL","Delhi"),
   ("GA","Goa"),
   ("GJ","Gujarat"),
   ("HR","Haryana"),
   ("HP","Himachal Pradesh"),
   ("JK","Jammu and Kashmir"),
   ("JH","Jharkhand"),
   ("KA","Karnataka"),
   ("KL","Kerala"),
   ("LA","Ladakh"),
   ("LD","Lakshadweep"),
   ("MP","Madhya Pradesh"),
   ("MH","Maharashtra"),
   ("MN","Manipur"),
   ("ML","Meghalaya"),
   ("MZ","Mizoram"),
   ("NL","Nagaland"),
   ("OD","Odisha"),
   ("PB","Punjab"),
   ("PY","Pondicherry"),
   ("RJ","Rajasthan"),
   ("SK","Sikkim"),
   ("TN","Tamil Nadu"),
   ("TS","Telangana"),
   ("TR","Tripura"),
   ("UP","Uttar Pradesh"),
   ("UK","Uttarakhand"),
   ("WB","West Bengal")
)

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    locality = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES ,  max_length=250)

    def __str__(self):
        # return str(self.id)
        return str(self.name)

CATEGORY_CHOICES =(
('M' , 'Mobile'),
('L' , 'Laptop'),
('TW' , 'Top Wear'),
('BW' , 'Bottom Wear'),
('R' , 'Random')

)

class Product(models.Model):
    title = models.CharField(max_length=50)
    selling_prize = models.FloatField()
    discount_prize = models.FloatField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=3)
    product_image = models.ImageField(upload_to='productimg')

    
    def __str__(self):
        return str(self.id)
     
class Cart(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    
    def __str__(self):
        return str(self.id)
        # return str(self.name)

# indiviusal amount show karwana checkcart m .. 1st option
@property
def total_cost(self):
    return self.quantity * self.product.discount_prize

    # or ka Secoand options h : {{item.product.discount_prize}}


STATUS_CHOICES =(
('Accepted', 'Accepted'),
('Packed', 'Packed'),
('On The Way', 'On The Way'),
('Delivered', 'Delivered'),
('Cancel', 'Cancel')
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    customer =models.ForeignKey(Customer , on_delete=models.CASCADE)
    product = models.ForeignKey(Product ,on_delete=models.CASCADE)
    orderes_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100 ,choices=STATUS_CHOICES,default='Pending')
    quantity = models.PositiveIntegerField(default=1)

    

