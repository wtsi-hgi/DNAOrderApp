from django import template

register = template.Library()

aiformlist=[]

def create_aiform_list(aiform):
	"""You call this once in the beginning to create the list of aiforms"""
	print "inside create aiform list"
	for aiform in aiformset:
		print "THIS IS AN AI FORM", aiform 
		aiformlist.append(aiform)

	print 'this is a list in aiformlist', aiformlist
	return aiformlist

def getaiform(aiformlist):
	"""Returns a list of ai forms"""
	print "this is aiformlist before POP", aiformset
	return aiformlist.pop()
	# return "[\"" + "\",\"".join(dnaorderappuser) + "\"]"


register.filter('create_aiform_list', create_aiform_list)
register.filter('getaiform', getaiform)