app directory
=============

app.__init__ module
-------------------

**def create_app(debug=False, test_config=None)** - Creates an application. :return: app

app.events module
-----------------

**def getKeys** - returns list of keys.

**def getValues** - return list of the values.

**def checkDatas** - Verfies if current room is stable.

**def clearDatas** - Takes currentRoom paramater; Deletes the room data.

**def join(data)** - Takes data parameter for new user. Adds user to the room array.

**def disconnect** - Remove the user from the room array.

**def drawing(data)** - Save current user drawing data into memory and emit data to all users in the room.

**def fill(data)** - Save current user fill data into memory and emit data to all users in the room.

**def loadImg(data)** - Save current user image data into memory and emit data to all users in the room.

**def new(data)** - Clear memory and emit to all users.

**def save(newdata)** - Save current user canvas data into database. Returns "Canvas Saved" output.

**def revokeAccess** - Init and emit revoke access to all current active shared users.

**def img** - Get image data.

app.forms module
----------------

.. automodule:: app.forms
    :members:
    :undoc-members:
    :show-inheritance:

app.models module
-----------------

.. automodule:: app.models
    :members:
    :undoc-members:
    :show-inheritance:

app.routes module
-----------------

This file is responsible for the applications backend pathing. Login is required for most features.

*Themes* - Settings for night and day theme settings.

**def index** - Main home page :return: Display all of user's notes.

**def changetheme** - Change theme. :return: Allow the user to change from day to dark theme.

**def newList** - New To Do List page. 

**def newnote** - New notes page. 

**def saveNewNote** - Saves new note. :return: Get data from submitted form and create a new JSON to insert into database.

**saveNoteById(id)** - Saves a modified note. :return: Get data from submitted form and create a new JSON to insert into database.

**noteData(title, bgcolor, tags, body, canvas = False)** - :return: Create a new Note data to later convert to JSON and insert into body.

**saveToDB(note)** - :return: Global Save Function to Database.

**editnote(id)** - :return: Get note data by id, check note's owner and if note's is writable

**def NoteOwner** -

    :return: Get Note by id and verify it with curren_user.id to check the ownership

    :return: return None = not owner

    :return: return **data** = owner

**def delNoteById(id)** - :return: Delete Note by id, use getNoteById() function to validate before deleting

**def getNoteById(id, owner=True)** -     
    :return: Get note data by id, check note's owner and or if note's is shared

    :return: return None = not owner

    :return: return **Data** = owner

**def newCanvas()** - :return: Open an empty canvas page for handwriting feature

**def saveCanvas(title, tags, thumbnail, JSONData)** - :return: Save canvas data to database

**def saveCanvasById(id, title, tags, thumbnail, JSONData)** - :return: Save Modified Canvas data by id, user getNoteById() to validate

**def shared()** - :return: Get all Shared Notes

**def shareNoteById(note_id, email)** - :return:  Using AJAX to get note data by id, and check note's owner. Then validate the provided email before insert into shares database.

**def delMemberByNoteId(getPost_id, getUser_id)** - :return: Get note data by id, and validate by checking note's owner, then delete column by id from shares database.

**def noteWriteAccess(note_id, type)** - :return: Using AJAX to modify note's writeAllowed value from database. Use getNoteById() to validate.

**def login()** - Login Function

    :return:Get radio form "login-option" to route functions to Login, Logout or Registration

    sign-in - :return: Get user's input email and password, then validate and authenticate the user.


    sign-up - :return: Get user's filled form data, then validate and create a new user.


    reset-login - :return: Get user's input email, then validate the email on file and send a reset password email to the user's email.

**def logout()** - :return: Log the user out

**def showdb()** - :return: result html

**def delShareId(id)** - Admin function.

    :return: showdb

    :return: index

**def delID(id)** - Admin function.

    :return: showdb

    :return: index

**def fillCheck()** - Admin funtion.

**def addadmin()** - Admin function. Hardcodes admins to database.

**def clearPosts()** - Admin function.

**def addDB()** - Admin function.

**def genPosts()** - Admin function. *Randomly generates post for demo*

**def sing_sen_maker()** - Admin function. *For def genPosts*

**def listToString(s, delimeter=' ')** - Admin function. *For def genPosts*

**def random_generator(size=4, chars=string.ascii_uppercase + string.digits)** - Admin function. *For def genPosts*





.. automodule:: app.routes
    :members:
    :undoc-members:
    :show-inheritance:


