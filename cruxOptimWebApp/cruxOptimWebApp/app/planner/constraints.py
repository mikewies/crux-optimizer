"""
Goal calculators
"""

from cruxOptimWebApp.app.models import (DailyNutrientIntake,
										PlannerGoal,
										PlannerNutrient)


class MinProtCalculator(object):

	def __call__(self, min_protein, weight):
		return min_protein * weight

class MaxProtCalculator(object):

	def __call__(self, max_protein, weight):
		return max_protein * weight

class MinFatCalculator(object):

	def __call__(self, min_fat, weight):
		return min_fat * weight

class MaxFatCalculator(object):

	def __call__(self, max_fat, weight):
		return max_fat * weight

class MinCarbCalculator(object):

	def __call__(self, min_carb, weight):
		return min_carb * weight

class MaxCarbCalculator(object):

	def __call__(self, max_carb, weight):
		return max_carb * weight


class MinKcalCalculator(object):
	"""
	Calculate the minimum amount of calories required for a given context
	"""

	def __call__(
		self,
		min_protein,
		min_fat,
		min_carb,
		weight,
		*args,
		**kwargs):
		"""
		Calculate the minimum amount of calories required from a given context

		Args:
			context: Context from which to perform the calculation
		
		Returns:
			The maximum target calories required
		"""

		result = sum( (min_protein * 4, min_fat * 9, min_carb * 4) )
		result = result * weight
		return result

class MaxKcalCalculator(object):
	"""
	Calculate the maximum amount of calories required for a given context
	"""

	def __call__(
		self,
		max_protein,
		max_fat,
		max_carb,
		weight,
		*args,
		**kwargs):
		"""
		Calculate the maximum amount of calories required from a given context
		
		Args:
			context: Context from which to perform the calculation

		Returns:
			The maximum target calories required
		"""

		result = sum( (max_protein * 4, max_fat * 9, max_carb * 4) )
		result = result * weight
		return result


class GoalProteinCalculator(object):
	"""
	Calculate the target amount of proteins to ingest for a given context
	"""

	def __call__(self, min_protein, max_protein, weight):
		"""
		Calculate the target amount of proteins to intake for a given context

		Args:
			context: Context that has data from which the target protein intake should be calculated from

		Returns:
			The target amount of protein to ingest
		"""

		result = (min_protein + max_protein) / 2
		result = result * weight
		return result

class GoalFatCalculator(object):

	def __call__(self, min_fat, max_fat, weight):
		"""
		Calculate the target amount of fat to ingest for a given context

		Args:
			context: Context that has data from which the target fat intake should be calculated from

		Returns:
			The target amount of fat to ingest
		"""
		result = (min_fat + max_fat) / 2
		result = result * weight
		return result

class GoalCarbCalculator(object):

	def __call__(self, min_carb, max_carb, weight):
		"""
		Calculate the target amount of carbs to ingest for a given context

		Args:
			context: Context that has data from which the target carbs intake should be calculated from

		Returns:
			The target amount of carbs to ingest
		"""

		result = (min_carb + max_carb) / 2
		result = result * weight
		return result

class GoalKcalCalculator(object):

	def __call__(self,
			min_protein, max_protein,
			min_carb, max_carb,
			min_fat, max_fat,
			weight):
		"""
		Calculate the goal amount of calories to ingest for a given context

		Args:
			context: Context from which to perform the calculation
		"""

		goal_protein = (min_protein + max_protein) / 2 * 4
		goal_fat = (min_fat + max_fat) / 2 * 9
		goal_carb = (min_carb + max_carb) / 2 * 4
		
		result = sum((goal_protein, goal_fat, goal_carb)) * weight
		
		return result

class MinDailyNutrientsAmountCalculator(object):
	"""Calculate the maximum daily amount for each nutrient for a given context"""

	def __init__(self):
		"""Constructor"""
		self.min_prot_fn = MinProtCalculator()
		self.min_fat_fn = MinFatCalculator()
		self.min_carb_fn = MinCarbCalculator()
		self.min_kcal_fn = MinKcalCalculator()
		
		# Get the planner related nutrients
		self.planner_nutrients = PlannerNutrient.objects.all()

	def __call__(
		self, 
		weight,
		min_protein,
		min_fat,
		min_carb,
		goal_nutrients_amount):
		"""Get the minimum amount of nutrients to intake daily
		
		Args:
			context: Dictionary with parameters to consider

		Returns:
			Dictionary with minimum amount of nutrients to consume daily
		"""

		result = {}
				
		# User calculated
		result["prot"] = self.min_prot_fn(
			min_protein=min_protein,
			weight=weight)
		
		result["fat"] = self.min_fat_fn(
			min_fat=min_fat,
			weight=weight)
		
		result["carb"] = self.min_carb_fn(
			min_carb=min_carb,
			weight=weight)
			
		result["kcal"] = self.min_kcal_fn(
			min_protein=min_protein,
			min_fat=min_fat,
			min_carb=min_carb,
			weight=weight)

		# Static amounts
		result["tsat"] = 0.
		result["tdf"] = 20.
		result["tsug"] = 0.
		result["na"] = 1500.
		

		# Derived from goal amounts
		for nutrient_symbol in ("ca", "fe", "mg", "k", "zn", "vitc", "b6", "b12", "trfa", "d-iu", "vitk"):
			result[nutrient_symbol] = goal_nutrients_amount[nutrient_symbol] * 0.75
		result["chol"] = goal_nutrients_amount["chol"] * 0.

		return result

class MaxDailyNutrientsAmountCalculator(object):
	"""Calculate the maximum daily amount for each nutrient for a given context"""

	def __init__(self):
		"""Constructor"""
		self.max_prot_fn = MaxProtCalculator()
		self.max_fat_fn = MaxFatCalculator()
		self.max_carb_fn = MaxCarbCalculator()
		self.max_kcal_fn = MaxKcalCalculator()

		# Get the planner related nutrients
		self.planner_nutrients = PlannerNutrient.objects.all()

	def __call__(
		self, 
		weight,
		max_protein,
		max_fat,
		max_carb,
		goal_nutrients_amount):
		"""Get the maximum amount of nutrients to intake daily
		
		Args:
			context: Dictionary with parameters to consider

		Returns:
			Dictionary with maximum amount of nutrients to consume daily
		"""
		result = {}
				
		# User calculated
		result["prot"] = self.max_prot_fn(
			max_protein=max_protein,
			weight=weight)
		
		result["fat"] = self.max_fat_fn(
			max_fat=max_fat,
			weight=weight)
		
		result["carb"] = self.max_carb_fn(
			max_carb=max_carb,
			weight=weight)
			
		result["kcal"] = self.max_kcal_fn(
			max_protein=max_protein,
			max_fat=max_fat,
			max_carb=max_carb,
			weight=weight)

		# Static amounts
		for nutrient_symbol in ("tsat", "tdf", "ca", "fe", "mg", "k", "zn", "vitc", "b6", "b12", "d-iu", "vitk", "trfa"):
			result[nutrient_symbol] = 9999.

		result["tsug"] = 150.
		result["na"] = 2300.

		# Derived from goal amounts
		result["chol"] = goal_nutrients_amount["chol"] * 1.25

		return result

class GoalDailyNutrientsAmountCalculator(object):

	def __init__(self):
		"""Constructor"""
		self.goal_protein_fn = GoalProteinCalculator()
		self.goal_fat_fn = GoalFatCalculator()
		self.goal_carb_fn = GoalCarbCalculator()
		self.goal_kcal_fn = GoalKcalCalculator()

		# Get the planner relate
		self.planner_nutrients = PlannerNutrient.objects.all()


	def __call__(
		self, 
		weight,
		min_protein, max_protein,
		min_fat, max_fat,
		min_carb, max_carb,
		daily_nutrient_intake,
		age):
		"""Get the goal amount of nutrients to intake daily
		
		Args:
			context: Dictionary with parameters to consider

		Returns:
			Dictionary with the goal amount of nutrients to consume daily
		"""

		result = {}
				
		# User calculated
		result["prot"] = self.goal_protein_fn(
			min_protein=min_protein,
			max_protein=max_protein,
			weight=weight)
		
		result["fat"] = self.goal_fat_fn(
			min_fat=min_fat,
			max_fat=max_fat,
			weight=weight)
		
		result["carb"] = self.goal_carb_fn(
			min_carb=min_carb,
			max_carb=max_carb,
			weight=weight)
			
		result["kcal"] = self.goal_kcal_fn(
			min_protein=min_protein, max_protein=max_protein,
			min_fat=min_fat, max_fat=max_fat,
			min_carb=min_carb, max_carb=max_carb,
			weight=weight)


		# Derived nutrient amounts
		result["tsat"] = result["fat"] * 0.25

		# Static nutrient amounts
		result["tdf"] = 25.0
		result["tsug"] = 0.0
		result["na"] = 1700.0
		result["trfa"] = 1.0

		# print('Planner nutrients {}'.format(len(self.planner_nutrients)))

		# Fill in the nutrients amounts left unfilled from the daily intake chart
		for nutrient_id, nutrient_amount in daily_nutrient_intake.items():
			if nutrient_id in result:
				# print('Nutrient {} already calculated'.format(nutrient_symbol))
				continue
			result[nutrient_id] = nutrient_amount

		return result


