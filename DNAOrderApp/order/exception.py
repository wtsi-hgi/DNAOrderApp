class InvalidTokenError(Exception):
	"""Exception raised for errors in the inputted token

	Attributes:
		expr -- input expression in which the error occurred
	"""

	def __init__(self, expr):
		self.expr = expr

	def __str__(self):
		return repr(self.expr)
