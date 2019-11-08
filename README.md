# Sidenote
### Notes and To-do List web application.

The application’s main features will enable users to simply append tasks onto their to-do list. Users are able to create their own account, and persisting their notes/to-do lists upon login. Using python language and database (SQLite / Postges SQL for heroku) as a backend to track user login data, which would permit user registration when an account does not already exist, and deny it when one does. Using HTML, Javascript (JQuery), and CSS (Bootstrap / MaterializeCSS) as front-end to make the user interface (UI) very elegant and appealing, implementing features such as customizable colorful backgrounds via a toggle menu on the page, etc.


## Getting Started

Make sure you have Python version 3.6 with pip installed on your computer to setup a localhost web server for development purpose.
More information can be found here:
[How do you set up a local testing server?]( https://developer.mozilla.org/en-US/docs/Learn/Common_questions/set_up_a_local_testing_server)

### Prerequisites

Python 3.6 with pip
  Required extensions: 
1.	Flask
2.	flask-heroku
3.	Flask-Login
4.	Flask-SQLAlchemy
5.	Flask-WTF
6.	Gunicorn
7.	Itsdangerous
8.	Jinja2
9.	MarkupSafe
10.	psycopg2 binary
11.	SQLAlchemy
12.	Werkzeug
13.	WTForms

### Installing

Clone this git repo then install the required extensions. 
To install individual extension, use the terminal: *(For Window, make sure to use “Run as administrator”)*
```
pip install Flask
```
For Mac:
```
pip3 install Flask
```
And repeat until all required extensions are installed.


## Running Test Cases

Test cases can be found in highest level of the app folder: test_main.py

### Test Cases Break down 

Test cases will run a series of commands to test the User and Note database.
One example:
```
test_new_user(new_user)
```
Testing insertion of new user into the User database

Another example:
```
 test_login(new_user)
```
Testing the login function to ensure authentication works using Flask-Login extension


## Deployment

This repo is built with Heroku extension and is ready for deployment. Please see Heroku official website for more information.
[GitHub Integration (Heroku GitHub Deploys)]( https://devcenter.heroku.com/articles/github-integration)


## Built With

* [Python](https://www.python.org/) - An interpreted, high-level, general-purpose programming language.
* [JQuery](https://www.jquery.com) - A fast, small, and feature-rich JavaScript library.
* [MaterializeCSS](https://materializecss.com/) - A modern responsive front-end framework based on Material Design
* [Bootstrap](https://getbootstrap.com) - Responsive, mobile-first projects on the web with the world's most popular front-end component library


## Authors

* **Tai Huynh** - *Initial work* - [Team4 - Sidenote]( https://github.com/Winternight5/Team4)
* **William Nguyen** - *Initial work* - [Team4 - Sidenote]( https://github.com/Winternight5/Team4)
* **Brian Tamsing** - *Initial work* - [Team4 - Sidenote]( https://github.com/Winternight5/Team4)
* **Nate Garza** - *Initial work* - [Team4 - Sidenote]( https://github.com/Winternight5/Team4)
See also the list of [contributors]( https://github.com/Winternight5/Team4/graphs/contributors)


## License

This project is licensed under the MIT License.
