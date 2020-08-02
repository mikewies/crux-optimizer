# coding=utf-8

# For data export
import json

from collections import namedtuple

import unicodecsv as csv

demerits = [0.02546522, 0., 0., 0., 0., 0., 0.72372, 0., 1.60874, 0., 0., 0., 1.25, 0., 0., 0., 0., 0., 0., 0.]
goal_nutrients = [
	"kcal", "prot", "fat", "tsat", "carb", "tdf", "tsug", "calcium", "iron", "magnesium", "potassium", "sodium", "zinc", "vitamin_c", "vitamin_b6", "vitamin_b12", "trfa", "d_iu", "vitamin_k", "cholesterol"
]
min_amount = [ 2682.50, 212.75, 129.5, 0.00, 166.50, 20, 0, 750, 13.5, 262.5, 3525, 1500, 30, 56.25, 1.125, 1.8, 11.25, 15, 67.5, 0]
# TSUG goal amount was zero => add a different formula for variation
goal_amount = [2969.25, 245.13, 138.75, 34.69, 185, 25, 0.01, 1000, 18, 350, 4700, 1700, 40, 75, 1.5, 2.4, 15, 20, 90, 250]
max_amount = [3256.00, 277.50, 148, 9999.00, 203.50, 9999, 150, 99999, 9999, 9999, 9999, 2300, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 312.5]
constraints = zip(min_amount, max_amount)


weight_overconsumption = [1.00, 10.00, 50.00, 30.00, 10.00, 0, 20, 0.10, 5.00, 0.00, 0.00, 10.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.1]
weight_underconsumption = [1.00, 20.00, 5.00, 10.00, 10.00, 1, 0, 1.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 5.00, 0]

food_nutrients = [
	"kcal", "prot", "fat", "tsat", "carb", "tdf", "tsug", "ca", "fe", "mg", "k", "na", "zn", "vitc", "b6", "b12", "trfa", "d_iu", "vitk", "chol"
]


# id, short name, desc, max_qty
food_list = [
	["12195","Almond Butter","ALMOND BUTTER,PLN,WO/SALT",250],
	["12063","Almonds","ALMONDS,DRY RSTD,WO/SALT",250],
	["09003","Apple","APPLES,RAW,WITH SKIN",250],
	["11007","Artichoke","ARTICHOKES,(GLOBE OR FRENCH),RAW",250],
	["11705","Asparagus","ASPARAGUS,CKD,BLD,DRND,W/SALT",250],
	["09037","Avodacdo","AVOCADOS,RAW,ALL COMM VAR",250],
	["18007","Bagel","BAGELS,OAT BRAN",250],
	["11026","Bamboo Shoots","BAMBOO SHOOTS,RAW",250],
	["09040","Banana","BANANAS,RAW",250],
	["16018","Black Turtle Beans","BEANS,BLACK TURTLE,MATURE SEEDS,CND",250],
	["16029","Kidney Beans","BEANS,KIDNEY,ALL TYPES,MATURE SEEDS,CND",250],
	["16039","Navy Beans","BEANS,NAVY,MATURE SEEDS,CND",250],
	["19002","Beef Jerky","BEEF JERKY,CHOPD&FORMED",250],
	["13416","Eye of Round Steak","BEEF,RND,EYE OF RND RST,BNLESS,LN & FT,0 FAT,CHOIC,CKD,RSTD",0],
	["11080","Beets","BEETS,RAW",250],
	["09042","BLACKBERRIES,RAW","BLACKBERRIES,RAW",250],
	["09050","BLUEBERRIES,RAW","BLUEBERRIES,RAW",250],
	["18036","Multigrain Bread","BREAD,MULTI-GRAIN,TSTD (INCLUDES WHOLE-GRAIN)",250],
	["16054","Fava Beans","BROADBEANS (FAVA BNS),MATURE SEEDS,CND",250],
	["11090","Broccoli","BROCCOLI,RAW",250],
	["11098","Brussel Sprouts","BRUSSELS SPROUTS,RAW",250],
	["11109","Cabbage","CABBAGE,RAW",250],
	["02054","Capers","CAPERS,CANNED",250],
	["11124","Carrots","CARROTS,RAW",250],
	["12088","Cashew Butter","CASHEW BUTTER,PLN,WO/SALT",250],
	["12085","Cashew Nuts","CASHEW NUTS,DRY RSTD,WO/SALT",250],
	["08013","Cheerios","CEREALS RTE,GENERAL MILLS,CHEERIOS",250],
	["08037","Granola","CEREALS RTE,GRANOLA,HOMEMADE",250],
	["08001","All-Bran Cereal","CEREALS RTE,KELLOGG,KELLOGG'S ALL-BRAN ORIGINAL",250],
	["11147","Swiss Chard","CHARD,SWISS,RAW",250],
	["01016","Cottage Cheese (1%)","CHEESE,COTTAGE,LOWFAT,1% MILKFAT",250],
	["01019","Feta Cheese","CHEESE,FETA",250],
	["01028","Mozzarella Cheese","CHEESE,MOZZARELLA,PART SKIM MILK",250],
	["01044","Swiss Chees","CHEESE,PAST PROCESS,SWISS",250],
	["12006","Chia Seeds","CHIA SEEDS,DRIED",250],
	["05332","Ground Chicken","CHICKEN,GROUND,RAW",250],
	["05118","Lt Meat Roast Chicken","CHICKEN,ROASTING,LT MEAT,MEAT ONLY,CKD,RSTD",250],
	["05114","Roast Chicken","CHICKEN,ROASTING,MEAT ONLY,CKD,RSTD",250],
	["16358","Chickpeas","CHICKPEAS,MAT SEEDS,CND,DRND SOL",250],
	["02010","cinnamon","CINNAMON,GROUND",250],
	["02011","ground cloves","CLOVES,GROUND",250],
	["12104","coconut meat","COCONUT MEAT,RAW",250],
	["12117","coconut milk","COCONUT MILK,RAW (LIQ EXPRESSED FROM GRATED MEAT&H2O)",250],
	["11161","collards","COLLARDS,RAW",250],
	["11167","corn","CORN,SWT,YEL,RAW",250],
	["20029","couscous","COUSCOUS,COOKED",250],
	["02016","dill seed","DILL SEED",250],
	["11212","edameme","EDAMAME,FRZ,PREP",250],
	["01124","egg whites","EGG,WHITE,RAW,FRESH",250],
	["01128","eggs, whole fried","EGG,WHL,CKD,FRIED",250],
	["01129","eggs, hard boiled","EGG,WHL,CKD,HARD-BOILED",250],
	["01123","eggs, raw","EGG,WHL,RAW,FRSH",250],
	["11209","eggplant","EGGPLANT,RAW",250],
	["09088","elderberries","ELDERBERRIES,RAW",250],
	["16138","falafel, home-made","FALAFEL,HOME-PREPARED",250],
	["09089","figs","FIGS,RAW",250],
	["04589","cod liver oil","FISH OIL,COD LIVER",250],
	["15192","Pacific Cod","FISH,COD,PACIFIC,CKD,DRY HEAT (MAYBE PREVIOUSLY FROZEN)",250],
	["15086","Salmon","FISH,SALMON,SOCKEYE,CKD,DRY HEAT",250],
	["15262","Tilapia","FISH,TILAPIA,CKD,DRY HEAT",250],
	["11215","Garlic","GARLIC,RAW",250],
	["19173","Gelatin Dessert","GELATIN DSSRT,DRY MIX,PREP W/ H2O",250],
	["11216","Fresh Ginger","GINGER ROOT,RAW",250],
	["09110","Goji Berries","GOJI BERRIES,DRIED",250],
	["09107","Gooseberries","GOOSEBERRIES,RAW",250],
	["09112","Grapefruit","GRAPEFRUIT,RAW,PINK&RED,ALL AREAS",250],
	["05306","Ground Turkey","GROUND TURKEY,CKD",250],
	["05664","Ground Turkey","GROUND TURKEY,FAT FREE,PATTIES,BRLD",0],
	["09139","Common Guavas","GUAVAS,COMMON,RAW",250],
	["15034","Fresh Haddock","HADDOCK,COOKED,DRY HEAT",250],
	["15037","Halibut","HALIBUT,ATLANTIC&PACIFIC,CKD,DRY HEAT",250],
	["16137","Fresh Hummus","HUMMUS,HOME PREP",250],
	["11233","Kale","KALE,RAW",250],
	["09148","Grn Kiwifruit","KIWIFRUIT,GRN,RAW",250],
	["09149","Kumquats","KUMQUATS,RAW",250],
	["11247","Fresh Leeks","LEEKS,(BULB&LOWER LEAF-PORTION),CKD,BLD,DRND,WO/SALT",250],
	["11249","Lentils","LENTILS,SPROUTED,CKD,STIR-FRIED,WO/SALT",250],
	["11031","Immat Seeds Lima Bns","LIMA BNS,IMMAT SEEDS,RAW",250],
	["12132","Dry Rstd Macadamia Nuts","MACADAMIA NUTS,DRY RSTD,WO/SALT",250],
	["09181","Melons","MELONS,CANTALOUPE,HONEYDEW,RAW",250],
	["01082","Milk","MILK,LOWFAT,FLUID,1% MILKFAT,W/ ADDED VIT A & VITAMIN D",250],
	["12135","Mixed Nuts","MIXED NUTS,DRY RSTD,W/PNUTS,WO/SALT",250],
	["18283","Muffins","MUFFINS,OAT BRAN",250],
	["11239","Chanterelle Mushrooms","MUSHROOMS,CHANTERELLE,RAW",250],
	["11243","Mushrooms","MUSHROOMS,PORTABELLA,SHIITAKE,WHITE",250],
	["15165","Mussels","MUSSEL,BLUE,CKD,MOIST HEAT",250],
	["11271","Mustard Grns","MUSTARD GRNS,CKD,BLD,DRND,WO/SALT",250],
	["11274","(Tendergreen) Mustard Spinach","MUSTARD SPINACH,(TENDERGREEN),RAW",250],
	["02025","Nutmeg","NUTMEG,GROUND",250],
	["01250","Nutritional Supp For People W/ Diabetes","NUTRITIONAL SUPP FOR PEOPLE W/ DIABETES,LIQ",250],
	["12737","Nuts","NUTS,MXD NUTS,OIL RSTD,W/ PNUTS,LIGHTLY SALTED",250],
	["20033","Oat Bran","OAT BRAN,RAW",250],
	["20038","Oats","OATS",250],
	["04047","Coconut Oil","OIL,COCNT",250],
	["04053","Olive Oil","OIL,OLIVE,SALAD OR COOKING",250],
	["11283","Onions","ONIONS,CKD,BLD,DRND,WO/SALT",250],
	["09206","Orange Juice","ORANGE JUICE,RAW",250],
	["09226","Papayas","PAPAYAS,RAW",250],
	["11299","Parsnips","PARSNIPS,CKD,BLD,DRND,WO/SALT",250],
	["09231","Passion-Fruit","PASSION-FRUIT,(GRANADILLA),PURPLE,RAW",250],
	["20125","Whole-Wheat Pasta","PASTA,WHOLE-WHEAT,CKD",250],
	["16097","Chunk Style Peanut Butter","PEANUT BUTTER,CHUNK STYLE,W/SALT",250],
	["16390","Peanuts","PEANUTS,ALL TYPES,DRY-ROASTED,WO/SALT",250],
	["16086","Peas","PEAS,SPLIT,MATURE SEEDS,CKD,BLD,WO/SALT",250],
	["02030","Pepper","PEPPER,BLACK",250],
	["02031","Red/Cayenee Pepper","PEPPER,RED OR CAYENNE",250],
	["02064","Fresh Peppermint","PEPPERMINT,FRESH",250],
	["09278","Fresh Plantains","PLANTAINS,COOKED",250],
	["09286","Pomegranates","POMEGRANATES,RAW",250],
	["19034","Popcorn","POPCORN,AIR-POPPED",250],
	["02033","Poppy Seed","POPPY SEED",250],
	["11356","Potatoes","POTATOES,RUSSET,FLESH & SKN,BKD",250],
	["01224","Muscle Milk Protein","PROTEIN SUPP,MILK BSD,MUSCLE MILK LT,PDR",250],
	["09289","Prunes","PRUNES,DEHYD (LOW-MOISTURE),UNCKD",250],
	["12016","Rstd Pumpkin&Squash Sd Krnls","PUMPKIN&SQUASH SD KRNLS,RSTD,WO/SALT",250],
	["09298","Raisins","RAISINS,SEEDLESS",250],
	["09302","Raspberries","RASPBERRIES,RAW",250],
	["20037","Brown Rice","RICE,BROWN,LONG-GRAIN,CKD",250],
	["02063","Rosemary","ROSEMARY,FRESH",250],
	["02037","Saffron","SAFFRON",250],
	["02038","Fresh Sage","SAGE,GROUND",250],
	["15209","Atlantic Wild Salmon","SALMON,ATLANTIC,WILD,CKD,DRY HEAT",250],
	["12012","Hemp Sd Seeds","SEEDS,HEMP SD,HULLED",250],
	["12198","Sesame Butter","SESAME BUTTER,TAHINI,FROM RAW&STONE GROUND KRNLS",60],
	["11451","Soybeans","SOYBEANS,GRN,CKD,BLD,DRND,WO/SALT",0],
	["16222","Soymilk (All Flavors)","SOYMILK (ALL FLAVORS),UNSWTND,W/ ADDED CA,VITAMINS A & D",0],
	["20127","Spinach Spaghetti","SPAGHETTI,SPINACH,COOKED",250],
	["02065","Spearmint","SPEARMINT,FRESH",250],
	["11457","Spinach","SPINACH,RAW",250],
	["11468","Squash","SQUASH,SMMR,CROOKNECK & STRAIGHTNECK,CKD,BLD,DRND,WO/ SALT",250],
	["09316","Strawberries","STRAWBERRIES,RAW",250],
	["12036","Sunflower Sd Krnls","SUNFLOWER SD KRNLS,DRIED",250],
	["11508","Sweet Potato","SWEET POTATO,CKD,BKD IN SKN,FLESH,WO/ SALT",250],
	["16129","Fried Tofu","TOFU,FRIED",250],
	["11530","Tomatoes","TOMATOES,RED,RIPE,CKD",250],
	["15116","Wild Rainbow Trout","TROUT,RAINBOW,WILD,CKD,DRY HEAT",250],
	["15118","Fresh Bluefin Tuna","TUNA,FRSH,BLUEFIN,CKD,DRY HEAT",250],
	["15184","Light Canned Tuna","TUNA,LT,CND IN H2O,WO/SALT,DRND SOL",250],
	["07944","Deli Turkey","TURKEY  WHITE  ROTISSERIE  DELI CUT",250],
	["07046","Deli Turkey Breast","TURKEY BREAST,LO SALT,PREPACKAGED OR DELI,LUNCHEON MEAT",250],
	["05186","Lt Meat Turkey","TURKEY,ALL CLASSES,LT MEAT,CKD,RSTD",0],
	["11565","Turnips","TURNIPS,CKD,BLD,DRND,WO/SALT",250],
	["02069","Balsamic Vinegar","VINEGAR,BALSAMIC",250],
	["02048","Cider Vinegar","VINEGAR,CIDER",250],
	["11602","Yam","YAM,CKD,BLD,DRND,OR BKD,WO/SALT",250],
	["01256","Plain Greek Yogurt Fat-Free","YOGURT,GREEK,PLN,NONFAT",250],
	["01117","LoFat Plain Yogurt","YOGURT,PLN,LOFAT,12 GRAMS PROT PER 8 OZ",250],
	["35165","Whitefish","FISH,WHITEFISH,DRIED (ALASKA NATIVE)",250],
	["99999","Basic Multivitamin","CENTRUM",250],
	["99998","Women MultiVitamin","CENTRUM WOMEN",250],
	["99997","Men MultiVitamin","CENTRUM MEN",250]
]

food_nutrition_data = [
[614, 20.96, 55.5, 4.152, 46.058, 18.82, 10.3, 4.43, 347, 3.49, 279, 748, 7, 3.29, 0, 0.103, 0, 24.21, 0, 0, 0],
[598, 20.96, 52.54, 4.092, 46.031, 21.01, 10.9, 4.86, 268, 3.73, 279, 713, 3, 3.31, 0, 0.136, 0, 23.9, 0, 0, 0],
[52, 0.26, 0.17, 0.028, 0.058, 13.81, 2.4, 10.39, 6, 0.12, 5, 107, 1, 0.04, 4.6, 0.041, 0, 0.18, 0, 2.2, 0],
[47, 3.27, 0.15, 0.036, 0.069, 10.51, 5.4, 0.99, 44, 1.28, 60, 370, 94, 0.49, 11.7, 0.116, 0, 0.19, 0, 14.8, 0],
[22, 2.4, 0.22, 0.048, 0.105, 4.11, 2, 1.3, 23, 0.91, 14, 224, 240, 0.6, 7.7, 0.079, 0, 1.5, 0, 50.6, 0],
[160, 2, 14.66, 2.126, 11.615, 8.53, 6.7, 0.66, 12, 0.55, 29, 485, 7, 0.64, 10, 0.257, 0, 2.07, 0, 21, 0],
[255, 10.7, 1.2, 0.191, 0.735, 53.3, 3.6, 1.63, 12, 3.08, 31, 115, 590, 0.9, 0.2, 0.043, 0, 0.33, 0, 0.4, 0],
[27, 2.6, 0.3, 0.069, 0.141, 5.2, 2.2, 3, 13, 0.5, 3, 533, 4, 1.1, 4, 0.24, 0, 1, 0, 0, 0],
[89, 1.09, 0.33, 0.112, 0.105, 22.84, 2.6, 12.23, 5, 0.26, 27, 358, 1, 0.15, 8.7, 0.367, 0, 0.1, 0, 0.5, 0],
[91, 6.03, 0.29, 0.075, 0.15, 16.55, 6.9, 0.23, 35, 1.9, 35, 308, 384, 0.54, 2.7, 0.055, 0, 0.62, 0, 2.3, 0],
[84, 5.22, 0.6, 0.141, 0.645, 14.5, 4.3, 1.85, 34, 1.17, 27, 237, 296, 0.46, 1.2, 0.074, 0, 0.02, 0, 4.1, 0],
[113, 7.53, 0.43, 0.112, 0.224, 20.45, 5.1, 0.28, 47, 1.85, 47, 288, 336, 0.77, 0.7, 0.103, 0, 0.78, 0, 2.9, 0],
[410, 33.2, 25.6, 10.85, 12.316, 11, 1.8, 9, 20, 5.42, 51, 597, 2081, 8.11, 0, 0.179, 0.99, 0.49, 11, 2.3, 48],
[171, 29.79, 4.83, 1.656, 2.292, 0, 0, 0, 16, 1.86, 15, 408, 66, 4.32, 0, 0.817, 2.13, 0.31, 1, 1.3, 74],
[43, 1.61, 0.17, 0.027, 0.092, 9.56, 2.8, 6.76, 16, 0.8, 23, 325, 78, 0.35, 4.9, 0.067, 0, 0.04, 0, 0.2, 0],
[43, 1.39, 0.49, 0.014, 0.327, 9.61, 5.3, 4.88, 29, 0.62, 20, 162, 1, 0.53, 21, 0.03, 0, 1.17, 0, 19.8, 0],
[57, 0.74, 0.33, 0.028, 0.193, 14.49, 2.4, 9.96, 6, 0.28, 6, 77, 1, 0.16, 9.7, 0.052, 0, 0.57, 0, 19.3, 0],
[288, 14.52, 4.6, 0.948, 2.861, 47.11, 8.1, 6.94, 111, 2.72, 85, 250, 414, 1.85, 0.1, 0.286, 0, 0.4, 0, 1.5, 0],
[71, 8, 0.7, 0.1, 0.4, 18, 8, 0, 26, 1, 32, 242, 453, 0.62, 1.8, 0.045, 0, 0, 0, 0, 0],
[34, 2.82, 0.37, 0.039, 0.049, 6.64, 2.6, 1.7, 47, 0.73, 21, 316, 33, 0.41, 89.2, 0.175, 0, 0.78, 0, 101.6, 0],
[43, 3.38, 0.3, 0.062, 0.176, 8.95, 3.8, 2.2, 42, 1.4, 23, 389, 25, 0.42, 85, 0.219, 0, 0.88, 0, 177, 0],
[25, 1.28, 0.1, 0.034, 0.034, 5.8, 2.5, 3.2, 40, 0.47, 12, 170, 18, 0.18, 36.6, 0.124, 0, 0.15, 0, 76, 0],
[23, 2.36, 0.86, 0.233, 0.367, 4.89, 3.2, 0.41, 40, 1.67, 33, 40, 2348, 0.32, 4.3, 0.023, 0, 0.88, 0, 24.6, 0],
[41, 0.93, 0.24, 0.037, 0.131, 9.58, 2.8, 4.74, 33, 0.3, 12, 320, 69, 0.24, 5.9, 0.138, 0, 0.66, 0, 13.2, 0],
[587, 17.56, 49.41, 9.763, 37.476, 27.57, 2, 0, 43, 5.03, 258, 546, 15, 5.16, 0, 0.252, 0, 0, 0, 0, 0],
[574, 15.31, 46.35, 9.157, 35.153, 32.69, 3, 5.01, 45, 6, 260, 565, 16, 5.6, 0, 0.256, 0, 0.92, 0, 34.7, 0],
[376, 12.09, 6.73, 1.5, 4.808, 73.23, 9.4, 4.36, 401, 33.17, 114, 641, 497, 16.73, 21.6, 2.39, 6.77, 0.65, 136, 1.8, 0],
[489, 13.67, 24.31, 3.957, 18.76, 53.88, 8.9, 19.8, 76, 3.95, 168, 539, 26, 4.17, 1.2, 0.37, 0, 11.1, 0, 5.3, 0],
[259, 13.14, 4.9, 1.1, 2.89, 74.24, 29.3, 15.69, 389, 17.6, 362, 1020, 258, 12.4, 20, 12, 18.8, 1.19, 170, 5.2, 0],
[19, 1.8, 0.2, 0.03, 0.11, 3.74, 1.6, 1.1, 51, 1.8, 81, 379, 213, 0.36, 30, 0.099, 0, 1.89, 0, 830, 0],
[72, 12.39, 1.02, 0.645, 0.322, 2.72, 0, 2.72, 61, 0.14, 5, 86, 406, 0.38, 0, 0.068, 0.63, 0.01, 0, 0.1, 4],
[264, 14.21, 21.28, 14.946, 5.214, 4.09, 0, 4.09, 493, 0.65, 19, 62, 917, 2.88, 0, 0.424, 1.69, 0.18, 16, 1.8, 89],
[254, 24.26, 15.92, 10.114, 4.982, 2.77, 0, 1.13, 782, 0.22, 23, 84, 619, 2.76, 0, 0.07, 0.82, 0.14, 12, 1.6, 64],
[334, 24.73, 25.01, 16.045, 7.668, 2.1, 0, 1.23, 772, 0.61, 29, 216, 1370, 3.61, 0, 0.036, 1.23, 0.34, 18, 2.2, 85],
[486, 16.54, 30.74, 3.33, 25.974, 42.12, 34.4, 0, 631, 7.72, 335, 407, 16, 4.58, 1.6, 0, 0, 0.5, 0, 0, 0],
[143, 17.44, 8.1, 2.301, 5.119, 0.04, 0, 0, 6, 0.82, 21, 522, 60, 1.47, 0, 0.512, 0.56, 0.27, 0, 0.8, 86],
[153, 27.13, 4.07, 1.08, 2.45, 0, 0, 0, 13, 1.08, 23, 236, 51, 0.78, 0, 0.54, 0.31, 0.27, 5, 0.3, 75],
[167, 25.01, 6.63, 1.81, 4.01, 0, 0, 0, 12, 1.21, 21, 229, 75, 1.52, 0, 0.41, 0.29, 0, 0, 0, 75],
[139, 7.05, 2.77, 0.214, 1.455, 22.53, 6.4, 4.01, 45, 1.07, 26, 126, 246, 0.63, 0.1, 0.116, 0, 0.29, 0, 3.4, 0],
[247, 3.99, 1.24, 0.345, 0.314, 80.59, 53.1, 2.17, 1002, 8.32, 60, 431, 10, 1.83, 3.8, 0.158, 0, 2.32, 0, 31.2, 0],
[274, 5.97, 13, 3.952, 4.999, 65.53, 33.9, 2.38, 632, 11.83, 259, 1020, 277, 2.32, 0.2, 0.391, 0, 8.82, 0, 141.8, 0],
[354, 3.33, 33.49, 29.698, 1.791, 15.23, 9, 6.23, 14, 2.43, 32, 356, 20, 1.1, 3.3, 0.054, 0, 0.24, 0, 0.2, 0],
[230, 2.29, 23.84, 21.14, 1.275, 5.54, 2.2, 3.34, 16, 1.64, 37, 263, 15, 0.67, 2.8, 0.033, 0, 0.15, 0, 0.1, 0],
[32, 3.02, 0.61, 0.055, 0.231, 5.42, 4, 0.46, 232, 0.47, 27, 213, 17, 0.21, 35.3, 0.165, 0, 2.26, 0, 437.1, 0],
[86, 3.27, 1.35, 0.325, 0.919, 18.7, 2, 6.26, 2, 0.52, 37, 270, 15, 0.46, 6.8, 0.093, 0, 0.07, 0, 0.3, 0],
[112, 3.79, 0.16, 0.029, 0.086, 23.22, 1.4, 0.1, 8, 0.38, 8, 58, 5, 0.26, 0, 0.051, 0, 0.13, 0, 0.1, 0],
[305, 15.98, 14.54, 0.73, 10.42, 55.17, 21.1, 0, 1516, 16.33, 256, 1186, 20, 5.2, 21, 0.25, 0, 0, 0, 0, 0],
[121, 11.91, 5.2, 0.62, 3.438, 8.91, 5.2, 2.18, 63, 2.27, 64, 436, 6, 1.37, 6.1, 0.1, 0, 0.68, 0, 26.7, 0],
[52, 10.9, 0.17, 0, 0, 0.73, 0, 0.71, 7, 0.08, 11, 163, 166, 0.03, 0, 0.005, 0.09, 0, 0, 0, 0],
[196, 13.61, 14.84, 4.323, 9.433, 0.83, 0, 0.4, 62, 1.89, 13, 152, 207, 1.39, 0, 0.184, 0.97, 1.31, 88, 5.6, 401],
[155, 12.58, 10.61, 3.267, 5.491, 1.12, 0, 1.12, 50, 1.19, 10, 126, 124, 1.05, 0, 0.121, 1.11, 1.03, 87, 0.3, 373],
[143, 12.56, 9.51, 3.126, 5.569, 0.72, 0, 0.37, 56, 1.75, 12, 138, 142, 1.29, 0, 0.17, 0.89, 1.05, 82, 0.3, 372],
[25, 0.98, 0.18, 0.034, 0.092, 5.88, 3, 3.53, 9, 0.23, 14, 229, 2, 0.16, 2.2, 0.084, 0, 0.3, 0, 3.5, 0],
[73, 0.66, 0.5, 0.023, 0.327, 18.4, 7, 0, 38, 1.6, 5, 280, 6, 0.11, 36, 0.23, 0, 0, 0, 0, 0],
[333, 13.31, 17.8, 2.383, 14.331, 31.84, 0, 0, 54, 3.42, 82, 585, 294, 1.5, 1.6, 0.125, 0, 0, 0, 0, 0],
[74, 0.75, 0.3, 0.06, 0.21, 19.18, 2.9, 16.26, 35, 0.37, 17, 232, 1, 0.15, 2, 0.113, 0, 0.11, 0, 4.7, 0],
[902, 0, 100, 22.608, 69.252, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10000, 0, 570],
[85, 18.73, 0.5, 0.105, 0.29, 0, 0, 0, 10, 0.2, 24, 289, 372, 0.39, 0, 0.136, 2.31, 0.67, 24, 0, 57],
[156, 26.48, 5.57, 0.969, 3.191, 0, 0, 0, 11, 0.52, 36, 436, 92, 0.55, 0, 0.827, 4.47, 0.99, 670, 0.1, 61],
[128, 26.15, 2.65, 0.94, 1.555, 0, 0, 0, 14, 0.69, 34, 380, 56, 0.41, 0, 0.123, 1.86, 0.79, 150, 0.9, 57],
[149, 6.36, 0.5, 0.089, 0.26, 33.06, 2.1, 1, 181, 1.7, 25, 401, 17, 1.16, 31.2, 1.235, 0, 0.08, 0, 1.7, 0],
[62, 1.22, 0, 0, 0, 14.19, 0, 13.49, 3, 0.02, 1, 1, 75, 0.01, 0, 0, 0, 0, 0, 0, 0],
[80, 1.82, 0.75, 0.203, 0.308, 17.77, 2, 1.7, 16, 0.6, 43, 415, 13, 0.34, 5, 0.16, 0, 0.26, 0, 0.1, 0],
[349, 14.26, 0.39, 0, 0, 77.06, 13, 45.61, 190, 6.8, 0, 0, 298, 0, 48.4, 0, 0, 0, 0, 0, 0],
[44, 0.88, 0.58, 0.038, 0.368, 10.18, 4.3, 0, 25, 0.31, 10, 198, 1, 0.12, 27.7, 0.08, 0, 0.37, 0, 0, 0],
[42, 0.77, 0.14, 0.021, 0.056, 10.66, 1.6, 6.89, 22, 0.08, 9, 135, 0, 0.07, 31.2, 0.053, 0, 0.13, 0, 0, 0],
[203, 27.37, 10.4, 2.669, 6.375, 0, 0, 0, 28, 1.52, 30, 294, 78, 3.11, 0, 0.633, 1.34, 0.11, 8, 0, 93],
[138, 28.99, 2.48, 0.673, 1.472, 0, 0, 0, 6, 0.78, 35, 339, 59, 2.19, 0, 0.908, 0.67, 0.09, 8, 0, 65],
[68, 2.55, 0.95, 0.272, 0.488, 14.32, 5.4, 8.92, 18, 0.26, 22, 417, 2, 0.23, 228.3, 0.11, 0, 0.73, 0, 2.6, 0],
[90, 19.99, 0.55, 0.111, 0.278, 0, 0, 0, 14, 0.21, 26, 351, 261, 0.4, 0, 0.327, 2.13, 0.55, 23, 0.1, 66],
[111, 22.54, 1.61, 0.354, 0.925, 0, 0, 0, 9, 0.2, 28, 528, 82, 0.43, 0, 0.632, 1.27, 0.74, 231, 0, 60],
[177, 4.86, 8.59, 1.141, 6.974, 20.12, 4, 0.27, 49, 1.56, 29, 173, 242, 1.09, 7.9, 0.399, 0, 0.75, 0, 3, 0],
[49, 4.28, 0.93, 0.091, 0.39, 8.75, 3.6, 2.26, 150, 1.47, 47, 491, 38, 0.56, 120, 0.271, 0, 1.54, 0, 704.8, 0],
[61, 1.14, 0.52, 0.029, 0.334, 14.66, 3, 8.99, 34, 0.31, 17, 312, 3, 0.14, 92.7, 0.063, 0, 1.46, 0, 40.3, 0],
[71, 1.88, 0.86, 0.103, 0.325, 15.9, 6.5, 9.36, 62, 0.86, 20, 186, 10, 0.17, 43.9, 0.036, 0, 0.15, 0, 0, 0],
[31, 0.81, 0.2, 0.027, 0.114, 7.62, 1, 2.11, 30, 1.1, 14, 87, 10, 0.06, 4.2, 0.113, 0, 0.5, 0, 25.4, 0],
[101, 8.8, 0.45, 0.053, 0.296, 21.25, 0, 0, 14, 3.1, 35, 284, 10, 1.6, 12.6, 0.164, 0, 0, 0, 0, 0],
[113, 6.84, 0.86, 0.198, 0.469, 20.17, 4.9, 1.48, 34, 3.14, 58, 467, 8, 0.78, 23.4, 0.204, 0, 0.32, 0, 5.6, 0],
[718, 7.79, 76.08, 11.947, 60.773, 13.38, 8, 4.14, 70, 2.65, 118, 363, 4, 1.29, 0.7, 0.359, 0, 0.57, 0, 0, 0],
[34, 0.84, 0.19, 0.051, 0.084, 8.16, 0.9, 7.86, 9, 0.21, 12, 267, 16, 0.18, 36.7, 0.072, 0, 0.05, 0, 2.5, 0],
[42, 3.37, 0.97, 0.633, 0.312, 4.99, 0, 5.2, 125, 0.03, 11, 150, 44, 0.42, 0, 0.037, 0.47, 0.01, 48, 0.1, 5],
[607, 19.5, 53.5, 8.01, 44.39, 22.42, 6.4, 5, 87, 3.73, 227, 643, 4, 4.06, 0.8, 0.36, 0, 6.13, 0, 12, 0],
[270, 7, 7.4, 1.087, 5.824, 48.3, 4.6, 8.22, 63, 4.2, 157, 507, 393, 1.84, 0, 0.161, 0.01, 0.66, 0, 13, 0],
[38, 1.49, 0.53, 0, 0, 6.86, 3.8, 1.16, 15, 3.47, 13, 506, 9, 0.71, 0, 0.044, 0, 0, 212, 0, 0],
[29, 3.28, 0.58, 0.064, 0.241, 4.44, 2.2, 2.26, 3, 0.4, 13, 437, 11, 0.65, 0, 0.122, 0, 0, 14, 0, 0],
[172, 23.8, 4.48, 0.85, 2.226, 7.39, 0, 0, 33, 6.72, 37, 268, 369, 2.67, 13.6, 0.1, 24, 0, 0, 0, 56],
[26, 2.56, 0.47, 0.012, 0.156, 4.51, 2, 1.41, 118, 0.87, 13, 162, 9, 0.22, 25.3, 0.098, 0, 1.78, 0, 592.7, 0],
[22, 2.2, 0.3, 0.015, 0.195, 3.9, 2.8, 0, 210, 1.5, 11, 449, 21, 0.17, 130, 0.153, 0, 0, 0, 0, 0],
[525, 5.84, 36.31, 25.94, 3.57, 49.29, 20.8, 2.99, 184, 3.04, 183, 350, 16, 2.15, 3, 0.16, 0, 0, 0, 0, 0],
[88, 4.4, 3.08, 0.232, 2.713, 11.88, 2.2, 2.64, 110, 1.98, 44, 176, 92, 1.65, 26.4, 0.22, 0.66, 1.46, 44, 8.8, 2],
[607, 20.04, 53.95, 8.711, 43.1, 21.05, 7, 4.15, 117, 2.61, 229, 632, 161, 3.36, 0.5, 0.352, 0, 7.82, 0, 5.7, 0],
[246, 17.3, 7.03, 1.328, 5.142, 66.22, 15.4, 1.45, 58, 5.41, 235, 566, 4, 3.11, 0, 0.165, 0, 1.01, 0, 3.2, 0],
[389, 16.89, 6.9, 1.217, 4.713, 66.27, 10.6, 0, 54, 4.72, 177, 429, 2, 3.97, 0, 0.119, 0, 0, 0, 0, 0],
[892, 0, 99.06, 82.475, 8.034, 0, 0, 0, 1, 0.05, 0, 0, 0, 0.02, 0, 0, 0, 0.11, 0, 0.6, 0],
[884, 0, 100, 13.808, 83.484, 0, 0, 0, 1, 0.56, 0, 1, 2, 0, 0, 0, 0, 14.35, 0, 60.2, 0],
[44, 1.36, 0.19, 0.031, 0.1, 10.15, 1.4, 4.73, 22, 0.24, 11, 166, 3, 0.21, 5.2, 0.129, 0, 0.02, 0, 0.5, 0],
[45, 0.7, 0.2, 0.024, 0.076, 10.4, 0.2, 8.4, 11, 0.2, 11, 200, 1, 0.05, 50, 0.04, 0, 0.04, 0, 0.1, 0],
[43, 0.47, 0.26, 0.081, 0.13, 10.82, 1.7, 7.82, 20, 0.25, 21, 182, 8, 0.08, 60.9, 0.038, 0, 0.3, 0, 2.6, 0],
[71, 1.32, 0.3, 0.05, 0.159, 17.01, 3.6, 4.8, 37, 0.58, 29, 367, 10, 0.26, 13, 0.093, 0, 1, 0, 1, 0],
[97, 2.2, 0.7, 0.059, 0.497, 23.38, 10.4, 11.2, 12, 1.6, 29, 348, 28, 0.1, 30, 0.1, 0, 0.02, 0, 0.7, 0],
[149, 5.99, 1.71, 0.243, 0.75, 30.07, 3.9, 0.75, 13, 1.72, 54, 96, 4, 1.34, 0, 0.093, 0, 0.23, 0, 0.6, 0],
[589, 24.06, 49.94, 7.607, 37.055, 21.57, 8, 8.41, 45, 1.9, 160, 745, 486, 2.79, 0, 0.418, 0, 6.3, 0, 0.5, 0],
[587, 24.35, 49.66, 7.723, 35.954, 21.26, 8.4, 4.9, 58, 1.58, 178, 634, 6, 2.77, 0, 0.466, 0, 4.93, 0, 0, 0],
[118, 8.34, 0.39, 0.054, 0.246, 21.1, 8.3, 2.9, 14, 1.29, 36, 362, 2, 1, 0.4, 0.048, 0, 0.03, 0, 5, 0],
[251, 10.39, 3.26, 1.392, 1.737, 63.95, 25.3, 0.64, 443, 9.71, 171, 1329, 20, 1.19, 0, 0.291, 0, 1.04, 0, 163.7, 0],
[318, 12.01, 17.27, 3.26, 11.12, 56.63, 27.2, 10.34, 148, 7.8, 152, 2014, 30, 2.48, 76.4, 2.45, 0, 29.83, 0, 80.3, 0],
[70, 3.75, 0.94, 0.246, 0.541, 14.89, 8, 0, 243, 5.08, 80, 569, 31, 1.11, 31.8, 0.129, 0, 0, 0, 0, 0],
[116, 0.79, 0.18, 0.069, 0.048, 31.15, 2.3, 14, 2, 0.58, 32, 465, 5, 0.13, 10.9, 0.24, 0, 0.13, 0, 0.7, 0],
[83, 1.67, 1.17, 0.12, 0.172, 18.7, 4, 13.67, 10, 0.3, 12, 236, 3, 0.35, 10.2, 0.075, 0, 0.6, 0, 16.4, 0],
[387, 12.94, 4.54, 0.637, 3.268, 77.78, 14.5, 0.87, 7, 3.19, 144, 329, 8, 3.08, 0, 0.157, 0, 0.29, 0, 1.2, 0],
[525, 17.99, 41.56, 4.517, 34.551, 28.13, 19.5, 2.99, 1438, 9.76, 347, 719, 26, 7.9, 1, 0.247, 0, 1.77, 0, 0, 0],
[97, 2.63, 0.13, 0.032, 0.057, 21.44, 2.3, 1.08, 18, 1.07, 30, 550, 14, 0.35, 8.3, 0.354, 0, 0.07, 0, 2, 0],
[396, 50, 12, 1.087, 9.713, 22, 2, 4, 1200, 12, 280, 840, 250, 10, 42, 1.4, 4.2, 9.45, 280, 0.5, 10],
[339, 3.7, 0.73, 0.059, 0.642, 89.07, 0, 0, 72, 3.52, 64, 1058, 5, 0.75, 0, 0.745, 0, 0, 0, 0, 0],
[574, 29.84, 49.05, 8.544, 35.59, 14.71, 6.5, 1.29, 52, 8.07, 550, 788, 18, 7.64, 1.8, 0.1, 0, 0.56, 0, 4.5, 0],
[299, 3.07, 0.46, 0.058, 0.088, 79.18, 3.7, 59.19, 50, 1.88, 32, 749, 11, 0.22, 2.3, 0.174, 0, 0.12, 0, 3.5, 0],
[52, 1.2, 0.65, 0.019, 0.439, 11.94, 6.5, 4.42, 25, 0.69, 22, 151, 1, 0.42, 26.2, 0.055, 0, 0.87, 0, 7.8, 0],
[123, 2.74, 0.97, 0.26, 0.735, 25.58, 1.6, 0.24, 3, 0.56, 39, 86, 4, 0.71, 0, 0.123, 0, 0.17, 0, 0.2, 0],
[131, 3.31, 5.86, 2.838, 2.061, 20.7, 14.1, 0, 317, 6.65, 91, 668, 26, 0.93, 21.8, 0.336, 0, 0, 0, 0, 0],
[310, 11.43, 5.85, 1.586, 2.496, 65.37, 3.9, 0, 111, 11.1, 264, 1724, 148, 1.09, 80.8, 1.01, 0, 0, 0, 0, 0],
[315, 10.63, 12.75, 7.03, 3.63, 60.73, 40.3, 1.71, 1652, 28.12, 428, 1070, 11, 4.7, 32.4, 2.69, 0, 7.48, 0, 1714.5, 0],
[182, 25.44, 8.13, 1.257, 5.953, 0, 0, 0, 15, 1.03, 37, 628, 56, 0.82, 0, 0.944, 3.05, 0, 0, 0, 71],
[553, 31.56, 48.75, 4.6, 43.5, 8.67, 4, 1.5, 70, 7.95, 700, 1200, 5, 9.9, 0.5, 0.6, 0, 0.8, 0, 0, 0],
[570, 17.81, 48, 6.722, 39.166, 26.19, 9.3, 0, 420, 2.51, 96, 414, 74, 4.64, 0, 0.149, 0, 0, 0, 0, 0],
[141, 12.35, 6.4, 0.74, 4.22, 11.05, 4.2, 0, 145, 2.5, 60, 539, 14, 0.91, 17, 0.06, 0, 0, 0, 0, 0],
[33, 2.86, 1.61, 0.206, 1.401, 1.74, 0.5, 0.41, 124, 0.46, 16, 120, 37, 0, 0, 0.049, 1.11, 0, 49, 0, 0],
[130, 4.58, 0.63, 0.091, 0.329, 26.15, 0, 0, 30, 1.04, 62, 58, 14, 1.08, 0, 0.096, 0, 0, 0, 0, 0],
[44, 3.29, 0.73, 0.191, 0.419, 8.41, 6.8, 0, 199, 11.87, 63, 458, 30, 1.09, 13.3, 0.158, 0, 0, 0, 0, 0],
[23, 2.86, 0.39, 0.063, 0.175, 3.63, 2.2, 0.42, 99, 2.71, 79, 558, 79, 0.53, 28.1, 0.195, 0, 2.03, 0, 482.9, 0],
[23, 1.04, 0.39, 0.064, 0.154, 3.79, 1.1, 2.48, 22, 0.37, 16, 177, 1, 0.22, 11.6, 0.078, 0, 0.12, 0, 4.4, 0],
[32, 0.67, 0.3, 0.015, 0.198, 7.68, 2, 4.89, 16, 0.41, 13, 153, 1, 0.14, 58.8, 0.047, 0, 0.29, 0, 2.2, 0],
[584, 20.78, 51.46, 4.455, 41.665, 20, 8.6, 2.62, 78, 5.25, 325, 645, 9, 5, 1.4, 1.345, 0, 35.17, 0, 0, 0],
[90, 2.01, 0.15, 0.052, 0.094, 20.71, 3.3, 6.48, 38, 0.69, 27, 475, 36, 0.32, 19.6, 0.286, 0, 0.71, 0, 2.3, 0],
[270, 18.82, 20.18, 2.918, 15.846, 8.86, 3.9, 2.72, 372, 4.87, 60, 146, 16, 1.99, 0, 0.099, 0, 0.04, 0, 7.8, 0],
[18, 0.95, 0.11, 0.015, 0.06, 4.01, 0.7, 2.49, 11, 0.68, 9, 218, 11, 0.14, 22.8, 0.079, 0, 0.56, 0, 2.8, 0],
[150, 22.92, 5.82, 1.619, 3.577, 0, 0, 0, 86, 0.38, 31, 448, 56, 0.51, 2, 0.346, 6.3, 0, 0, 0, 69],
[184, 29.91, 6.28, 1.612, 3.897, 0, 0, 0, 10, 1.31, 64, 323, 50, 0.77, 0, 0.525, 10.88, 0, 0, 0, 49],
[116, 25.51, 0.82, 0.234, 0.496, 0, 0, 0, 11, 1.53, 27, 237, 50, 0.77, 0, 0.35, 2.99, 0, 0, 0, 30],
[112, 13.5, 3, 0.118, 0.961, 7.7, 0.4, 4, 16, 2.2, 20, 349, 1200, 2.1, 10, 0.294, 0.22, 0, 0, 0, 55],
[109, 21.81, 0.83, 0.197, 0.445, 3.51, 0.5, 3.51, 8, 0.63, 21, 211, 772, 1.33, 5.7, 0.128, 0.09, 0.09, 2, 0, 44],
[147, 30.13, 2.08, 0.593, 1.154, 0, 0, 0, 9, 0.71, 32, 249, 99, 1.72, 0, 0.807, 0.37, 0.06, 10, 0, 80],
[22, 0.71, 0.08, 0.008, 0.047, 5.06, 2, 2.99, 33, 0.18, 9, 177, 16, 0.12, 11.6, 0.067, 0, 0.02, 0, 0.1, 0],
[88, 0.49, 0, 0, 0, 17.03, 0, 14.95, 27, 0.72, 12, 112, 23, 0.08, 0, 0, 0, 0, 0, 0, 0],
[21, 0, 0, 0, 0, 0.93, 0, 0.4, 7, 0.2, 5, 73, 5, 0.04, 0, 0, 0, 0, 0, 0, 0],
[116, 1.49, 0.14, 0.029, 0.065, 27.48, 3.9, 0.49, 14, 0.52, 18, 670, 8, 0.2, 12.1, 0.228, 0, 0.34, 0, 2.3, 0],
[59, 10.19, 0.39, 0.117, 0.065, 3.6, 0, 3.24, 110, 0.07, 11, 141, 36, 0.52, 0, 0.063, 0.75, 0.01, 0, 0, 5],
[63, 5.25, 1.55, 1, 0.47, 7.04, 0, 7.04, 183, 0.08, 17, 234, 70, 0.89, 0.8, 0.049, 0.56, 0.03, 1, 0.2, 6],
[371, 62.44, 13.44, 2.85, 6.54, 0, 0, 0, 810, 4.1, 85, 1080, 0, 5, 0, 0.365, 18.4, 0.66, 0, 1.3, 266],
[0, 0, 0, 0, 0, 0, 0, 0, 17500, 1000, 5000, 0, 0, 0, 9000, 300, 1400, 1675, 1000, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 40000, 750, 6400, 0, 0, 800, 15000, 500, 2160, 1876, 2000, 2000, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 30000, 600, 8400, 0, 0, 1100, 18000, 550, 460, 2680, 2000, 2500, 0]
]

def export_as_json(obj, filepath):
	fp = open(filepath, "w")

	json.dump(obj, fp,  indent=4, separators=(',', ': '), ensure_ascii=False)

def export_food_as_json(filepath):
	food_items = []
	for food_idx in range(0, len(food_list)):
		food_meta = food_list[food_idx]
		food_nutrition = food_nutrition_data[food_idx]
		food_item = {
			'id': food_meta[0],
			'name': food_meta[1],
			'description': food_meta[2],
			'nutritionData': []
		}

		for nutrient_idx in range(0, len(nutrients)):
			nutrient_id = nutrients[nutrient_idx]
			nutrition_data = {
				'id': nutrient_id,
				'value': food_nutrition[nutrient_idx],
				'unit': '100g'
			}
			food_item['nutritionData'] += [nutrition_data]

		food_items += [food_item]
	nutrition_db = {
		'food': food_items,
	}
	fp = open(filepath, 'w')
	json.dump(nutrition_db, fp, indent=4, separators=(',', ': '))


# Food items CSV schema
FOOD_ITEMS_CSV_SCHEMA = {
	"hasHeader": True,
	"fields": {
		"nbd_no": {
			'index': 0,
			'name': 'ndb_no'
		},
		"name": {
			'index': 1,
			'name': 'Name'
		},
		"description": {
			'index': 2,
			'name': 'Description'
		},
		"kcal": {
			'index': 3,
			'name': 'kcal',
			'type': 'decimal',
			'metadata': {
				'units': 'kCal/100g'
			}
		},
		"prot": {
			'index': 4,
			'name': 'prot',
			'type': 'decimal',
			'metadata': {
				'units': 'g/100g'
			}
		},
		"fat": {
			'index': 5,
			'name': 'fat',
			'type': 'decimal',
			'metadata': {
				'units': 'g/100g'
			}
		},
		"tsat": {
			'index': 6,
			'name': 'tsat',
			'type': 'decimal',
			'metadata': {
				'units': 'g/100g'
			}
		},
		"carb": {
			'index': 7,
			'name': 'carb',
			'type': 'decimal',
			'metadata': {
				'units': 'g/100g'
			}
		},	
		"tdf": {
			'index': 8,
			'name': 'tdf',
			'type': 'decimal',
			'metadata': {
				'units': 'g/100g'
			}
		},
		"tsug": {
			'index': 9,
			'name': 'tsug',
			'type': 'decimal',
			'metadata': {
				'units': 'g/100'
			}
		},
		"calcium": {
			'index': 10,
			'name': 'Calcium',
			'type': 'decimal',
			'metadata': {
				'units': 'mg/100g'
			}
		},
		"iron": {
			'index': 11,
			'name': 'Iron',
			'type': 'decimal',
			'metadata': {
				'units': 'mg/100g'
			}
		},
		"magnesium": {
			'index': 12,
			'name': 'mg',
			'type': 'decimal',
			'metadata': {
				'units': 'mg/100g'
			}
		},
		"potassium": {
			'index': 13,
			'name': 'k',
			'type': 'decimal',
			'metadata': {
				'units': 'mg/100g'
			}
		},
		"sodium": {
			'index': 14,
			'name': 'Sodium',
			'type': 'decimal',
			'metadata': {
				'units': 'mg/100g'
			}
		},
		"zinc": {
			'index': 15,
			'name': 'Zinc',
			'type': 'decimal',
			'metadata': {
				'units': 'mg/100g'
			}
		},
		"vitamin_c": {
			'index': 16,
			'name': 'Vitaming C',
			'type': 'decimal',
			'metadata': {
				'units': 'mg/100g'
			}
		},
		"vitamin_b6": {
			'index': 17,
			'name': 'Vitamin B6',
			'type': 'decimal',
			'metadata': {
				'units': 'mg/100g'
			}
		},
		"vitamin_b12": {
			'index': 18,
			'name': 'Vitamin C',
			'type': 'decimal',
			'metadata': {
				'units': 'µg/100g'
			}
		},
		"trfa": {
			'index': 19,
			'name': 'trfa',
			'type': 'decimal',
			'metadata': {
				'units': 'mg/100g'
			}
		},
		"d_iu": {
			'index': 20,
			'name': 'd_iu',
			'type': 'decimal',
			'metadata': {
				'units': 'µg/100g'
			}
		},
		"vitamin_k": {
			'index': 21,
			'name': 'Vitamin K',
			'type': 'decimal',
			'metadata': {
				'units': 'µg/100g'
			}
		},
		"cholesterol": {
			'index': 22,
			'name': 'Cholesterol',
			'type': 'decimal',
			'metadata': {
				'units': 'mg/100g'
			}
		},
		"tusat": {
			'index': 23,
			'name': 'tusat',
			'type': 'decimal',
			'metadata': {
				'units': 'g/100g'
			}
		},
	}
}


# High-level goals CSV schema
HIGH_LEVEL_GOALS_CSV_SCHEMA = {
	"hasHeader": True,
	"fields": {
		'goal_name': {
			'id': 'name',
			'name': 'High-Level Goal',
			'index': 0,
		},
		'min_protein': {
			'id': 'min_protein',
			'name': 'Min Protein',
			'index': 1,
		},
		'max_protein': {
			'id': 'max_protein',
			'name': 'Max protein',
			'index': 2,
		},
		'min_fat': {
			'id': 'min_fat',
			'name': 'Min Fat',
			'index': 3,
		},
		'max_fat': {
			'id': 'max_fat',
			'name': 'Max Fat',
			'index': 4,
		},
		'min_carb': {
			'id': 'min_carb',
			'name': 'Min Carb',
			'index': 5,
		},
		'max_carb': {
			'id': 'max_carb',
			'name': 'Max carb',
			'index': 6,
		}
	}
}

# Food intake CSV schema
FOOD_INTAKE_CHART_CSV_SCHEMA = {
	"hasHeader": True,
	"fields": {
		"scope": {
			'index': 0,
			'name': 'Scope'
		},
		"age": {
			'index': 1,
			'name': 'Age'
		},
		"vitamin_c": {
			'index': 2,
			'name': 'Vitamin C',
			'type': 'decimal',
			'metadata': {
				'units': 'mg'
			}
		},
		"vitamin_b6": {
			'index': 3,
			'name': 'Vitamin B6',
			'type': 'decimal',
			'metadata': {
				'units': 'mg'
			}
		},
		"vitamin_b12": {
			'index': 4,
			'name': 'Vitamin B12',
			'type': 'decimal',
			'metadata': {
				'units': 'µg'
			}
		},
		"vitamin_e": {
			'index': 5,
			'name': 'Vitamin E',
			'type': 'decimal',
			'metadata': {
				'units': 'mg'
			}
		},
		"vitamin_d": {
			'index': 6,
			'name': 'Vitamin D',
			'type': 'decimal',
			'metadata': {
				'units': 'µg'
			}
		},	
		"vitamin_k": {
			'index': 7,
			'name': 'Vitamin K',
			'type': 'decimal',
			'metadata': {
				'units': 'µg'
			}
		},
		"zinc": {
			'index': 8,
			'name': 'Zinc',
			'type': 'decimal',
			'metadata': {
				'units': 'mg'
			}
		},
		"potassium": {
			'index': 9,
			'name': 'Potassium',
			'type': 'decimal',
			'metadata': {
				'units': 'mg'
			}
		},
		"magnesium": {
			'index': 10,
			'name': 'Magnesium',
			'type': 'decimal',
			'metadata': {
				'units': 'mg'
			}
		},
		"iron": {
			'index': 11,
			'name': 'Iron',
			'type': 'decimal',
			'metadata': {
				'units': 'mg'
			}
		},
		"calcium": {
			'index': 12,
			'name': 'Calcium',
			'type': 'decimal',
			'metadata': {
				'units': 'mg'
			}
		},
		"fiber": {
			'index': 13,
			'name': 'Fiber',
			'type': 'decimal',
			'metadata': {
				'units': 'mg'
			}
		},
		"cholesterol": {
			'index': 14,
			'name': 'Cholesterol',
			'type': 'decimal',
			'metadata': {
				'units': 'mg'
			}
		}
	}
}

# Food items constraints CSV schema
FOOD_ITEMS_CONSTRAINTS_CSV_SCHEMA = {
	'hasHeader': True,
	'fields': {
		'nbd_no': {
			'id': 'nbd_no',
			'name': 'nbd_no',
			'index': 0
		},
		'max_qty': {
			'id': 'max_qty',
			'name': 'max_qty',
			'index': 1
		}
	}
}

def import_food_items_csv_as_dict(in_filepath = None, schema = None):
	"""
	Import food items from CSV and transform to dict objects

	Args:
		in_filepath: Input filepath containing the food items description
		schema: Metadata description the input CSV schema

	Returns:
		List of dict objects describing the food items
	"""
	schema = schema or FOOD_ITEMS_CSV_SCHEMA
	in_filepath = in_filepath or 'data/food_items.csv.csv'
	fp = open(in_filepath, "r")
	csv_reader = csv.reader(fp)

	header = next(csv_reader) if 'hasHeader' in schema and schema['hasHeader'] else None

	food_nutrient_metadata_keys = ['units']
	nutrients_fields_ids = ['kcal', 'prot', 'fat', 'tsat', 'carb',
			'tdf', 'tsug', 'calcium', 'iron', 'magnesium', 'potassium', 'sodium', 'zinc', 'vitamin_c',
			'vitamin_b6', 'vitamin_b12', 'trfa', 'd_iu', 'vitamin_k', 'cholesterol', 'tusat'
	]

	food_items = []
	for data in csv_reader:
		food_item = {}
		for field_id in ['nbd_no', 'name', 'description']:
			food_item[field_id] = data[schema['fields'][field_id]['index']]
		
		food_nutrients = {}
		for nutrient_field_id in nutrients_fields_ids:
			nutrient_field_schema = schema['fields'][nutrient_field_id]
			nutrient_value = data[nutrient_field_schema['index']].strip()
			nutrient_value = 0. if not nutrient_value else float(nutrient_value)
			food_nutrient_obj = {
				'id': nutrient_field_id,
				'value': nutrient_value
			}

			if 'metadata' in nutrient_field_schema:
				for key in food_nutrient_metadata_keys:
					if not key in food_nutrient_metadata_keys:
						continue
					food_nutrient_obj[key] = nutrient_field_schema['metadata'][key]

			food_nutrients[nutrient_field_id] = food_nutrient_obj
		food_item['nutrients'] = food_nutrients

		food_items += [food_item]

	return food_items

def import_daily_intake_chart_csv_as_dict(in_filepath = None, schema = None):
	"""
	Import daily intake rules from CSV and transform to dict objects

	Args:
		in_filepath: Input filepath containing the daily intake rules description
		schema: Metadata description the input CSV schema

	Returns:
		List of dict objects describing the daily intake rules
	"""
	schema = schema or FOOD_INTAKE_CHART_CSV_SCHEMA
	in_filepath = in_filepath or 'data/daily_intake_chart.csv'
	fp = open(in_filepath, "r")
	csv_reader = csv.reader(fp)
	header = next(csv_reader) if 'hasHeader' in schema and schema['hasHeader'] else None

	nutrients_fields_ids = ['vitamin_c', 'vitamin_b6', 'vitamin_b12',
		'vitamin_e', 'vitamin_d', 'vitamin_k', 'zinc', 'potassium',
		'magnesium', 'iron', 'calcium','fiber', 'cholesterol'
	]

	intake_rules = []
	for data in csv_reader:
		intake_rule = {
			'context': {
				'user_profile': data[schema['fields']['scope']['index']].title(),
				'age': data[schema['fields']['age']['index']].title(),
				'timeframe': 'daily'
			}
		}

		nutrients = []
		for field_id in nutrients_fields_ids:
			nutrient_field_schema = schema['fields'][field_id]
			nutrient_value = data[nutrient_field_schema['index']].strip()
			nutrient_value = 0. if not nutrient_value else float(nutrient_value)
			nutrient_obj = {
				'id': field_id,
				'name':  nutrient_field_schema['name'].title(),
				'value': nutrient_value
			}
			if 'metadata' in nutrient_field_schema:
				if 'units' in nutrient_field_schema:
					nutrient_obj['units'] = nutrient_field_schema['metadata']['units']

			nutrients += [nutrient_obj]

		intake_rule['nutrients'] = nutrients
		intake_rules += [intake_rule]


	return intake_rules

def import_high_level_goals_csv_as_dict(in_filepath = None, schema = None):
	"""
	Import high-level goals from CSV and transform to dict objects

	Args:
		in_filepath: Input filepath containing the high-level goals description
		schema: Metadata description the input CSV schema

	Returns:
		List of dict objects describing the high level goals
	"""
	schema = schema or HIGH_LEVEL_GOALS_CSV_SCHEMA
	in_filepath = in_filepath or 'data/goals.csv'
	fp = open(in_filepath, "r")
	csv_reader = csv.reader(fp)
	header = next(csv_reader) if 'hasHeader' in schema and schema['hasHeader'] else None

	rules_fields_ids = ['min_protein', 'max_protein', 'min_fat', 'max_fat', 'min_carb', 'max_carb']

	goals = []
	for data in csv_reader:
		goal = {
			'name': data[schema['fields']['goal_name']['index']]
		}
		rules = []
		for rule_field_id in rules_fields_ids:
			rule_field_schema = schema['fields'][rule_field_id]
			rule_obj = {
				'name': rule_field_id,
				'value': float(data[rule_field_schema['index']])
			}
			rules += [rule_obj]

		goal['rules'] = rules
		goals += [goal]

	return goals


def import_food_items_constraints_csv_as_dict(in_filepath = None, schema = None):
	"""
	Import high-level goals from CSV and transform to dict objects

	Args:
		in_filepath: Input filepath containing the high-level goals description
		schema: Metadata description the input CSV schema

	Returns:
		List of dict objects describing the high level goals
	"""
	schema = schema or FOOD_ITEMS_CONSTRAINTS_CSV_SCHEMA
	in_filepath = in_filepath or 'data/food_items_constraints.csv'
	fp = open(in_filepath, "r")
	csv_reader = csv.reader(fp)
	header = next(csv_reader) if 'hasHeader' in schema and schema['hasHeader'] else None

	result = {}
	for data in csv_reader:
		result[data[schema['fields']['nbd_no']['index']]] = {
			'max_qty': float(data[schema['fields']['max_qty']['index']])
		}
	return result

if __name__ == '__main__':
	
	food_items = import_food_items_csv_as_dict('./data/food_items.csv')
	intake_rules = import_daily_intake_chart_csv_as_dict('./data/daily_intake_chart.csv')
	goals = import_high_level_goals_csv_as_dict('./data/goals.csv')

	export_as_json(food_items, './data/food_items.json')
	export_as_json(intake_rules, './data/daily_intake_chart.json')
	export_as_json(goals, './data/goals.json')