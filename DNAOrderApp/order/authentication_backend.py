''' CUSTOMIZED AUTHENTICATION BACKEND '''
import hmac
import base64
from time import time
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
import django.contrib.auth

from django.db import IntegrityError
from DNAOrderApp.order.exception import InvalidTokenError

class AuthenticationBackend(ModelBackend):
	
	def __init__(self,):
		self.sekret = "F1eFi2G2+UlIrv1uhY7jsOGsen3JA6NZregtaGPf8wE="

	def hmac(self, token):
		print "token: " + token
		print "sekret: " + self.sekret
		# sekret = "F1eFi2G2+UlIrv1uhY7jsOGsen3JA6NZregtaGPf8wE="
		# print "sekret: " + sekret
		hmaccer = hmac.new(base64.b64decode(self.sekret))
		# hmaccer = hmac.new(base64.b64decode(sekret))
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
		import sys
		print "sys.version: " + sys.version
		print "Username = " + username
		print "Passwrod = " + str(type(password))
		parts = base64.b64decode(username)
		print "parts: " + parts

		# CHECK THAT PARTS IS A VALID TOKEN
		# I NEED TO ALSO TRY AND CATCH ValueError Exception when expiry is not a float
		# when you try to cast it to be a float if it contains chars. Or if it is an integer
		try:
			if parts.count(":") != 3:
				raise InvalidTokenError(parts)
			
			expiry = parts.split(':')[1]
			print "expiry: " + expiry
			realuser = parts.split(':')[0]
			print "realuser: " + realuser

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
		except InvalidTokenError as e:
			print "Please check token again. There's not enough colons."
		except ValueError:
			print "Expiry date is not a float."
			

	# user_id can be a username, database ID, must be primary key of the User object
	# THIS FUNCTION IS CALLED FROM auth/__init__.py
	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except:
			return None

	# def get_user(self, username):
	# 	try:
	# 		realuser = base64.b64decode(username).split(':')[0]
	# 		user = User.objects.get(email=realuser)
	# 		return user
	# 	except User.DoesNotExist:
	# 		return None





















