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

class InvalidTokenError(Exception):
	"""Exception raised for errors in the inputted token

	Attributes:
		expr -- input expression in which the error occurred
	"""

	def __init__(self, expr):
		self.expr = expr

	def __str__(self):
		return repr(self.expr)
