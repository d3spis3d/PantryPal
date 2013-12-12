PantryPal
=========

PantryPal is a webapp for home networks designed to store recipes, plan weekly meals, and organise your pantry.
It uses Flask, Twitter Bootstrap 3, and comes configured to run on lighttpd. 

Current features include:
  Users database
  Add ingredients and create recipes
  
Future features include:
  Weekly meal plans
  Store items currently in your pantry
  Generate shopping lists from weekly meal plans

Install
-------

1. Run setup.py which will install Flask and the required modules. 
2. Run db_create.py to create and initialise the sqlite database.
3. The development server can be started by running run.py from the virtualenv, 
   flask/bin/python run.py (flask/Scripts/python run.py on windows).
