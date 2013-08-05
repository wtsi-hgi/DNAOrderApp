from django import template
from DNAOrderApp.order.models import AffiliatedInstitute

register = template.Library()

# DEPRECATED - NOT IN USE
# def get_affiliated_institute_given_ai_list(ailist):
# 	"""Returns all affiliated institute for fmprojectlist"""
# 	print "this is ailist", ailist
# 	html_string = "<ul>"
# 	for ai in ailist:
# 		html_string += "<li>" + ai.ai_name + "</li>"
# 	html_string+="</ul>"
# 	return html_string


def get_all_affiliated_institute_for_tss4(QuerySet_Affiliated_Institute):
	"""Returns all affiliated institute for tmp-sample-submission-4.html"""
	ai_list = QuerySet_Affiliated_Institute.all()
	html_string = "<ul>"
	for ai in ai_list:
		html_string += "<li>" + ai.ai_name + "</li>"
	html_string+="</ul>"
	print "inside get_all_affiliated_institute with queryset affiliated institute"
	return html_string

def get_all_affiliated_institute(Queryset_Affiliated_Institute):
	"""Returns all affiliated institute for typeahead function in fmprojectlist"""
	ai_list = []
	for c in Queryset_Affiliated_Institute:
		print str(c.ai_name)
		ai_list.append(str(c.ai_name))

	print 'this is a list', ai_list
	return "[\"" + "\",\"".join(ai_list) + "\"]"

def get_affiliated_institute_by_contact(dnaorderappuser):
	"""Returns the affiliated institute associated to the DNAOrderAppUser"""
	return AffiliatedInstitute.objects.filter(dnaorderappuser__username__exact=dnaorderappuser)

# register.filter('get_affiliated_institute_given_ai_list', get_affiliated_institute_given_ai_list)
register.filter('get_all_affiliated_institute_for_tss4', get_all_affiliated_institute_for_tss4)
register.filter('get_all_affiliated_institute', get_all_affiliated_institute)
register.filter('get_affiliated_institute_by_contact', get_affiliated_institute_by_contact)