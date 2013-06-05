''' CUSTOMIZED AUTHENTICATION BACKEND '''
import hmac
import base64
from time import time
from django.contrib.auth.models import User

class AuthenticationBackend(object):
	
	def __init__(self,):
		self.sekret = "F1eFi2G2+UlIrv1uhY7jsOGsen3JA6NZregtaGPf8wE="

	def hmac(self, token):
		print "token: " + token
		#global sekret
		print "sekret: " + self.sekret
		hmaccer = hmac.new(base64.b64decode(self.sekret))
		hmaccer.update(token)
		digest = hmaccer.digest()
		return digest


	def add_padding_to_password(self, password):
		modulo = len(password) % 4
		print "modulo: " , modulo

		dict = { 
					2: "==",
					3: "="
				}

		new_pw = password + dict[modulo]
		return new_pw

	def authenticate(self, username = None, password = None):
		print "Username = " + username
		print "Passwrod = " + str(type(password))
		parts = base64.b64decode(username)
		print "parts: " + parts
		expiry = parts.split(':')[1]
		print "expiry: " + expiry
		realuser = parts.split(':')[0]
		print "realuser: " + realuser

		import sys
		print "sys.version: " + sys.version

		currentTime = time()
		print "Time: " + str(currentTime)
		if currentTime < float(expiry):
			print "Token has " , str(float(expiry) - currentTime) , " seconds remaining."
		else:
			print "Token expired"

		print "before if"
		print "currentTimetype",type(currentTime),type(expiry)

		print "self.hmac(parts) : " + base64.b64encode(self.hmac(parts))
		print "password: " + password
		print "len(password): " , len(password)

		padded_pw = self.add_padding_to_password(password)

		print "padded_pw: " + padded_pw

		if self.hmac(parts) == base64.b64decode(padded_pw) and currentTime < float(expiry):
			print "in here!"
			try:
				print "before user"
				user = User.objects.get(username=realuser)
				print "after user!"
			except User.DoesNotExist:
				# Create a new user. Note that we can set password
				# to anything, because it won't be checked; the password
				# from settings.py will.
				user = User(username=realuser, password='not a password really')
				user.is_staff = True
				user.is_superuser = True
				user.save()
			return user
		print "no user"
		return None

	# user_id can be a username, database ID, must be primary key of the User object
	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None



















