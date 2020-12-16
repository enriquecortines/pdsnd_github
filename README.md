15/12/2020
# Sparkify Datawarehouse

## Description
Discuss the purpose of this database in the context of the startup, Sparkify, and their analytical goals.
- The purpose of this Database is to provide the analytics team with business data so that they are able to provide insights to decision makers across the company
- This data is arranged in a series of tables and is based on user data generated during the app's use
- We used a star schema for faster reads with the table **songlays** as our fact table
- **time, users, songs, artists** are our dimension tables
- We developed an ETL script that uses .json files which are genereated by the user (backend) when it interacts with the app:
    - song data .json files: this files are used in the creation of artists and songs tables an contain relevent information for both tables
    - log data .json files: this files are logs of user interaction with the app and are used in the creation of songplay, user, time tables

![Screenshot](Sparkify diagram.png)

## Files used
- create_table.py: this script creates the database and tables based on the sql_queries.py file
- sql_queries.py: this script contains CREATE, INSERT and SELECT queries for the tables in the database
- etl.py: this scripts inserts data from .json files into the database tables
- .json files in data folder

## How to run
Open a terminal a type:
> python create_tables

This is to create the database a tables

To inset the data type:
>python etl.py

## Example Queries
- Number of users:
> SELECT COUNT(1) FROM USERS 

- Number of songs:
> SELECT COUNT(1) FROM SONGS

- Most5 most active paid users:
> SELECT u.user_id, u.first_name, u.last_name, u.level, count(1) 
FROM songplays sp 
JOIN users u on u.user_id = sp.user_id 
GROUP BY u.user_id, u.first_name, u.last_name, u.level 
HAVING u.level like 'paid' 
ORDER BY COUNT(1) DESC 
limit 5;
