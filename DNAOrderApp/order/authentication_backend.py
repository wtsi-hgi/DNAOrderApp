''' CUSTOMIZED AUTHENTICATION BACKEND '''
import hmac
import base64
import time
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

	def authenticate(self, username = None, password = None):
		print "Username = " + username
		print "Passwrod = " + password
		parts = base64.b64decode(username)
		print "parts: " + parts
		expiry = parts.split(':')[1]
		print "expiry: " + expiry
		realuser = parts.split(':')[0]
		print "realuser: " + realuser
		now = time.time()
		if now:
			print "now exists!" + str(now)
		else:
			print "now does not exist"

		print "before if"
		print "nowtype",type(now),type(expiry)

		print "self.hmac(parts) : " + self.hmac(parts)
		print "password: " + password
		if self.hmac(parts) == base64.b64decode(password) and now < float(expiry):
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

	# # Check token and return a User
	# def authenticate(self, token=None):
	# 	pass


	# user_id can be a username, database ID, must be primary key of the User object
	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None