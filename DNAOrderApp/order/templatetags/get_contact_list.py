from django import template
from DNAOrderApp.order.models import DNAOrderAppUser

register = template.Library()

def get_all_contacts(Queryset_DNAOrderAppUser):
	"""Returns all contacts"""
	dnaorderappuser = []
	for c in Queryset_DNAOrderAppUser:
		print str(c.username)
		dnaorderappuser.append(str(c.username))

	print 'this is a list', dnaorderappuser
	return "[\"" + "\",\"".join(dnaorderappuser) + "\"]"

def get_contacts_by_affiliated_institute(affiliated_institute):
	"""Returns the contacts associated with the Affiliated Institute"""
	return DNAOrderAppUser.objects.filter(affiliatedinstitute__ainame__exact=affiliated_institute)

register.filter('get_all_contacts', get_all_contacts)
register.filter('get_contacts_by_affiliated_institute', get_contacts_by_affiliated_institute)