from django.db import models


class Maincategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    maincategory = models.ForeignKey(Maincategory, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    color = models.CharField(max_length=20, default="Blue")
    size = models.CharField(max_length=20, default="MD")

    baseprice = models.IntegerField()
    discount = models.IntegerField(default=0,)
    finalprice = models.IntegerField()
    color: models.CharField(max_length=20)
    size: models.CharField(max_length=10)
    stock = models.BooleanField(default=True)
    description = models.TextField()
    pic1 = models.ImageField(upload_to="uploads/products")
    pic2 = models.ImageField(upload_to="uploads/products",
                             default=None, blank=True, null=True)
    pic3 = models.ImageField(upload_to="uploads/products",
                             default=None, blank=True, null=True)
    pic4 = models.ImageField(upload_to="uploads/products",
                             default=None, blank=True, null=True)

    def __str__(self):
        return self.name


class Buyer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    addressline1 = models.TextField(default="", null=True, blank=True)
    addressline2 = models.TextField(default="", null=True, blank=True)
    addressline3 = models.TextField(default="", null=True, blank=True)
    pin = models.TextField(default="", null=True, blank=True)
    city = models.TextField(default="", null=True, blank=True)
    state = models.TextField(default="", null=True, blank=True)
    pic = models.ImageField(upload_to="uploads/buyers",default=None, null=True, blank=True)
    otp= models.IntegerField(null=True, blank=True, default=1231212)

    def __str__(self):
        return self.username+" / "+self.email


orderStatusOptions = ((0, 'Order Placed'),
                      (1, 'Ready to Pack'),
                      (2, 'Packed'),
                      (3, 'Ready to Ship'),
                      (4, 'Shipped'),
                      (5, 'Order in Transit'),
                      (6, 'Product reached at final destination'),
                      (7, 'Out for Delievery'),
                      (8, 'Delievery'))
paymentStatusOptions = ((0, 'Pending'),
                        (1, 'Done'))
paymentModeOptions = ((0, 'COD'),
                      (1, 'Net Banking'))


class Checkout(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    paymentmode = models.IntegerField(choices=paymentModeOptions, default=0)
    paymentstatus = models.IntegerField(choices=paymentStatusOptions, default=0)
    orderstatus = models.IntegerField(choices=orderStatusOptions, default=0)
    subtotal = models.IntegerField()
    shipping = models.IntegerField()
    total = models.IntegerField()
    rppid = models.CharField(max_length=50, default='', null=True, blank=True)
    date= models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

class CheckoutProduct(models.Model):
    id= models.AutoField(primary_key=True)
    checkout= models.ForeignKey(Checkout, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    qty= models.IntegerField(default=0)
    total=models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)
    
class Wishlist(models.Model):
    id= models.AutoField(primary_key=True)
    buyer= models.ForeignKey(Buyer,on_delete=models.CASCADE)
    product= models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

statusOptions = ((0,"Active"),
                    (1,"Done"))
class Contact(models.Model):
    id= models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email= models.EmailField(max_length=50)
    phone= models.CharField(max_length=15)
    subject= models.CharField(max_length=200)
    message= models.TextField()
    status=models.IntegerField(choices=statusOptions,default=0)
    date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)+" "+self.email+" "+" "+self.subject[0:50]+"..."
    
    