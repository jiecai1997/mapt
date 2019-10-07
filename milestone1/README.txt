To create the tables for our database, one simply needs to run the following bash command, as was done in homework 2:

dropdb mapt; createdb mapt; psql mapt -af create-tables.sql

This will run the create-tables.sql file on a new databse named mapt on one's local machine. Once this is done, a user can run the following command to write the output of the queries from our file test-sample.sql into a file called test-sample.out:
psql mapt -af test-sample.sql > test-sample.out

