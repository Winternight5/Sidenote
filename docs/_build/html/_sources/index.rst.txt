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

- **app**
    - events.py     -   For SocketIO implementation.
    - forms.py      -   For FlaskForms like login etc.
    - __init__.py   -   For creating the application.
    - models.py     -   Contains database table structure.
    - routes.py     -   Location for SideNote's logic.


Using SideNote
==============

*Login Page*

.. image:: loginPage.png
Existing users can input information here to sign in to view their notes and new users can enter in their information under the Sign In tab.

*Clean User Page* (Dark Theme setting on)

.. image:: newUserPage.png
After registering new users will be taken to this page. There are buttons near the top which list their purpose when hovered over.
They include: Settings, New Canvas, New To-Do List and New Note.

*Making New Canvas Page*

.. image:: makingNewNote.png
This is what will display when user types New Canvas button on User Page.
The user can write freehand on the page, upload a picture, reset the page or make the screen fullpage.
One of the features is Save which will keep the canvas and display it on User page. Once Save is clicked user will be prompt with naming and giving a hash to the item. 

*Updated User Page*

.. image:: afterSavingNewNote.png
This canvas was named "First note" and given the hashtag First. Now that I have a Canvas created I can share it with other people or edit it later.

**Files**
=========

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
