from celery import shared_task
from api.models import *
import parser
import re
import datetime
from scripts import send_email_notification
import requests

@shared_task
def add_product(url,user):
	
	raw_asin = re.findall("product/([A-Z0-9]{,10})/",url)
	if raw_asin:
		asin = raw_asin[0]
	else:
		asin = re.findall("dp/([A-Z0-9]{,10})",url)[0]
	try:
		data_from_db = ProductData.objects.get(product_id=asin)
		try:
			d=Subscription.objects.get(user = user,product=data_from_db)
			print "here new subscripton added"
		except:
			print "except"
			Subscription(user = user,product=data_from_db).save()
			print "saved"

	except ProductData.DoesNotExist:
		print "ProductData.DoesNotExist"
		data = parser.parse(url)
		price = data["price"]
		availability = data["availability"]
		product_id = data["product_id"]
		DatafromSite = ProductData(product_price = price,product_previous_price=price,product_name = data["name"],product_availability = availability,product_url = url,product_id=product_id,product_image=data["image"])
		DatafromSite.save()
		PriceData = PriceDetails(price=price,product=DatafromSite,date=datetime.datetime.now())
		PriceData.save()
		Subscription(user = user,product=DatafromSite).save()
		return data

@shared_task
def refresh():
	print "....................refresh beging here..........."
	send_email_notification('Product Refresh started')
	products_to_refresh = ProductData.objects.all()

	for i in products_to_refresh:
		url = i.product_url
		data = parser.parse(url)
		price = data["price"]
		product_availability = data['availability']
		
		PriceData = PriceDetails(price = price, product = i, date = datetime.datetime.now())
		PriceData.save()
		i.product_availability = product_availability
		i.product_previous_price  = i.product_price
		i.product_price = price
		try:
			i.save()
		except:
			print "in except url is ",url
		print "updating......",i.product_id
	send_email_notification('Product Refresh Completed')

@shared_task
def keep_alive_task():
	print "in keep alive task"
	response = requests.get("https://pricetrack-api.herokuapp.com/index")
	print response