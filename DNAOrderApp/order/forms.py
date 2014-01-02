# Copyright (c) 2013 Genome Research Ltd.
# 
# Author: Albertina Wong <aw18@sanger.ac.uk>
# 
# This file is part of DNAOrderApp.
# 
# DNAOrderApp is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option) any
# later version.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

#Trying out the tutorial: https://docs.djangoproject.com/en/dev/topics/http/file-uploads/
from django import forms

class DocumentForm(forms.Form):
	docfile = forms.FileField(
		label='Select a manifest (in .csv or .xls format)',
		help_text='max. 42 megabytes'
	)

		
