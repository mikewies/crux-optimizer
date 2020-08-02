from django.test import TestCase, SimpleTestCase, TransactionTestCase

from cruxOptimWebApp.app.models import (PlannerGoal,
                                        PlannerNutrient,
                                        Nutrient,
                                        NutrientAmount,
                                        DailyNutrientIntake,
                                        Food,
                                        FoodConstraint,
                                        NutrientConstraint)

from cruxOptimWebApp.app.planner.planner import Planner
from cruxOptimWebApp.app.planner.constraints import (GoalDailyNutrientsAmountCalculator,
                                                     MinDailyNutrientsAmountCalculator,
                                                     MaxDailyNutrientsAmountCalculator)
import math

class PlannerTestCase(TestCase):
    
    EXPECTED_MIN_NUTRIENTS_AMOUNT = {
        "kcal": 1998.00,
        "prot": 148.00,
        "fat": 74.,
        "tsat": 0.,
        "carb": 185.00,
        "tdf": 20.00,
        "tsug": 0.00,
        "ca": 750.00,
        "fe": 6.00,
        "mg": 262.5,
        "k": 3525.,
        "na": 1500.,
        "zn": 30.,
        "vitc": 67.50,
        "b6": 1.2750,
        "b12": 1.80,
        "trfa": 0.750,
        "d-iu": 15.00,
        "vitk": 90.00,
        "chol": 0.00
    }

    EXPECTED_MAX_NUTRIENTS_AMOUNT = {
        "kcal": 2997.00,
        "prot": 222.00,
        "fat": 111.00,
        "tsat": 9999.00,
        "carb": 277.5,
        "tdf": 9999.00,
        "tsug": 150.00,
        "ca": 9999.00,
        "fe": 9999.00,
        "mg": 9999.00,
        "k": 9999.00,
        "na": 2300.00,
        "zn": 9999.00,
        "vitc": 9999.00,
        "b6": 9999.00,
        "b12": 9999.00,
        "trfa": 9999.00,
        "d-iu": 9999.00,
        "vitk": 9999.00,
        "chol": 312.50
    }

    EXPECTED_GOAL_NUTRIENTS_AMOUNT = {
        "kcal": 2497.50,
        "prot": 185.00,
        "fat": 92.5,
        "tsat": 23.1250,
        "carb": 231.250,
        "tdf": 25.,
        "tsug": 0.,
        "ca": 1000.,
        "fe": 8.,
        "mg": 350.,
        "k": 4700.,
        "na": 1700.,
        "zn": 40,
        "vitc": 90,
        "b6": 1.70,
        "b12": 2.40,
        "trfa": 1.,
        "d-iu": 20.,
        "vitk": 120.,
        "chol": 250.
    }
    
    INPUTS = {
        "weight": 185,
        "height": 72,
        "scope_id": 1, # Male
        "age": 29,
        "goal_id": 4 # All of the above
    }

    def setUp(self):
        print('Inputs={}'.format(self.INPUTS))
    #   pass

        #Animal.objects.create(name="lion", sound="roar")
        #Animal.objects.create(name="cat", sound="meow")

    def show_dict(self, d):
        for key, value in d.items():
            print(key, value)

    def show_diff(self, d1, d2, diff_keys):
        for k in diff_keys:
            print(k, d1[k], d2[k])

    def diff_dict(self, d1, d2):
        return {k for k in set(d1) & set(d2) if abs(float(d1[k]) - float(d2[k])) >= 0.001}

    def _test_goal_nutrients_calculator(self):
        """Check correct calculation of goal amount of nutrients"""
        print('\nGoal Nutrients Calculator')
        inputs = {}
        inputs.update(self.INPUTS)
        goal_nutrients_amount_fn = GoalDailyNutrientsAmountCalculator()

        output_nutrients_amount = goal_nutrients_amount_fn(**inputs)
        print('output_nutrients_amount size={}'.format(len(output_nutrients_amount)))
        diff = self.diff_dict(self.EXPECTED_GOAL_NUTRIENTS_AMOUNT, output_nutrients_amount)

        if diff:
            print('Goal Nutrient Differences')
            self.show_diff(self.EXPECTED_GOAL_NUTRIENTS_AMOUNT, output_nutrients_amount, diff)

    def _test_min_nutrients_calculator(self):
        """Check correct calculation of minimum amount of nutrients"""
        print('\nMin  Nutrients Calculator')
        goal_nutrients_amount_fn = GoalDailyNutrientsAmountCalculator()
        inputs = {}
        inputs.update(self.INPUTS)
        goal_nutrients_amount = goal_nutrients_amount_fn(**inputs)

        min_nutrients_amount_fn = MinDailyNutrientsAmountCalculator()
        inputs["goal_nutrients_amount"] = goal_nutrients_amount

        output_nutrients_amount = min_nutrients_amount_fn(**inputs)
        print('output_nutrients_amount size={}'.format(len(output_nutrients_amount)))
        diff = self.diff_dict(self.EXPECTED_MIN_NUTRIENTS_AMOUNT, output_nutrients_amount)

        if diff:
            print('Min Nutrient Differences')
            self.show_diff(self.EXPECTED_MIN_NUTRIENTS_AMOUNT, output_nutrients_amount, diff)
        
    def _test_max_nutrients_calculator(self):
        """Check correct calculation of maximum amount of nutrients"""
        print('\nMax  Nutrients Calculator')
        inputs = {}
        inputs.update(self.INPUTS)
        goal_nutrients_amount_fn = GoalDailyNutrientsAmountCalculator()
        goal_nutrients_amount = goal_nutrients_amount_fn(**inputs)

        max_nutrients_amount_fn = MaxDailyNutrientsAmountCalculator()
        inputs["goal_nutrients_amount"] = goal_nutrients_amount
        
        output_nutrients_amount = max_nutrients_amount_fn(**inputs)
        print('output_nutrients_amount size={}'.format(len(output_nutrients_amount)))
        diff = self.diff_dict(self.EXPECTED_MAX_NUTRIENTS_AMOUNT, output_nutrients_amount)

        if diff:
            print('Max Nutrient Differences')
            self.show_diff(self.EXPECTED_MAX_NUTRIENTS_AMOUNT, output_nutrients_amount, diff)
        
    def test_planner(self):
        FLOAT_FORMAT = '{:.2f}'
        use_demerits = True
        display_results = True

        inputs = {}
        inputs.update(self.INPUTS)

        # Get the relevant nutrients
        planner_nutrients = list(PlannerNutrient.objects.all())
        # print('planner_nutrients', planner_nutrients)
        nutrients_ids = [planner_nutrient.nutrient_id \
                         for planner_nutrient in planner_nutrients]
        nutrients_symbols = [nutrient.symbol.lower().strip() \
                             for nutrient in Nutrient.objects.filter(id__in=nutrients_ids)]

        # Set the selected food items constraints
        food_items = dict( [ (food_constraint.food_id, { "name": food_constraint.food.description_en,
                                                         "constraints": { 
                                                            "min_qty": float(food_constraint.min_qty),
                                                            "max_qty": float(food_constraint.max_qty) 
                                                         } 
                                                       })  \
                                        for food_constraint in FoodConstraint.objects.all() ])

        # Create a dictionary of food item nutrients
        missing_food_nutrients={}
        for food_id, food_item in food_items.items():
            food_nutrients = list(NutrientAmount.objects.filter(
                food_id=food_id,
                nutrient_id__in=nutrients_ids))

            food_item["nutrients"] = dict( (food_nutrient.nutrient.symbol.lower().strip(), float(food_nutrient.value)) \
                                            for food_nutrient in food_nutrients )
            # Sanity check - Ensure all planner nutrients are contained in the food nutrients
            missing_nutrients = set(nutrients_symbols) - set(food_item["nutrients"].keys())
            if missing_nutrients:
                missing_food_nutrients[food_id] = missing_nutrients

        # Sanity check - Check for missing nutrients used by the planner
        if missing_food_nutrients:
            print('Missing nutrients')
            for food_id, missing_nutrients in missing_food_nutrients.items():
                print('Food item id={} name={} is missing nutrients [{}]'.format(
                    food_id,
                    food_items[food_id]["name"],
                    ','.join(missing_nutrients)))
            sys.exit(0)
       
        # Get the daily nutrient intake for the relevant nutrients
        daily_nutrient_intake = dict([ (nutrient_intake.nutrient.symbol.lower().strip(), float(nutrient_intake.value)) \
                                        for nutrient_intake in DailyNutrientIntake.objects.filter(
                                            intake_profile__scope__id=inputs["scope_id"],
                                            intake_profile__age=inputs["age"],
                                            nutrient__id__in=nutrients_ids) ])

        planner_goal = PlannerGoal.objects.get(id=inputs["goal_id"])
        
        min_protein, max_protein = float(planner_goal.min_protein), float(planner_goal.max_protein)

        min_fat, max_fat = float(planner_goal.min_fat), float(planner_goal.max_fat)

        min_carb, max_carb = float(planner_goal.min_carb), float(planner_goal.max_carb)

        goal_nutrients_amount = GoalDailyNutrientsAmountCalculator()(
                weight=inputs["weight"],
                age=inputs["age"],
                min_protein=min_protein, max_protein=max_protein,
                min_fat=min_fat, max_fat=max_fat,
                min_carb=min_carb, max_carb=max_carb,
                daily_nutrient_intake=daily_nutrient_intake,
        )
        max_nutrients_amount = MaxDailyNutrientsAmountCalculator()(
            weight=inputs["weight"],
            max_protein=max_protein,
            max_fat=max_fat,
            max_carb=max_carb,
            goal_nutrients_amount=goal_nutrients_amount,
        )
        min_nutrients_amount = MinDailyNutrientsAmountCalculator()(
            weight=inputs["weight"],
            min_protein=min_protein,
            min_fat=min_fat,
            min_carb=min_carb,
            goal_nutrients_amount=goal_nutrients_amount,
        )

        # Create nutrients dictionary
        nutrients = dict( (nutrient_symbol, {
                                                "symbol": nutrient_symbol,
                                                "constraints": {
                                                    "min": min_nutrients_amount[nutrient_symbol],
                                                    "max": max_nutrients_amount[nutrient_symbol],
                                                    "goal": goal_nutrients_amount[nutrient_symbol]
                                                }
                                            })  \
                            for nutrient_symbol in nutrients_symbols )

        # Show nutrients constraints
        print("Nutrient constraints")
        for nutrient_symbol, nutrient_data in nutrients.items():
            print(''.join(["{} min=", FLOAT_FORMAT, " max=", FLOAT_FORMAT, " goal=", FLOAT_FORMAT]).format(
                nutrient_symbol,
                nutrient_data["constraints"]["min"],
                nutrient_data["constraints"]["max"],
                nutrient_data["constraints"]["goal"]
            ))
        
        for nutrient_constraint in NutrientConstraint.objects.filter(nutrient_id__in=nutrients_ids):
            nutrient_symbol = nutrient_constraint.nutrient.symbol.lower().strip()
            nutrients[nutrient_symbol]["weights"] = {
                "overconsumption": float(nutrient_constraint.weight_overconsumption),
                "underconsumption": float(nutrient_constraint.weight_underconsumption)
        }

        planner = Planner(use_demerits=use_demerits)
        result = planner(
            nutrients=nutrients,
            food_items=food_items,
            age=inputs["age"],
            weight=inputs["weight"],
            height=inputs["height"],
            daily_nutrient_intake=daily_nutrient_intake
        )

        prob = result["prob"]

        # Save problem definition
        problem_definition_filepath = '_'.join(['/tmp/FoodNutritionLP', 
                                        'with' if use_demerits else 'without',
                                        'demerits'])
        prob.writeLP(problem_definition_filepath)

        # Solve problem
        optimization_result = prob.solve()
        
        # display the results
        if display_results:
            print('Optimization result={}'.format(optimization_result))
            print('Objective value={}'.format(prob.objective.value()))

            print('Optimal amount of food (grams) to ingest')
            for var in prob.variables():
                food_qty = math.floor(var.value())
                if food_qty == 0.:
                    continue
                print('{} = {} ({})g'.format(var.name, var.value(), food_qty))

            
            print('\nNutrients amount')

            for category, expressions in result['expressions'].items():
                print('\nCategory={}'.format(category))
                if category == Planner.NUTRIENTS_QTY_EXPRESSIONS_CATEGORY:
                    for nutrient_symbol, expression in expressions.items():
                        print(' '.join(['{}', '=>', FLOAT_FORMAT, '<=', FLOAT_FORMAT, '<=', FLOAT_FORMAT, '  (', 'goal=', FLOAT_FORMAT, ')']).format(
                            nutrient_symbol,
                            min_nutrients_amount[nutrient_symbol],
                            expression.value(),
                            max_nutrients_amount[nutrient_symbol],
                            goal_nutrients_amount[nutrient_symbol]))
                else:
                    for name, expression in expressions.items():
                        print(''.join(['{}', '=', FLOAT_FORMAT]).format(name, expression.value()))
            
