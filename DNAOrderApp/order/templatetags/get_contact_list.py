from django import template
from DNAOrderApp.order.models import DNAOrderAppUser, SampleSubmission

register = template.Library()

def access(ss_contacts_dict, ssid):
	print  "this is ss_contact_dict", ss_contacts_dict, SampleSubmission.objects.get(pk=ssid)

	html_str = "<ul>"
	for contact in ss_contacts_dict[SampleSubmission.objects.get(pk=ssid)]:
		html_str = html_str + "<li>" + contact + "</li>"
	html_str += "</ul>"
	return html_str

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

register.filter('access', access)
register.filter('get_all_contacts', get_all_contacts)
register.filter('get_contacts_by_affiliated_institute', get_contacts_by_affiliated_institute)