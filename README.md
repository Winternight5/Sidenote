# Cmpe131
# Team4
Live demo: http://sidenotex.herokuapp.com

Local Installation
  Make sure you have the proper pluggins installed (also noted in the requirements.txt):
  Python 3.6 with pip
  Required pluggins: Flask, flask-heroku, Flask-Login, Flask-SQLAlchemy, Flask-WTF, gunicorn, itsdangerous, Jinja2, MarkupSafe, psycopg2 binary, SQLAlchemy, Werkzeug, and WTForms
  
  After, all required softwares are installed; use the terminal and type in the following command: $python main.py
  
Sidenote current working features:
  1) Create an Account
  2) Login
  3) Logout
  4) Adding a note
  5) Viewing All Notes (filterable and searchable by individual note) 
  6) Viewing note by id
  7) Editing note
  8) Deletion of note

Test Cases
Test case can be found in highest level of the app folder: test_main.py. Test cases will run a series of commands to test the User and Note database. 
To run it use $pytest test_main.py in the terminal or click on the link below:

[![Build Status](https://travis-ci.org/Winternight5/Team4.svg?branch=master)](https://travis-ci.org/Winternight5/Team4)