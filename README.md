[![Build Status](https://travis-ci.org/Winternight5/Sidenote.svg?branch=master)](https://travis-ci.org/Winternight5/Sidenote)

# Sidenote
### Notes and To-do List web application.

The application’s main features will enable users to simply append tasks onto their to-do list. Users are able to create their own account, and persisting their notes/to-do lists upon login. Using python language and database (SQLite / Postges SQL for heroku) as a backend to track user login data, which would permit user registration when an account does not already exist, and deny it when one does. Using HTML, Javascript (JQuery), and CSS (Bootstrap / MaterializeCSS) as front-end to make the user interface (UI) very elegant and appealing, implementing features such as customizable colorful backgrounds via a toggle menu on the page, etc.


[Live Demo - http://sidenotex.herokuapp.com/](http://sidenotex.herokuapp.com/)


## Getting Started

Make sure you have Python version 3.6 with pip installed on your computer to setup a localhost web server for development purpose.

More information can be found here:

[How do you set up a local testing server?]( https://developer.mozilla.org/en-US/docs/Learn/Common_questions/set_up_a_local_testing_server)

### Prerequisites

Python 3.6 with pip

Required packages: 
1.	Flask
2.	Flask-Heroku
3.	Flask-Login
4.	Flask-SQLAlchemy
5.	Flask-WTF
6.	Gunicorn (only required on Heroku)
7.	psycopg2 binary (only required on Heroku)
8.	SQLAlchemy
9. ...

See the most updated complete list [requirements.txt](https://github.com/Winternight5/Team4/blob/master/requirements.txt)

### Installation

Clone this git repo then install the required packages. 

To install individual package, use the terminal: *(For Window, make sure to “Run as administrator”)*

```
pip install Flask
```
For Mac:
```
pip3 install Flask
```
All packages listed in the requirements text file are required to run the application.


## Running Test Cases

Test cases can be found in the following folder: [Sidenote/app/tests/](https://github.com/Winternight5/Sidenote/tree/master/app/tests)

### Test Cases Break down 

#### conftest.py

Contains the pytest configuration and fixtures of app_context, client, and databases.


#### test_auth.py

##### Testing of server availability
The first step is to test and check if the server is up and running:
```
test_login(client)
``` 
This test simply check the server response status code. If the server is up and running, it will returns HTTP 200 OK success status response code.

##### Testing of databases
The following test to ensure various python functions and database works properly, we uses pytest for back-end testing.

Testing database availability by using the following functions:
```
test_add_user_to_db(db)
``` 
```
test_valid_register(db)
```
```
test_verify_user_exists(db)
```
```
test_theme(db)
```
This is checking the schema of the User database by insertion of a new user. Then, validate and verifies if the database session and data integrity was successfully committed.


Additional database verification and validity of Post db: by insertion of a new note:
```
 test_new_note(db)
```

##### Testing of functions

Testing data integrity of a note object: 
```
test_noteData()
```
This is needed to ensure the note object data integrity is valid. Later on, this object is converted to JSON string to allows saving of data into the database.


An example of function testing:
```
test_listToString()
```

## Deployment

This repo is built with Heroku package and is ready for deployment. Please see Heroku official website for more information.
[GitHub Integration (Heroku GitHub Deploys)]( https://devcenter.heroku.com/articles/github-integration)


## Documentation
For more information regarding how to navigate or code implementation please go to Sphinx Documentation.

```
[Sidenote/docs/_build/html/](https://github.com/Winternight5/Sidenote/tree/master/docs/_build/html)
```


## Built With

* [Python](https://www.python.org/) - An interpreted, high-level, general-purpose programming language.
* [JQuery](https://www.jquery.com) - A fast, small, and feature-rich JavaScript library.
* [MaterializeCSS](https://materializecss.com/) - A modern responsive front-end framework based on Material Design.
* [Bootstrap](https://getbootstrap.com) - Responsive, mobile-first projects on the web with the world's most popular front-end component library.


## Authors, *Initial work*

* **Tai Huynh** - *Project Manager* - [Team4 - Sidenote]( https://github.com/Winternight5/Team4)
* **William Nguyen** - *Frontend Engineer* - [Team4 - Sidenote]( https://github.com/Winternight5/Team4)
* **Brian Tamsing** - *UI/UX Engineer* - [Team4 - Sidenote]( https://github.com/Winternight5/Team4)
* **Nate Garza** - *Devops/Infrastucture Engineer* - [Team4 - Sidenote]( https://github.com/Winternight5/Team4)

List of [contributors]( https://github.com/Winternight5/Team4/graphs/contributors)


## License

This project is licensed under the MIT License.
