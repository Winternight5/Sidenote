.. SideNote documentation master file, created by
   sphinx-quickstart on Tue Dec  3 21:53:29 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

**SideNote Documentation**
====================================
The application’s main features will enable users to simply append tasks onto their to-do list. Users are able to create their own account, and persisting their notes/to-do lists upon login.

- *Required packages:*

 - python3
 - Flask 
 - Flask-Heroku
 - Flask-Login
 - Flask-SQLAlchemy
 - Flask-WTF
 - Gunicorn
 - Itsdangerous
 - Jinja2
 - MarkupSafe
 - psycoph2 binary
 - SQLAlchemy
 - Werkzeug
 - Sphinx

 - WTForms

Package installation(Linux):
``$ pip install (package name)``

SideNote Navigation
===================
This is an image of all the top level files in root level.

.. image:: topLevelNav32Font.png

- **main.py**       -   This file is what you will run to launch the application locally.
    - Use the command(Linux): ``$ python3 main.py``
- config.py     -   This file contains the Config class for database setup.
- test_main.py  -   This file contains the testing for Travis CI on github.
- app directory -   Contains the majority of the application's files.
- docs directory-   Contains all the documentation required for Sphinx.



This is an image of all the files below the root level.

.. image:: nav14Font.png

- **app directory** (Application's location)
    - events.py     -   For SocketIO implementation.
    - forms.py      -   For FlaskForms like login etc.
    - __init__.py   -   For creating the application.
    - models.py     -   Contains database table structure.
    - routes.py     -   Location for SideNote's logic.


**Files**
=========

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   modules
   tutorial
   functions

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
