import numpy as np
import pulp
from pulp.solvers import GUROBI # Not available
from pulp.solvers import GLPK
from pulp.solvers import LpSolver # Not implemented
from pulp.solvers import XPRESS

import math

import sys

import test_data

# create the LP object, set up as a minimization problem
solver = None  #GLPK()
display_results = True
use_demerits = False
write_problem_definition = True
prob = pulp.LpProblem('FoodNutritionOptimization', pulp.LpMinimize)

# create the decision variables

# Model nutrients_constraints

# Objective function
# objective_function = pulp.lpSum([kcal_ingestion, prot_ingestion, fat_ingestion])

# nutrients_constraints
variables = {}

"""
Create variables
"""

food_items = test_data.import_food_items_csv_as_dict('./data/food_items.csv')
intake_chart = test_data.import_daily_intake_chart_csv_as_dict('./data/daily_intake_chart.csv')
food_items_nutrients_constraints = test_data.import_food_items_constraints_csv_as_dict('./data/food_items_constraints.csv')

# 1x variable per food item qty
food_variables = {}
for food in food_items:
	variable_name = food["name"]
	min_qty = 0
	max_qty = food_items_nutrients_constraints[food['nbd_no']]['max_qty']
	food_variables[variable_name] = pulp.LpVariable(variable_name, lowBound=min_qty, upBound=max_qty * 1.0)

demerits_variables = {}
if use_demerits:
	# 1x variable per demerit of nutrient_id type
	for i in range(0, len(test_data.goal_nutrients)):
		nutrient_id = test_data.goal_nutrients[i]
		variable_name = '_'.join([nutrient_id, 'demerit'])
		demerits_variables[variable_name] = pulp.LpVariable(variable_name)


# nutrients_constraints modeling
nutrients_amounts = {}
nutrients_constraints = {}
nutrients_variations = {}
for goal_nutrient_idx in range(0, len(test_data.goal_nutrients)):
	nutrient_id = test_data.goal_nutrients[goal_nutrient_idx]

	nutrient_nutrients_constraints = []

	for food_item in food_items:
		food_variable_name = food_item["name"]
		food_nutrients = food_item["nutrients"]

		# Map goal nutrient_id to food nutrient_id index
		nutrient_nutrients_constraints += [food_nutrients[nutrient_id]['value'] * food_variables[food_variable_name] / 100.]

	nutrients_amounts[nutrient_id] = pulp.lpSum(nutrient_nutrients_constraints)

	nutrients_variations[nutrient_id] = (nutrients_amounts[nutrient_id] - test_data.goal_amount[goal_nutrient_idx]) / test_data.goal_amount[goal_nutrient_idx]
	# nutrients_variations[nutrient_id] = (nutrients_amounts[nutrient_id] * test_data.goal_amount[goal_nutrient_idx] - (test_data.goal_amount[goal_nutrient_idx]**2))

	nutrients_constraints[nutrient_id] = {}
	nutrients_constraints[nutrient_id]['max'] = pulp.LpConstraint(e=nutrients_amounts[nutrient_id],
								  					sense=pulp.LpConstraintLE,
							 	 					rhs= test_data.max_amount[goal_nutrient_idx],
							 	 					name= '_'.join([nutrient_id, "max"]))
	
	nutrients_constraints[nutrient_id]['min'] = pulp.LpConstraint(e=nutrients_amounts[nutrient_id],
								 					 sense=pulp.LpConstraintGE,
								   					 rhs= test_data.min_amount[goal_nutrient_idx],
								 					 name='_'.join([nutrient_id, "min"]))
	
	# Demerits constrain => use max(of deviation)
	if use_demerits:
		nutrient_demerits_variable = demerits_variables['_'.join([nutrient_id, 'demerit'])]

		
		nutrients_constraints[nutrient_id]['dev'] = pulp.LpConstraint(e= nutrient_demerits_variable - (nutrients_variations[nutrient_id] * test_data.weight_overconsumption[goal_nutrient_idx]),
									   						sense=pulp.LpConstraintGE,
									   						rhs= 0.,
									   						name='_'.join([nutrient_id, "dev"]))
						   							
		nutrients_constraints[nutrient_id]['dev_ve'] = pulp.LpConstraint(e= nutrient_demerits_variable - (-nutrients_variations[nutrient_id] * test_data.weight_underconsumption[goal_nutrient_idx]),
										  						  sense=pulp.LpConstraintGE,
										  						  rhs= 0.,
										  						  name='_'.join([nutrient_id, "dev_ve"]))
		
	
	# print('NutrientIdx Goal amount', (goal_nutrient_idx, nutrient_id, test_data.goal_amount[goal_nutrient_idx]))
	for constraint in nutrients_constraints[nutrient_id].values():
		prob += constraint


# Objective function
# objective_function = pulp.lpSum( test_data.demerits[i] * nutrients_amounts[test_data.nutrients[i]] for i in range(0, len(test_data.demerits)))
if use_demerits:
	objective_function = pulp.lpSum( [ demerits_variables['_'.join([test_data.goal_nutrients[i], 'demerit'])] for i in range(0, len(test_data.goal_nutrients)) ])
else:
	objective_function = pulp.lpSum( [ nutrients_amounts[nutrient_id] for nutrient_id in test_data.nutrients ] )
	

prob.setObjective(objective_function)

problem_definition_filepath = '_'.join(['output/FoodNutritionLP', 
										'with' if use_demerits else 'without',
										'demerits'])
prob.writeLP(problem_definition_filepath)

# solve the LP using the default solver
optimization_result = prob.solve(solver=solver)


# display the results
if display_results:
	print('Optimal amount of food (grams) to ingest')
	for var in food_variables.values():
		food_qty = math.floor(var.value())
		if food_qty == 0.:
			continue
		print('{} = {} ({})g'.format(var.name, var.value(), food_qty))

	if use_demerits:
		print('')
		print('Demerits for each nutrient')
		for var in demerits_variables.values():
			print('{} = {}'.format(var.name, var.value()))


# make sure we got an optimal solution
assert optimization_result == pulp.LpStatusOptimal

print('\nNutrients amount')
for nutrient, nutrient_amount in nutrients_amounts.items():
	print(nutrient, nutrient_amount.value())

print('\nNutrients variations')
for nutrient, nutrient_variation in nutrients_variations.items():
	print(nutrient, nutrient_variation.value())

print('Optimization result={}'.format(optimization_result))
print ('Objective value={}'.format(prob.objective.value()))

# make sure we got an optimal solution