from django import template
from django.forms import ModelForm
from DNAOrderApp.order.models import AffiliatedInstituteForm

register = template.Library()

def create_aiform(projid):
	"""You call this whenever you want an aiform to be made"""
	aiform = AffiliatedInstituteForm(auto_id=True) 
	aiform = aiform.as_p()
	print "this is aiform", aiform
	return aiform

register.filter('create_aiform', create_aiform)

# prefix=str(projid)
