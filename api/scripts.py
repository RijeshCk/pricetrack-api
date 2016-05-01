from django.core.mail import send_mail
from price_track_api import settings

def send_email_notification(msg):
	subject = 'Pricetrack API notification'
	message = msg
	send_mail(subject, message, 'rijesh471@gmail.com' , ['rijesh36@gmail.com'], fail_silently=False)