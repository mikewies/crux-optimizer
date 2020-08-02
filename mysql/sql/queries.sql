-- Get all nutrients amount for a given food item
/**
 * Planner nutrient symbols
 * symbol IN ('PROT', 'FAT', 'TSAT', 'CARB', 'KCAL', 'TSUG', 'TDF', 'CA', 'FE', 'MG', 'K', 'NA', 'ZN', 'VITC', 'B6', 'B12', 'TRFA', 'D-IU', 'VITK', 'CHOL')

 * Planner food ids
 * food_id IN (2605,2536,1696,2364,501578,1511,3677,1999,1704,3254,3379,3266,4086,5997,2500,1515,1705,3703,3277,2374,2378,2361,4890,2380,2548,2546,1475,1222,1472,2052,107,108,111,47,2511,918,644,640,502261,178,179,2558,2643,2063,2388,4490,184,6218,126,129,130,125,2088,1544,3339,1711,457,3139,3053,5967,2394,4230,2091,501662,1560,1562,816,742,1578,3199,3012,3338,2395,1585,1586,2397,2114,2003,4975,1721,63,2577,3925,502136,5957,3116,2127,2130,193,502343,4493,4421,420,422,2402,1619,1628,2407,1630,4517,3309,3362,3395,198,199,4724,1662,1667,4110,201,5706,502444,1670,2517,1745,1747,4497,4723,205,206,3156,503362,2608,2209,501527,4519,4725,2213,2219,1749,2526,2241,501799,2461,3206,3080,3131,502382,5702,709,2262,6196,13,2284,502776,502163,3208)
 *
 */

/*
 * Example: food_id=2605 (almond butter), 2364 = Artichoke
 */
SELECT N.symbol, NA.value, NA.nutrient_source_id
FROM nutrient_amount NA 
	INNER JOIN food F ON NA.food_id = F.id
	INNER JOIN nutrient N ON NA.nutrient_id = N.id
WHERE F.id = 1704
AND N.symbol IN ('PROT', 'FAT', 'TSAT', 'CARB', 'KCAL', 'TSUG', 'TDF', 'CA', 'FE', 'MG', 'K', 'NA', 'ZN', 'VITC', 'B6', 'B12', 'TRFA', 'D-IU', 'VITK', 'CHOL')
ORDER BY N.symbol;


-- Count nutrients per food item
SELECT F.id, COUNT(*) as total_nutrients
FROM nutrient_amount NA
	INNER JOIN food F ON NA.food_id = F.id
	INNER JOIN nutrient N ON NA.nutrient_id = N.id
WHERE F.id IN (2605,2536,1696,2364,501578,1511,3677,1999,1704,3254,3379,3266,4086,5997,2500,1515,1705,3703,3277,2374,2378,2361,4890,2380,2548,2546,1475,1222,1472,2052,107,108,111,47,2511,918,644,640,502261,178,179,2558,2643,2063,2388,4490,184,6218,126,129,130,125,2088,1544,3339,1711,457,3139,3053,5967,2394,4230,2091,501662,1560,1562,816,742,1578,3199,3012,3338,2395,1585,1586,2397,2114,2003,4975,1721,63,2577,3925,502136,5957,3116,2127,2130,193,502343,4493,4421,420,422,2402,1619,1628,2407,1630,4517,3309,3362,3395,198,199,4724,1662,1667,4110,201,5706,502444,1670,2517,1745,1747,4497,4723,205,206,3156,503362,2608,2209,501527,4519,4725,2213,2219,1749,2526,2241,501799,2461,3206,3080,3131,502382,5702,709,2262,6196,13,2284,502776,502163,3208)
AND N.symbol IN ('PROT', 'FAT', 'TSAT', 'CARB', 'KCAL', 'TSUG', 'TDF', 'CA', 'FE', 'MG', 'K', 'NA', 'ZN', 'VITC', 'B6', 'B12', 'TRFA', 'D-IU', 'VITK', 'CHOL')
GROUP BY F.id;

/*
 * Check which nutrients are chosen to be used in the planner
 */
SELECT N.id, N.symbol
FROM planner_nutrient PN
	INNER JOIN nutrient N ON PN.nutrient_id = N.id;



/**
 * Get data from daily nutrient intake
 * Male, age=29 => intake_profile_id=29
 */
SELECT N.symbol, DNI.value
FROM nutrient N
	INNER JOIN daily_nutrient_intake DNI ON N.id=DNI.nutrient_id
WHERE DNI.intake_profile_id=29;

/**
 * Get nutrient symbols for a specific set of nutrients
 * Vitam C (mg)	Vitam B6 (mg)	Vitam B12 (µg)	Vitam E (mg) 	Vitam D (µg)	Vitam K (µg)	Zinc (mg)	Potassium (mg)	Magnesium (mg)	Iron(mg)	Calcium(mg)	Fiber (mg)	Cholestorol(mg)
 * 401	415	418	875	324	430	309	306	304	303	301	291	601
 */
select symbol from nutrient where id in (401,415,418,875,324,430,309,306,304,303,301,291,601)