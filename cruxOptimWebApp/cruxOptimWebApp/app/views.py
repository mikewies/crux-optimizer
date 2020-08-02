from django.shortcuts import render

from django.utils.safestring import mark_safe
from .forms import NutritionOptimizerInputForm
from .models import (PlannerGoal,
                     IntakeProfileScope,
                     PlannerNutrient,
                     Nutrient,
                     NutrientConstraint,
                     NutrientAmount,
                     FoodConstraint,
                     DailyNutrientIntake)

from django.utils.translation import ugettext_lazy as _

from .planner.planner import Planner
from .planner.constraints import (GoalDailyNutrientsAmountCalculator,
                                  MinDailyNutrientsAmountCalculator,
                                  MaxDailyNutrientsAmountCalculator)


from operator import itemgetter, attrgetter

import math

import logging

# Get module logger instance
logger = logging.getLogger(__name__)

def nutrition_calculator(request):
    """Calculate nutrition recipe based on user inputs

    Args:
        request: HTTP Request
    """

    GENDER_CHOICES = [
        (its.id, _(its.name)) for its in IntakeProfileScope.objects.all()
    ]
    WEIGHT_UNITS_CHOICES = [
        ("lbs","lbs")
    ]
    HEIGHT_UNITS_CHOICES = [
        ("inches","Inches")
    ]
    planner_goals = [planner_goal for planner_goal in PlannerGoal.objects.all()]
    GOALS_CHOICES = [
        (goal.id, _(goal.name)) for goal in planner_goals
    ]

    AGE_CHOICES = [
        ("years", "years")
    ]

    USE_DEMERITS = True

    context = {}
    errMsg = None
    form_params = {
        "goals_choices": GOALS_CHOICES,
        "height_units_choices": HEIGHT_UNITS_CHOICES,
        "weight_units_choices": WEIGHT_UNITS_CHOICES,
        "gender_choices": GENDER_CHOICES,
        "age_units_choices": AGE_CHOICES,
        "use_demerits": USE_DEMERITS,
    }
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form_params["data"] = request.POST
        form = NutritionOptimizerInputForm(**form_params)
        # check whether it"s valid:
        if form.is_valid():
            form_data = form.cleaned_data

            # TODO Make weight/height value conversions from units to planner units
            # Build planner inputs from user submitted form data
            inputs = {
                "weight": float(form_data["weight_value"]),
                "height": float(form_data["height_value"]),
                "age": int(form_data["age"]),
                "goal_id": int(form_data["goal"]),
                "scope_id": int(form_data["gender"]),
                "use_demerits": form_data["use_demerits"],
            }

            print('User Inputs {}'.format(inputs))

            logger.debug("User Inputs = {}".format(inputs))

            # Get the relevant nutrients
            planner_nutrients = list(PlannerNutrient.objects.all())
            # print("planner_nutrients", planner_nutrients)
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
                errMsg = "\nMissing nutrients"
                for food_id, missing_nutrients in missing_food_nutrients.items():
                    errMsg += "\nFood item id={} name={} is missing nutrients [{}]".format(
                        food_id,
                        food_items[food_id]["name"],
                        ",".join(missing_nutrients))
                raise Exception(errMsg)

            # Get the daily nutrient intake for the relevant nutrients
            daily_nutrient_intake = dict([ (nutrient_intake.nutrient.symbol.lower().strip(), float(nutrient_intake.value)) \
                                            for nutrient_intake in DailyNutrientIntake.objects.filter(
                                                intake_profile__scope__id=inputs["scope_id"],
                                                intake_profile__age=inputs["age"],
                                                nutrient__id__in=nutrients_ids) ])

            # Get the planner goal object that maps to the user choice
            planner_goal = next(filter(lambda goal: goal.id == inputs["goal_id"], planner_goals), None)
            if not planner_goal:
                raise Exception("Planner goal object not found for id={}".format(inputs["goal_id"]))

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
            nutrients = dict(
                (nutrient_symbol, 
                {
                    "symbol": nutrient_symbol,
                    "constraints": {
                        "min": min_nutrients_amount[nutrient_symbol],
                        "max": max_nutrients_amount[nutrient_symbol],
                        "goal": goal_nutrients_amount[nutrient_symbol]
                    }
                })  \
             for nutrient_symbol in nutrients_symbols)

            # Load nutrient constraints from the database
            for nutrient_constraint in NutrientConstraint.objects.filter(nutrient_id__in=nutrients_ids):
                nutrient_symbol = nutrient_constraint.nutrient.symbol.lower().strip()
                nutrients[nutrient_symbol]["weights"] = {
                    "overconsumption": float(nutrient_constraint.weight_overconsumption),
                    "underconsumption": float(nutrient_constraint.weight_underconsumption)
            }

            # Instantiate the planner
            planner = Planner(use_demerits=form_data["use_demerits"])
            result = result = planner(
                nutrients=nutrients,
                food_items=food_items,
                age=inputs["age"],
                weight=inputs["weight"],
                height=inputs["height"],
                daily_nutrient_intake=daily_nutrient_intake
            )

            prob = result["prob"]

            # Store problem definition as string
            problem_definition = str(prob)
            problem_definition = problem_definition.replace("MINIMIZE", "<h4>Minimize</h4>")
            problem_definition = problem_definition.replace("SUBJECT TO", "<h4>SUBJECT TO</h4>")
            problem_definition = problem_definition.replace("\n", "<br/>")

            # Save problem definition
            problem_definition_filepath = '_'.join(['/tmp/FoodNutritionLP', 
                                            'with' if USE_DEMERITS else 'without',
                                            'demerits'])
            prob.writeLP(problem_definition_filepath)

            # Solve problem
            optimization_result = prob.solve()

            # Build context for rendering
            context = {
                "inputs": inputs,
                "problem_definition": mark_safe(problem_definition)
            }

            food_items_variables = result["variables"][Planner.FOOD_QTY_VARIABLES_CATEGORY]
            # Build food items context
            food_items_data = [
                {
                    "id": food_id,
                    "name": food_item["name"],
                    "minQty": food_item["constraints"]["min_qty"],
                    "maxQty": food_item["constraints"]["max_qty"],
                    "qty": food_items_variables[food_id].value() if food_id in food_items_variables else None
                }
                for food_id, food_item in food_items.items()
                if food_id in food_items_variables and math.floor(food_items_variables[food_id].value()) != 0.0
            ]
            food_items_data = sorted(food_items_data, key=lambda food_item: food_item["name"].lower())
            
            # Build nutrient amounts context
            nutrient_demerits_variables = result["variables"][Planner.NUTRIENT_DEMERIT_VARIABLES_CATEGORY] \
                                        if Planner.NUTRIENT_DEMERIT_VARIABLES_CATEGORY in result["variables"] \
                                        else None
            nutrients_quantities = result["expressions"][Planner.NUTRIENTS_QTY_EXPRESSIONS_CATEGORY]
            nutrients_variations = result["expressions"][Planner.NUTRIENTS_VARIATION_EXPRESSIONS_CATEGORY]
            nutrients_data = [
                {
                    "symbol": nutrient_symbol,
                    "min": nutrient_metadata["constraints"]["min"],
                    "max": nutrient_metadata["constraints"]["max"],
                    "goal": nutrient_metadata["constraints"]["goal"],
                    "weightOver": nutrient_metadata["weights"]["overconsumption"],
                    "weightUnder": nutrient_metadata["weights"]["underconsumption"],
                    "qty": nutrients_quantities[nutrient_symbol].value() if nutrient_symbol in nutrients_quantities else None,
                    "variation": nutrients_variations[nutrient_symbol].value() if nutrient_symbol in nutrients_variations else None,
                    "demerit": nutrient_demerits_variables[nutrient_symbol].value() if nutrient_demerits_variables and nutrient_symbol in nutrient_demerits_variables else None,
                } \
                for nutrient_symbol, nutrient_metadata in nutrients.items()
            ]
            nutrients_data = sorted(nutrients_data, key=lambda nutrient: nutrient["symbol"].lower())

            context["result"] = {
                "objective_value": prob.objective.value(),
                "food_items": food_items_data,
                "nutrients": nutrients_data,
            }

            return render(request, "templates/app/nutrition_calculator_result.html", context)
        else:
            errMsg = "Form is invalid"
            logging.error(errMsg)

    # if a GET (or any other method) we"ll create a blank form
    form = NutritionOptimizerInputForm(**form_params)
    form.fields["goal"].initial = GOALS_CHOICES[3][0]

    context["form"] = form
    if errMsg:
        context["msg"] = errMsg

    return render(request, "templates/app/nutrition_calculator.html", context)