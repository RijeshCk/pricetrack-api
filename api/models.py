from django.db import models
from django.contrib.auth.models import User

class ProductData(models.Model):
	product_name = models.CharField(max_length=200,blank=True,)
	product_price =models.FloatField()
	product_url = models.URLField(max_length=200,)
	product_id = models.CharField(max_length=200,unique=True)
	product_previous_price = models.FloatField(default=0)
	procuct_extra_data = models.TextField()
	product_availability = models.CharField(max_length=50)
	product_image = models.CharField(max_length=200,blank=True)

class PriceDetails(models.Model):
	price = models.FloatField()
	product = models.ForeignKey(ProductData)
	date = models.DateTimeField(auto_now_add=True)
	
class Subscription(models.Model):
	user = models.CharField(max_length=50)
	product = models.ForeignKey(ProductData)

class CustomAuth(models.Model):
	user = models.OneToOneField(User)
	client_id = models.CharField(max_length=20)
	access_token  =models.CharField(max_length=100)
