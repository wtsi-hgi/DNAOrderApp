#Trying out the tutorial: https://docs.djangoproject.com/en/dev/topics/http/file-uploads/
from django import forms

class DocumentForm(forms.Form):
	docfile = forms.FileField(
		label='Select a manifest (in .csv or .xls format)',
		help_text='max. 42 megabytes'
	)

		