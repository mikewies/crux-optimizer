-- Choose database
use food_nutrition;

/**
 * CNF data
 */
DROP TABLE IF EXISTS nutrient_amount;
DROP TABLE IF EXISTS conversion_factor;
DROP TABLE IF EXISTS refuse_amount;
DROP TABLE IF EXISTS yield_amount;
DROP TABLE IF EXISTS food;
DROP TABLE IF EXISTS food_group;
DROP TABLE IF EXISTS food_source;
DROP TABLE IF EXISTS nutrient;
DROP TABLE IF EXISTS nutrient_source;
DROP TABLE IF EXISTS measure;
DROP TABLE IF EXISTS refuse_type;
DROP TABLE IF EXISTS yield_type;

/**
 * Custom data (integrated with CNF)
 */
DROP TABLE IF EXISTS intake_profile_scope
DROP TABLE IF EXISTS intake_profile;
DROP TABLE IF EXISTS daily_nutrient_intake;
DROP TABLE IF EXISTS food_constraint;
