-- Choose database
use food_nutrition;

/*
 * Load data into the "food_group" table
 */
LOAD DATA LOCAL INFILE './../data/cnf-fcen-csv/food_group.csv'
REPLACE INTO TABLE food_group
CHARACTER SET 'latin1'
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(id, code, name_en, name_fr)
;

/*
 * Load data into the "food_source" table
 */
LOAD DATA LOCAL INFILE './../data/cnf-fcen-csv/food_source.csv'
REPLACE INTO TABLE food_source
CHARACTER SET 'latin1'
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
IGNORE 1 LINES
(id, code, description_en, description_fr)
;

/*
 * Load data into the "nutrient" table
 */
LOAD DATA LOCAL INFILE './../data/cnf-fcen-csv/nutrient.csv'
REPLACE INTO TABLE nutrient
CHARACTER SET 'latin1'
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(id, code, symbol, unit, name_en, name_fr, tagname, num_decimals)
;

/*
 * Load data into the "nutrient_source" table
 */
LOAD DATA LOCAL INFILE './../data/cnf-fcen-csv/nutrient_source.csv'
REPLACE INTO TABLE nutrient_source
CHARACTER SET 'latin1'
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(id, code, description_en, description_fr)
;

/*
 * Load data into the "measure" table
 */
LOAD DATA LOCAL INFILE './../data/cnf-fcen-csv/measure.csv'
REPLACE INTO TABLE measure
CHARACTER SET 'latin1'
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, description_en, description_fr)
;

/*
 * Load data into the "refuse_type" table
 */
LOAD DATA LOCAL INFILE './../data/cnf-fcen-csv/refuse_type.csv'
REPLACE INTO TABLE refuse_type
CHARACTER SET 'latin1'
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(id,description_en, description_fr)
;

/*
 * Load data into the "yield_type" table
 */
LOAD DATA LOCAL INFILE './../data/cnf-fcen-csv/yield_type.csv'
REPLACE INTO TABLE yield_type
CHARACTER SET 'latin1'
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(id,description_en, description_fr)
;

/*
 * Load data into the "food" table
 * Issues with data.
 * Cannot cross-reference food_source_id and food_group_id
 */
LOAD DATA LOCAL INFILE './../data/cnf-fcen-csv/food.csv'
REPLACE INTO TABLE food
CHARACTER SET 'latin1'
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(id,code,group_id,source_id,description_en,description_fr,@entry_date,@publication_date,@country_code,scientific_name)
SET entry_date = nullif(@entry_date,''), publication_date = nullif(@publication_date,''), country_code = nullif(@country_code, '')
;

/**
 * Load data into the "nutrient_amount" table
 * Issues with data.
 * Cannot cross-reference nutrient_id
 */
LOAD DATA LOCAL INFILE './../data/cnf-fcen-csv/nutrient_amount.csv'
REPLACE INTO TABLE nutrient_amount
CHARACTER SET 'latin1'
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(food_id,nutrient_id,value,@standard_error,@num_observations,nutrient_source_id,@entry_date)
SET standard_error = nullif(@standard_error,''),
	num_observations = nullif(@num_observations,''),
	entry_date = nullif(@entry_date,'')
;


/*
 * Load data into the "conversion_factor" table
 * Issues with data.
 * Cannot cross-reference measure_id
 */
LOAD DATA LOCAL INFILE './../data/cnf-fcen-csv/conversion_factor.csv'
REPLACE INTO TABLE conversion_factor
CHARACTER SET 'latin1'
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(food_id, measure_id, value, entry_date)
;

/*
 * Load data into the "refuse_amount" table
 */
LOAD DATA LOCAL INFILE './../data/cnf-fcen-csv/refuse_amount.csv'
REPLACE INTO TABLE refuse_amount
CHARACTER SET 'latin1'
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(food_id, refuse_type_id, amount, entry_date)
;

/*
 * Load data into the "yield_amount" table
 */
LOAD DATA LOCAL INFILE './../data/cnf-fcen-csv/yield_amount.csv'
REPLACE INTO TABLE yield_amount
CHARACTER SET 'latin1'
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(food_id, yield_type_id, amount, entry_date)
;