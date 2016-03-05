from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
import parser
from django.conf import settings
from api.models import *
import celery
import re
from LinkedinAuth import LinkedinOauthClient
from .tasks import add_product,refresh
from rest_framework.exceptions import ParseError,ValidationError
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from time import sleep
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import urllib
from time import sleep
import requests
import pdb
LINKEDIN_CLIENT_ID='750l026y5ehsuh'
LINKEDIN_CLIENT_SECRET='b72h0CFesFgLqcME'
AUTHORIZATION_URL = 'https://www.linkedin.com/uas/oauth2/authorization'
ACCESS_TOKEN_URL = 'https://www.linkedin.com/uas/oauth2/accessToken'

class TenItemsSetPagination(PageNumberPagination):
	page_size = 10

class MyBasicAuthentication(BasicAuthentication):

	def authenticate(self, request):
		user, _ = super(MyBasicAuthentication, self).authenticate(request)
		login(request, user)
		return user, _

class Login(APIView):
	# authenticaion_classes = (SessionAuthentication,MyBasicAuthentication)
	# permission_classes = (IsAuthenticated,)
	def get_subscribed_product_data(self,user):
		product_list=[]
		subscribed_products = Subscription.objects.filter(user=user)
		for product in subscribed_products:
			data={}
			price =product.product.product_price
			data["id"] = product.product.product_id
			data["name"] = product.product.product_name
			data["availability"] = product.product.product_availability
			data["extra_data"] = product.product.procuct_extra_data
			data["image"]=product.product.product_image
			product_list.append(data)

		try:
			return product_list
		except:
			raise DataUnavailable()

	def post(self,request):
		
		username = request.data["username"]
		password = request.data["password"]
		user = authenticate(username = username,password = password)
		if user is not None:
			if user.is_active:
				#ie te user is active show subscribed products
				login(request, user)
				request.session["user_name"] = username
				subscribed_data = self.get_subscribed_product_data(username)
				print subscribed_data
				return render(request,'api/index.html',{"name":username,"data":subscribed_data})
			else:
				pass
		else:
			pass
		# if request.POST["type"]=="Linkedin":
		# 	username = request.POST["username"]
		# 	a=User.objects.get(email=username)
			
	def delete(self,request):
		logout(request)
	

@api_view(['GET', 'POST', ])
def Index(request, format=None):

	name=''	
	if request.GET.get('code'):
		code=request.GET["code"]
		getLinkedIn = LinkedinOauthClient(LINKEDIN_CLIENT_ID,LINKEDIN_CLIENT_SECRET)
		access_details = getLinkedIn.get_access_token(code)
		if getLinkedIn.is_authorized:
			content = getLinkedIn.getUserInfo()
			u = {
					"email":content["emailAddress"],
					"client_id":content["id"],
					"first_name":content["firstName"],
					"last_name":content["lastName"]
				}
			first_name = content["firstName"]
			last_name = content["lastName"]
			email = content["emailAddress"]
			client_id = content["id"]
			user = User(first_name=first_name,last_name=last_name,email=email,username=email)
			try:
				user.save()
				user_additional_info = CustomAuth(user=user,client_id=client_id,access_token=access_details["access_token"])
				user_additional_info.save()
			except:
				print "duplicate entry"
				pass
	return render(request,'api/index.html',name)

class ValidationFailed(ParseError):
	default_detail = 'url validation failed'

class Endpoint(APIView):
	
	def get(self,request):
		user = request.session.get("user_name")
		url = request.GET["url"]
		raw_asin = re.findall("product/(.*)/ref",url)
		raw_asin2 = re.findall("dp/([A-Z0-9]{,10})",url)
		if not (raw_asin or raw_asin2):
			raise ValidationFailed()
		result = add_product.delay(url,user)
		return Response(result.id)
	
class DataUnavailable(ParseError):
	default_detail = 'No data available for given page'

class PriceHistory(APIView):
	
	def get_product_data(self,id):

		products=PriceDetails.objects.filter(product__product_id=id)
		price_list = []
		for i in products:
			price =i.price
			date = i.date
			product_id = i.product.product_id
			data={"price":price,"date":date}
			price_list.append(data)
		try:
			return price_list
		except:
			raise DataUnavailable()
	
	def get(self,request,id=id):
		
		subscribed_product = Subscription.objects.filter(product__product_id=id)
		if not subscribed_product:
			subscribed_product = PriceDetails.objects.filter(product__product_id=id)
		
		if subscribed_product:
			for i in subscribed_product:
				id = i.product.product_id
				return Response(self.get_product_data(id))
		else:
			raise DataUnavailable()
class GetallProducts(ListAPIView):
	
	throttle_scope='test'
	def PagenateThis(self,objects,current_page,pages):
		paginator = Paginator(objects,pages)
		try:
			s=paginator.page(current_page)
		except PageNotAnInteger:
			raise DataUnavailable()

		except EmptyPage:
			s = paginator.page(paginator.num_pages)
		if s.has_next():
			next_page_number = s.next_page_number()	
		else:
			next_page_number = None
		if s.has_previous():
			previous_page_number = s.previous_page_number()
		else:
			previous_page_number = None
		data = {	'data':s,
					'next_page_number':next_page_number,
					'previous_page_number':previous_page_number
				}
		return data
	
	def get(self,request):
		if request.GET.get('page'):
			current_page = request.GET.get('page')
		else:
			current_page = 1

		if current_page:
			products_list = ProductData.objects.all().order_by('-id')
			paginated_data = self.PagenateThis(products_list,current_page,10)
			first_list = None
			next_url = paginated_data['next_page_number']
			previous_url = paginated_data['previous_page_number']
			page = {
						'next_url' : next_url,
						'previous_url' : previous_url
					}

		if not request.session.get("user_name"):
			Data = {}
			product_list=[]
			for i in paginated_data['data']:
				data={}
				data["id"] = i.product_id
				data["name"] = i.product_name
				data["availability"] = i.product_availability
				data["extra_data"]=i.procuct_extra_data
				data["image"] = i.product_image
				data['price'] = i.product_price
				data['product_previous_price'] = i.product_previous_price
				current_price = data['price']
				previous_price = data['product_previous_price']
				price_diff = float(current_price) - float(previous_price)
				data['price_diff'] = price_diff
				product_list.append(data)
			Data = {
						'product_list':product_list,
						'pagination':page
					}
			return Response(Data)
		
		else:
			logged_in_user = request.session["user_name"]
			subscribed_products = Subscription.objects.filter(user=logged_in_user)
			nextpage = self.PagenateThis(subscribed_products,current_page,10)
			next_url = nextpage['next_page_number']
			page = {
						'next_url' : next_url,
						'previous_url' : previous_url
					}

			product_list = []
			for product in subscribed_products:
				data={}
				data["id"] = product.product.product_id
				data["name"] = product.product.product_name
				data["availability"] = product.product.product_availability
				data["extra_data"] = product.product.procuct_extra_data
				data["image"] = product.product.product_image
				data['price'] = product.product.product_price
				data['product_previous_price'] = product.product.product_previous_price
		
				current_price = data['price'] if data['price'] else 0
				previous_price =data['product_previous_price'] if data['product_previous_price'] else 0
				price_diff = previous_price -current_price
				data['price_diff'] = price_diff
				product_list.append(data)
			
			Data = {
						'product_list':product_list,
						'pagination':page
					}
			
			try:
				if product_list:
					return Response(Data)
				else:
					raise DataUnavailable()
			except:
				raise DataUnavailable()

class GetsubscribedProducts(APIView):
	def get(self,request):
		
		if "user" in request.session:
			logged_in_user = request.session["user_name"]
			subscribed_products = Subscription.objects.filter(user=logged_in_user)
			product_list = []
			for product in subscribed_products:
				data={}
				price =product.product.product_price
				data["id"] = product.product.product_id
				data["name"] = product.product.product_name
				data["availability"] = product.product.product_availability
				data["extra_data"] = product.product.procuct_extra_data
				data["product_image"]=product.product.product_image
				product_list.append(data)
			try:
				return Response(product_list)
			except:
				raise DataUnavailable()
		

		# class Linkedin(APIView):
		# 	print "Linkedin view"
		# 	LINKEDIN_CLIENT_ID='750l026y5ehsuh'
		# 	LINKEDIN_CLIENT_SECRET='b72h0CFesFgLqcME'
		# 	def get(self,request):
		# 		getLinkedIn = LinkedinOauthClient(self.LINKEDIN_CLIENT_ID,self.LINKEDIN_CLIENT_SECRET)
		# 		code = request.GET['code']
		# 		getLinkedIn.get_access_token('code')
		# 		getLinkedIn.getUserInfo()

		# @api_view(['GET', 'POST', ])
def linkedin_login(request,format=None):
	getLinkedIn = LinkedinOauthClient(LINKEDIN_CLIENT_ID,LINKEDIN_CLIENT_SECRET)
	if getLinkedIn.is_authorized:
		content = getLinkedIn.getUserInfo()
	else:
		global profile_track
		profile_track = 'linkedin'
		linkedin_url = getLinkedIn.get_authorize_url()
		return HttpResponseRedirect(linkedin_url)

	context = {'title': 'linkedin example', 'content': content}
	return render(request, 'api/linkedin.html', context)