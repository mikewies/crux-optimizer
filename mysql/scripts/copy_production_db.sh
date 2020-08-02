#!/bin/sh

DB_HOST=mysql
DB_USER=root
DB_PASS=rootpass
PROD_DB_NAME=food_nutrition
TEST_DB_NAME=test_$PROD_DB_NAME
echo "DROP DATABASE IF EXISTS $TEST_DB_NAME; CREATE DATABASE $TEST_DB_NAME" | \
	 mysql -h $DB_HOST -u $DB_USER -p$DB_PASS && \
	 mysqldump -h $DB_HOST -u $DB_USER -p$DB_PASS $PROD_DB_NAME | mysql -h $DB_HOST -u $DB_USER -p$DB_PASS $TEST_DB_NAME
