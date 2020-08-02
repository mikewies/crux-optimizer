
from cruxOptimWebApp.app.planner.constraints import (MinDailyNutrientsAmountCalculator,
												     MaxDailyNutrientsAmountCalculator,
												     GoalDailyNutrientsAmountCalculator)

from cruxOptimWebApp.app.models import (PlannerGoal)

import pulp
from pulp.solvers import (GUROBI,   # Not available
						  LpSolver, # Not implemented
						  GLPK,
						  XPRESS)

class Planner(object):
	"""Daily nutrition planner"""

	FOOD_QTY_VARIABLES_CATEGORY = 'food_qty'
	NUTRIENT_DEMERIT_VARIABLES_CATEGORY = 'nutrient_demerit'

	NUTRIENTS_QTY_EXPRESSIONS_CATEGORY = 'nutrients_qty'
	NUTRIENTS_VARIATION_EXPRESSIONS_CATEGORY = 'nutrients_variation'

	def __init__(self, use_demerits = False):
		"""Constructor"""
		self.use_demerits = use_demerits

		self.min_nutrients_amount_fn = MinDailyNutrientsAmountCalculator()
		self.max_nutrients_amount_fn = MaxDailyNutrientsAmountCalculator()
		self.goal_nutrients_amount_fn = GoalDailyNutrientsAmountCalculator()

	def set_inputs(self, inputs):
		self.inputs = inputs


	def _create_variables(
		self,
		food_items,
		nutrients):
		"""Create variables for each food item"""

		# Create food qty variables (1x per food item)
		variables = {
			'food_qty': {}
		}
		for food_id, food_item in food_items.items():
			variable_name = self._build_food_qty_variable_name(food_item)
			variables[self.FOOD_QTY_VARIABLES_CATEGORY][food_id] = pulp.LpVariable(
				variable_name,
				lowBound=food_item["constraints"]["min_qty"],
				upBound=food_item["constraints"]["max_qty"])

		if self.use_demerits:
			variables[self.NUTRIENT_DEMERIT_VARIABLES_CATEGORY] = {}
			# 1x variable per nutrient
			for nutrient_id in nutrients:
				variable_name = self._build_nutrient_demerit_variable_name(nutrient_id)
				variables[self.NUTRIENT_DEMERIT_VARIABLES_CATEGORY][nutrient_id] = pulp.LpVariable(variable_name)

		return variables

	def _build_food_qty_variable_name(self, food_item):
		"""Build the name for a food quantity variable"""
		return '_'.join([food_item["name"], 'qty'])

	def _build_nutrient_demerit_variable_name(self, nutrient):
		"""Build the name for a nutrient demerit variable"""
		return '_'.join([nutrient, 'demerit'])

	def _create_expressions(
		self,
		variables,
		nutrients,
		food_items):
		"""Create a dict of affine expressions relevant to the LP problem

		Args:
			variables: Dictionary with problem variables
			nutrients: Nutrients to use in the problem formulation
			food_items: Food items to use in the problem formulation

		Returns:
			List of constraints to apply to the problem
		"""
		# Pre load all food nutrients into a dictionary
		
		# Iterate all nutrients to create constraints
		expressions = {}
		expressions[self.NUTRIENTS_QTY_EXPRESSIONS_CATEGORY] = {}
		expressions[self.NUTRIENTS_VARIATION_EXPRESSIONS_CATEGORY] = {}

		for nutrient_id, nutrient_data in nutrients.items():

			food_nutrients_parts = []
			for food_id, food_item in food_items.items():
				food_nutrients = food_item["nutrients"]

				# Map goal nutrient_id to food nutrient_id index
				food_nutrients_parts += [float(food_nutrients[nutrient_id]) * variables['food_qty'][food_id] / float(100.)]

			# Total nutrients amount
			total_nutrient_amount = pulp.lpSum(food_nutrients_parts)
			expressions[self.NUTRIENTS_QTY_EXPRESSIONS_CATEGORY][nutrient_id] = total_nutrient_amount

			# Demerits constraint => use max(of deviation)
			# Nutrient variation
			expressions[self.NUTRIENTS_VARIATION_EXPRESSIONS_CATEGORY][nutrient_id] = (total_nutrient_amount - nutrient_data["constraints"]["goal"]) / nutrient_data["constraints"]["goal"] \
																						if nutrient_data["constraints"]["goal"] != 0.0 \
																						else total_nutrient_amount / 100.0
			# expressions[self.NUTRIENTS_VARIATION_EXPRESSIONS_CATEGORY][nutrient_id] = total_nutrient_amount * nutrient_data["constraints"]["goal"] - nutrient_data["constraints"]["goal"]**2

		return expressions

	def _create_constraints(
		self,
		variables,
		nutrients,
		food_items,
		expressions):
		"""Create LP problem constraints

		Args:
			variables: Dictionary with problem variables
			nutrients: Nutrients to use in the problem formulation
			food_items: Food items to use in the problem formulation

		Returns:
			List of constraints to apply to the problem
		"""
		constraints = []

		# Iterate all nutrients to create constraints
		for nutrient_id, nutrient_data in nutrients.items():

			max_nutrient_amount_constraint = pulp.LpConstraint(
				e=expressions[self.NUTRIENTS_QTY_EXPRESSIONS_CATEGORY][nutrient_id],
				sense=pulp.LpConstraintLE,
				rhs=nutrient_data["constraints"]["max"],
				name= '_'.join([nutrient_id, "max"]))
			constraints.append(max_nutrient_amount_constraint)

			min_nutrient_amount_constraint = pulp.LpConstraint(
				e=expressions[self.NUTRIENTS_QTY_EXPRESSIONS_CATEGORY][nutrient_id],
				sense=pulp.LpConstraintGE,
				rhs=nutrient_data["constraints"]["min"],
				name='_'.join([nutrient_id, "min"]))
			constraints.append(min_nutrient_amount_constraint)

			# Demerits constrain => use max(of deviation)
			if self.use_demerits:
				# Nutrient variation
				nutrient_demerits_variable = variables['nutrient_demerit'][nutrient_id]
				
				nutrient_deviation_constraint = pulp.LpConstraint(
					e=nutrient_demerits_variable - (expressions[self.NUTRIENTS_VARIATION_EXPRESSIONS_CATEGORY][nutrient_id] * nutrient_data["weights"]["overconsumption"]),
					sense=pulp.LpConstraintGE,
					rhs= 0.,
					name='_'.join([nutrient_id, "dev"]))
				constraints.append(nutrient_deviation_constraint)
								   							
				nutrient_deviation_ve_constraint = pulp.LpConstraint(
					e=nutrient_demerits_variable - (-expressions[self.NUTRIENTS_VARIATION_EXPRESSIONS_CATEGORY][nutrient_id] * nutrient_data["weights"]["overconsumption"]),
					sense=pulp.LpConstraintGE,
					rhs= 0.,
					name='_'.join([nutrient_id, "dev_ve"]))
				constraints.append(nutrient_deviation_ve_constraint)

		return constraints
		

	def _create_objective_function(
		self,
		variables,
		nutrients,
		expressions):
		"""Create LP Problem objective function"""
		
		if self.use_demerits:
			return pulp.lpSum( [ variables[self.NUTRIENT_DEMERIT_VARIABLES_CATEGORY][nutrient_id] \
								 for nutrient_id in nutrients])
		
		return pulp.lpSum( [ total_nutrient_amount \
							 for total_nutrient_amount in expressions[self.NUTRIENTS_QTY_EXPRESSIONS_CATEGORY].values() ] )
			
	def __call__(
		self,
		food_items,
		nutrients,
		age,
		weight,
		height,
		daily_nutrient_intake):
		"""Formulate the LP Problem"""

		prob = pulp.LpProblem('FoodNutritionOptimization', pulp.LpMinimize)

		# Create variables
		variables = self._create_variables(
			food_items=food_items,
			nutrients=nutrients)

		expressions = self._create_expressions(
			variables=variables,
			food_items=food_items,
			nutrients=nutrients)

		# Add problem constraints
		constraints = self._create_constraints(
			variables=variables,
			nutrients=nutrients,
			food_items=food_items,
			expressions=expressions)
		for constraint in constraints:
			prob += constraint

		objective_function = self._create_objective_function(
			variables=variables,
			nutrients=nutrients,
			expressions=expressions)
		
		prob.setObjective(objective_function)

		return {
			"prob": prob,
			"expressions": expressions,
			"variables": variables
		}


