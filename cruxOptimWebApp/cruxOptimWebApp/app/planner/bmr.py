class BmrCalculator(object):
	"""
	Calculate the Basal Metabolic Rate (BMR) for a given context
	"""

	def __call__(self, context):
		"""
		Calculate the Basal Metabolic Rate (BMR) for a given context

		Args:
			context: Context from which to calculate the BMR

		Returns the BMD for the given context
		"""

		gender = context["gender"]

		# Weight (lbs)
		target_body_weight = context["target_body_weight"]
		# Height (inches)
		height = context["height"]
		# Age (years)
		age = context["age"]

		if gender == "female":
			result = 66.47 + (13.75 * target_body_weight / 2.2) + (5 * height * 2.54) - (6.75 * age)
		else:
			result = 665.09 + (9.56 * target_body_weight / 2.2) + 1.84 * height * 2.54 - 4.67 * age

		return result