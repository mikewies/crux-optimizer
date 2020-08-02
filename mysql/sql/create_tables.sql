-- Choose database
use food_nutrition;

/*
This file is a support or "list" table that is used to link to the FOOD NAME table. It
contains a list of 23 different group headings (in English and French) based on similar
characteristics of the foods.
*/
CREATE TABLE IF NOT EXISTS food_group (
	id TINYINT UNSIGNED,
	code TINYINT UNSIGNED,
	name_en VARCHAR(200),
	name_fr VARCHAR(200) NULL,
	CONSTRAINT PK_food_group PRIMARY KEY (id)
);

/*
This file is a support or "list" table that is used to link to the FOOD NAME table. It
contains a list of several food sources (in English and French) that foods can be
grouped on.
*/
CREATE TABLE IF NOT EXISTS food_source (
	id TINYINT UNSIGNED,
	code TINYINT UNSIGNED,
	description_en VARCHAR(200),
	description_fr VARCHAR(200),
	CONSTRAINT PK_food_source PRIMARY KEY (id)
);

/*
This file is a support or "list" table that contains the list of nutrients (in English and
French) used in the NT_AMT file, with which it is linked.
*/
CREATE TABLE IF NOT EXISTS nutrient (
	id SMALLINT UNSIGNED,
	code SMALLINT UNSIGNED,
	symbol VARCHAR(10),
	unit VARCHAR(8),
	name_en VARCHAR(200),
	name_fr VARCHAR(200) NULL,
	tagname VARCHAR(20),
	num_decimals TINYINT UNSIGNED,
	CONSTRAINT PK_nutrient PRIMARY KEY (id)
);

/*
This file is a support or "list" table that is used to link to the NUTRIENT AMOUNT file.
It contains a list of several sources and/or types of nutrient data (in English and
French).
*/
CREATE TABLE IF NOT EXISTS nutrient_source (
	id TINYINT UNSIGNED,
	code TINYINT UNSIGNED,
	description_en VARCHAR(200),
	description_fr VARCHAR(200),
	CONSTRAINT PK_nutrient_source PRIMARY KEY (id)
);

/*
This file is a support or "list" table that is used to link to the CONV FAC table. It
contains a list of measures (in English and French).
*/
CREATE TABLE IF NOT EXISTS measure (
	id MEDIUMINT UNSIGNED,
	description_en VARCHAR(200),
	description_fr VARCHAR(200) NULL,
	CONSTRAINT PK_measure PRIMARY KEY (id)
);

/*
This file is a support or "list" table that is used to link to the REFUSE table. It contains
a list of refuse types.
*/
CREATE TABLE IF NOT EXISTS refuse_type (
	id MEDIUMINT UNSIGNED,
	description_en VARCHAR(200),
	description_fr VARCHAR(200) NULL,
	CONSTRAINT PK_refuse_type PRIMARY KEY (id)
);

/*
This file is a support or "list" table that is used to link to the YIELD table. It contains a
list of yield types or yield descriptions (in English and French).
*/
CREATE TABLE IF NOT EXISTS yield_type (
	id MEDIUMINT UNSIGNED,
	description_en VARCHAR(200),
	description_fr VARCHAR(200) NULL,
	CONSTRAINT PK_yield_type PRIMARY KEY (id)
);
/*
This is the principle file.
It stores information about each food in the database.
It contains a description_en of each food in English and French as well as dates and
comments
*/
CREATE TABLE IF NOT EXISTS food (
	id MEDIUMINT UNSIGNED,
	code SMALLINT UNSIGNED,
	group_id TINYINT UNSIGNED,
	source_id TINYINT UNSIGNED,
	description_en VARCHAR(255),
	description_fr VARCHAR(255),
	entry_date DATE NULL,
	publication_date DATE NULL,
	country_code MEDIUMINT UNSIGNED NULL,
	scientific_name VARCHAR(100),
	CONSTRAINT PK_food PRIMARY KEY (id)
);
/* 	CONSTRAINT FK_food_group FOREIGN KEY (group_id) REFERENCES food_group(id) */
/*	CONSTRAINT FK_food_source FOREIGN KEY (source_id) REFERENCES food_source(id)*/


/*
This is the main file.
It uses information (by linking) from the "food" table (among others) to identify which nutrients and amounts are recorded for that food.
*/
CREATE TABLE IF NOT EXISTS nutrient_amount (
	id MEDIUMINT UNSIGNED AUTO_INCREMENT,
	food_id MEDIUMINT UNSIGNED,
	nutrient_id SMALLINT UNSIGNED,
	value DECIMAL(12,5),
	standard_error DECIMAL(8,4),
	num_observations SMALLINT UNSIGNED,
	nutrient_source_id TINYINT UNSIGNED,
	entry_date DATE NULL,
	CONSTRAINT PK_nutrient_amount PRIMARY KEY (id),
	CONSTRAINT FK_nutrient_amount_food FOREIGN KEY(food_id) REFERENCES food(id),
	CONSTRAINT UN_nutrient_amount_food_nutrient UNIQUE INDEX(food_id, nutrient_id)
);
/* 	CONSTRAINT PK_nutrient_amount PRIMARY KEY (food_id, nutrient_id), */
/* 	CONSTRAINT FK_nutrient_amount_nurient FOREIGN KEY(nutrient_id) REFERENCES nutrient(id) */

/*
This is a principal file. This file contains portion size conversion factors. The
conversion factors are food specific multipliers by which the nutrient values for each
food may be multiplied to give the nutrients in described portions.
*/
CREATE TABLE IF NOT EXISTS conversion_factor (
	id MEDIUMINT UNSIGNED AUTO_INCREMENT,
	food_id MEDIUMINT UNSIGNED,
	measure_id MEDIUMINT UNSIGNED,
	value DECIMAL(10,5),
	entry_date DATE NULL,
	CONSTRAINT PK_conversion_factor PRIMARY KEY (id),
	CONSTRAINT FK_conversion_factor_food FOREIGN KEY(food_id) REFERENCES food(id),
	CONSTRAINT UN_conversion_factor_food_measure UNIQUE INDEX(food_id, measure_id)
);
/* 	CONSTRAINT PK_conversion_factor PRIMARY KEY (food_id, measure_id),*/
/* CONSTRAINT FK_conversion_factor_measure FOREIGN KEY(measure_id) REFERENCES measure(id) */

/*
This is a principal file.
This file contains the percent of refuse, or inedible portion, for each food.
*/
CREATE TABLE IF NOT EXISTS refuse_amount (
	id MEDIUMINT UNSIGNED AUTO_INCREMENT,
	food_id MEDIUMINT UNSIGNED,
	refuse_type_id MEDIUMINT UNSIGNED,
	amount DECIMAL,
	entry_date DATE NULL,
	CONSTRAINT PK_refuse_amount PRIMARY KEY (id),
	CONSTRAINT FK_refuse_amount_food FOREIGN KEY(food_id) REFERENCES food(id),
	CONSTRAINT FK_refuse_amount_refuse FOREIGN KEY(refuse_type_id) REFERENCES refuse_type(id),
	CONSTRAINT UN_refuse_amount_food_refuse UNIQUE INDEX(food_id, refuse_type_id)
);
/* CONSTRAINT PK_refuse_amount PRIMARY KEY (food_id, refuse_type_id),*/

/*
This is a principal file. This file contains the yield from refuse and/or cooking losses
assigned to certain foods. These yields are most often used for food inventory
purposes.
*/
CREATE TABLE IF NOT EXISTS yield_amount (
	id MEDIUMINT UNSIGNED AUTO_INCREMENT,
	food_id MEDIUMINT UNSIGNED,
	yield_type_id MEDIUMINT UNSIGNED,
	amount DECIMAL,
	entry_date DATE NULL,
	CONSTRAINT PK_yield_amount PRIMARY KEY (id),
	CONSTRAINT FK_yield_amount_food FOREIGN KEY (food_id) REFERENCES food(id),
	CONSTRAINT FK_yield_amount_yield FOREIGN KEY (yield_type_id) REFERENCES yield_type(id),
	CONSTRAINT UN_ryield_amount_food_yield UNIQUE INDEX(food_id, yield_type_id)
);

/**
 * CUSTOM TABLES
 */

/*
 * Scope that characteris the instake profile
 */
CREATE TABLE IF NOT EXISTS intake_profile_scope (
	id TINYINT UNSIGNED,
	name VARCHAR(200),
	description VARChAR(200),
	CONSTRAINT PK_scope PRIMARY KEY (id)
);

/*
 * Stores information about user profiles to be used for nutrient intakes
 * Describes the available profiles for nutrient intake per scope and age
 */
CREATE TABLE IF NOT EXISTS intake_profile (
	id SMALLINT UNSIGNED AUTO_INCREMENT,
	name VARCHAR(200),
	description VARCHAR(200),
	scope_id TINYINT UNSIGNED,
	age TINYINT,
	CONSTRAINT PK_intake_profile PRIMARY KEY (id),
	CONSTRAINT PK_intake_profile_scope FOREIGN KEY (scope_id) REFERENCES intake_profile_scope(id)
);

/*
 * Describes the daily nutrient intake per profile
 */
CREATE TABLE IF NOT EXISTS daily_nutrient_intake (
	id MEDIUMINT UNSIGNED AUTO_INCREMENT,
	intake_profile_id SMALLINT UNSIGNED,
	nutrient_id SMALLINT UNSIGNED,
	value DECIMAL(10,5) NOT NULL,
	CONSTRAINT PK_daily_nutrient_intake PRIMARY KEY (id),
	CONSTRAINT FK_daily_nutrient_intake_nutrient FOREIGN KEY (nutrient_id) REFERENCES nutrient(id),
	CONSTRAINT FK_daily_nutrient_intake_profile FOREIGN KEY (intake_profile_id) REFERENCES intake_profile(id),
	CONSTRAINT UN_daily_nutrient_intake_profile_nutrient UNIQUE INDEX(intake_profile_id, nutrient_id)
);


/**
 * Food constraints
 * NOTES:
 * - Should be refactored to allow flexible constraints (N Food <-> M Constratints)
 * - Quantities are expressed in grams
 */
CREATE TABLE IF NOT EXISTS food_constraint (
	id MEDIUMINT UNSIGNED AUTO_INCREMENT,
	food_id MEDIUMINT UNSIGNED,
	min_qty DECIMAL(10,5) DEFAULT 0.0,
	max_qty DECIMAL(10,5) NOT NULL,
	CONSTRAINT PK_food_constraint PRIMARY KEY (id),
	CONSTRAINT FK_food_constraint_food FOREIGN KEY (food_id) REFERENCES food(id)	
);
# CONSTRAINT UN_food_constraint_food UNIQUE INDEX(food_id)

/**
 * Nutrient constraints
 */
CREATE TABLE IF NOT EXISTS nutrient_constraint (
	id MEDIUMINT UNSIGNED AUTO_INCREMENT,
	nutrient_id SMALLINT UNSIGNED,
	weight_overconsumption DECIMAL(10,5) DEFAULT 1.0,
	weight_underconsumption DECIMAL(10,5) DEFAULT 1.0,
	CONSTRAINT PK_nutrient_constraint PRIMARY KEY (id),
	CONSTRAINT FK_nutrient_constraint_nutrient FOREIGN KEY (nutrient_id) REFERENCES nutrient(id)	
);
# CONSTRAINT nutrient_constraint UNIQUE INDEX(nutrient_id)


/**
 * Goals for the planner
 * Values expressed in g/lb
 */
CREATE TABLE IF NOT EXISTS planner_goal (
	id SMALLINT UNSIGNED AUTO_INCREMENT,
	name VARCHAR(50) UNIQUE,
	description VARCHAR(255) NULL,
	min_protein DECIMAL(10,5),
	max_protein DECIMAL(10,5),
	min_fat DECIMAL(10,5),
	max_fat DECIMAL(10,5),
	min_carb DECIMAL(10,5),
	max_carb DECIMAL(10,5),
	CONSTRAINT PK_goal PRIMARY KEY (id)
);

/**
 * Nutrients to be used in the planner calculations
 */
CREATE TABLE IF NOT EXISTS planner_nutrient (
	id SMALLINT UNSIGNED AUTO_INCREMENT,
	nutrient_id SMALLINT UNSIGNED,
	CONSTRAINT PK_planner_nutrient PRIMARY KEY (id),
	CONSTRAINT FK_planner_nutrient_nutrient FOREIGN KEY (nutrient_id) REFERENCES nutrient(id)
);