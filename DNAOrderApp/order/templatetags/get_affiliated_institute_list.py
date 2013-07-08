from django import template
from DNAOrderApp.order.models import AffiliatedInstitute

register = template.Library()

def get_all_affiliated_institute(Queryset_Affiliated_Institute):
	"""Returns all affiliated institute"""
	ai_list = []
	for c in Queryset_Affiliated_Institute:
		print str(c.ai_name)
		ai_list.append(str(c.ai_name))

	print 'this is a list', ai_list
	return "[\"" + "\",\"".join(ai_list) + "\"]"

def get_affiliated_institute_by_contact(dnaorderappuser):
	"""Returns the affiliated institute associated to the DNAOrderAppUser"""
	return AffiliatedInstitute.objects.filter(dnaorderappuser__username__exact=dnaorderappuser)

register.filter('get_all_affiliated_institute', get_all_affiliated_institute)
register.filter('get_affiliated_institute_by_contact', get_affiliated_institute_by_contact)