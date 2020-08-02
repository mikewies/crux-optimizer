#!/bin/sh

mysql -u root -p$MYSQL_ROOT_PASSWORD < /tmp/sql/initial_db_setup.sql