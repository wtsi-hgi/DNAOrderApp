from django import template
from django.template.defaultfilters import stringfilter
import re

# To be a valid tag library, module must contain a module-level variable named register
# in which all the tags and filters are registered.
register = template.Library()

# Taking in a variable and replacing it with the argument
@stringfilter #only expects a string as first argument; converts an object to its string value 
def replace(value):
	"""Taking in a string value and replacing any non-words with underscores, i.e. spaces, ;:/?:@=&"""
	return re.sub(r'[^\w]', '_', value)

# register filter definition with the Library instance, to make it available to Django's template language
register.filter('replace', replace) 

