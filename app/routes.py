from flask import current_app as app
from flask import render_template, flash, redirect, url_for, request, jsonify, json, session
from . import db, events
from .forms import LoginForm, RegistrationForm, ResetForm
from .models import User, Post, Share
from flask_login import current_user, login_user, logout_user, login_required, login_manager
from werkzeug.urls import url_parse
import random, string, html, re, uuid
from sqlalchemy.orm import Session

themes = {
    'day': {
        'browser': '#ffc400',
        'switch': 'Dark Mode',
        'nav': 'amber accent-3',
        'note': 'amber',
        'themeMode': 'lighten-4',
        'background': 'amber lighten-5',
        'canvasBackground': 'amber lighten-5',
        'button1': 'amber lighten-2',
        'btnBrush': 'green accent-4',
        'btnCheckbox': 'light-blue darken-3',
        'btnNote': 'orange accent-2',
        'indicator': '#ffc400',
        'indicatorActive': '#424242',
        'font': 'black-text',
        'font_input': 'black-text',
        'font_header': 'black-text',
        'c1': 'yellow lighten-3',
        'c2': 'light-blue lighten-3',
        'c3': 'red lighten-4',
        'warning': 'red darken-4',
    },
    'dark': {
        'browser': '#212121',
        'switch': 'Day Mode',
        'nav': 'grey darken-4',
        'note': 'grey',
        'themeMode': 'darken-2',
        'background': 'black',
        'canvasBackground': 'grey darken-2',
        'button1': 'indigo darken-4',
        'btnBrush': 'green accent-4',
        'btnCheckbox': 'light-blue darken-3',
        'btnNote': 'orange accent-2',
        'indicator': '#424242',
        'indicatorActive': '#bdbdbd',
        'font': 'grey-text',
        'font_input': 'grey-text text-lighten-4',
        'font_header': 'grey-text text-lighten-1',
        'c1': 'yellow lighten-3',
        'c2': 'light-blue lighten-3',
        'c3': 'red lighten-4',
        'warning': 'red darken-4',
    }
}

currentTheme = 'day'

# -------------------------------------------------------------------------------------------------------------------------
#----- Index
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/')
@app.route('/index')
@login_required
def index():
    '''Main home page

    *login required*

    :return: Display all of user's notes
    '''
    global tags, currentTheme
    currentTheme = current_user.settings

    getposts = []
    for post in current_user.post:
        post.body = json.loads(post.body)
        post.body['body'] = post.body['body'].replace('chevron_right', '')
        post.body.update(id=post.id)
        getposts.append(post.body)

    getposts.reverse()
    return render_template('index.html', theme=themes[currentTheme], allposts=getposts, tags=tags, title='Home')
# -------------------------------------------------------------------------------------------------------------------------
#----- Theme & Styles
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/changetheme', methods=['GET'])
@login_required
def changetheme():
    '''Change theme

    *login required*

    :return: Allow the user to change from day to dark theme
    '''
    global currentTheme
    currentTheme = 'dark' if current_user.settings == 'day' else 'day'
    current_user.settings = currentTheme
    db.session.commit()

    return redirect(url_for('index'))
    
#-------------------------------------------------------------------------------------------------------------------------
#----- Create new To Do List
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/newlist')
@login_required
def newlist():
    '''New To Do List page

    *login required*
    '''
    return render_template('todo.html', theme=themes[currentTheme], post=None, title='List') 
    
#-------------------------------------------------------------------------------------------------------------------------
#----- Create & Delete Notes / Modify all type of nodes
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/newnote')
@login_required
def newnote():
    '''New Note page

    *login required*
    '''
    return render_template('note.html', theme=themes[currentTheme], post=None, title='Note')

# -------------------------------------------------------------------------------------------------------------------------
@app.route('/savenote', methods=['POST'])
@login_required
def saveNewNote():
    '''Save New Note

    *login required*

    :return: Get data from submitted form and create a new JSON to insert into database
    '''
    title = request.form.get('title')
    tags = request.form.get('tags')
    noteColor = request.form.get('noteColor')
    body = request.form.get('content')

    # generate new note array
    data = noteData(title, noteColor, tags, body)
    newNote = Post()
    # convert noteData to json
    newNote.body = json.dumps(data)
    newNote.user_id = current_user.id
    #newNote.share = current_user

    saveToDB(newNote)
    print("Note saved")
    return str(newNote.id)

    #return redirect(url_for('index'))

# -------------------------------------------------------------------------------------------------------------------------
@app.route('/savenote/<int:id>', methods=['POST'])
@login_required
def saveNoteById(id):
    '''Save a modified Note

    *login required*

    :return: Get data from submitted form and create a new JSON to insert into database
    '''
    idExists = db.session.query(Post.id).filter_by(id=id).scalar() is not None
    if idExists:
        title = request.form.get('title')
        tags = request.form.get('tags')
        noteColor = request.form.get('noteColor')
        body = request.form.get('content')

        owner = NoteOwner(id)

        # generate new note array
        data = noteData(title, noteColor, tags, body)
        # get current note by ID (it's linked with current_user)
        currentPost = getNoteById(id, owner)

        # only allow owner to write or shared note with write access
        if owner or not owner and currentPost.writeAllowed:
            # convert noteData to json
            currentPost.body = json.dumps(data)

            saveToDB(currentPost)
            print("Note saved")
            return str(currentPost.id)
            
    print("Error: Note not found or no access")
    return '0'
        
def noteData(title, bgcolor, tags, body, canvas = False):
    '''Note Data

    :return: Create a new Note data to later convert to JSON and insert into body
    '''
    icon = 'event_note'
    if "cbox" in body:
        icon = 'event_available'
    elif canvas:
        icon = 'brush'
    elif "<img src" in body:
        icon = 'image'

    post = {
        'title': '' if title is None else title,
        'icon': icon,
        'note_bgcolor': '' if bgcolor is None else bgcolor,
        'tags': '' if tags is None else tags,
        'body': '' if body is None else body
    }
    return post

# -------------------------------------------------------------------------------------------------------------------------
def saveToDB(note):
    '''Save To Database

    :return: Global Save Function to Database.
    '''
    try:
        db.session.add(note)
        db.session.commit()
    except Exception as e:
        print("\n FAILED entry: {}\n")
        print(e)

# -------------------------------------------------------------------------------------------------------------------------
@app.route('/editnote/<int:id>', methods=['GET'])
@login_required
def editnote(id):
    '''Edit Note page

    *login required*

    :return: Get note data by id, check note's owner and if note's is writable
    '''
    # return True or False
    # True = get from owner
    # False = get from sharing
    owner = NoteOwner(id)

    note = getNoteById(id, owner)
    
    currentRoom = None

    if note is not None:
        # if not owner and no write access, go to view page
        if not owner and not note.writeAllowed:
            note.body = note if note.body is None else note.body
            note.body = json.loads(note.body)
            note.owner = ''
            return render_template('view.html', theme=themes[currentTheme], post=note, title='View')

        # if owner or with write access go to edit page
        if note:
            note.body = note if note.body is None else note.body
            note.body = json.loads(note.body)
            note.owner = owner
            note.ownerEmail = note.user.email
            #note.shared = 

            # edit to do list
            if note.body['icon'] == 'event_available':
                pageUrl = 'todo.html'
                pageTitle = 'List'
                
            # edit canvas note
            elif note.body['icon'] == 'brush':
                currentRoom = session['room'] = 'c'+str(id)
                
                if currentRoom not in events.datas:
                    events.datas[currentRoom] = json.loads(note.imgUrl) 
                pageUrl = 'canvas.html'
                pageTitle = 'Canvas'
                
            # edit note
            else:
                pageUrl = 'note.html'
                pageTitle = 'Note'
                
            return render_template(pageUrl, theme=themes[currentTheme], post=note, title=pageTitle, room=currentRoom) 

    return redirect(url_for('index'))
#-------------------------------------------------------------------------------------------------------------------------
def NoteOwner(id):
    '''Note Owner

    :return: Get Note by id and verify it with curren_user.id to check the ownership
    :return: return None = not owner
    :return: return **data** = owner
    '''
    noteOwner = Post.query.filter_by(id=id, user_id=current_user.id).scalar() is not None

    return noteOwner
    
#-------------------------------------------------------------------------------------------------------------------------   
@app.route('/delnote/<int:id>', methods=['GET'])
@login_required
def delNoteById(id):
    '''Delete Note by id

    *login required*

    :return: Delete Note by id, use getNoteById() function to validate before deleting
    '''
    post = getNoteById(id)
    if post is None:
        print("note not found or no access")
    else:
        db.session.delete(post)
        db.session.commit()
        
    return redirect(url_for('index'))

# -------------------------------------------------------------------------------------------------------------------------
def getNoteById(id, owner=True):
    '''Get Note By Id

    :return: Get note data by id, check note's owner and or if note's is shared
    :return: return None = not owner
    :return: return **Data** = owner
    '''
    note = None

    if owner:
        note = Post.query.filter_by(id=id, user_id=current_user.id).first()
        
    else:
        shared = Share.query.filter_by(post_id=id, user_id=current_user.id).first()
        if shared is not None:
            note = Post.query.filter_by(id=shared.post_id).first()
    
    if note is not None:
        user = User()
        note.user
        note.collaborators = []
        for item in note.shareto:
            note.collaborators.append({'email': item.email, 'id': item.id})
            
    return note
    
#-------------------------------------------------------------------------------------------------------------------------
#----- Handwriting/drawing Note
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/newCanvas')
@login_required
def newCanvas():
    '''New Canvas page

    *login required*

    :return: Open an empty canvas page for handwriting feature
    '''
    session['room'] = str(current_user.email)
        
    return render_template('canvas.html', room=session['room'], theme=themes[currentTheme], post=None, title='Canvas')

#-------------------------------------------------------------------------------------------------------------------------
def saveCanvas(title, tags, thumbnail, JSONData):
    '''Save Canvas

    :return: Save canvas data to database
    '''
    if title is not None:
        data = noteData(title, None, tags, thumbnail, True)

        # generate new note array
        newNote = Post()
        # convert noteData to json
        newNote.body = json.dumps(data)
        newNote.imgUrl = json.dumps(JSONData)
        newNote.user_id = current_user.id
        saveToDB(newNote)
        print('saved')
        return True
        
    print('Did not save, title is empty')
    return False
    
#-------------------------------------------------------------------------------------------------------------------------
def saveCanvasById(id, title, tags, thumbnail, JSONData):  
    '''Save Canvas By Id


    :return: Save Modified Canvas data by id, user getNoteById() to validate
    '''
    idExists = db.session.query(Post.id).filter_by(id=id).scalar() is not None
    if idExists:
        owner = NoteOwner(id)
        
        # generate new note array
        data = noteData(title, None, tags, thumbnail, True)
        # get current note by ID (it's linked with current_user)
        currentPost = getNoteById(id, owner)
        
        # only allow owner to write or shared note with write access
        if owner or not owner and currentPost.writeAllowed:
            # convert noteData to json
            currentPost.body = json.dumps(data)
            currentPost.imgUrl = json.dumps(JSONData)
            
            saveToDB(currentPost)
            return True
            
    return False
    
#-------------------------------------------------------------------------------------------------------------------------
#----- Share Note
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/shared')
@login_required
def shared():
    '''Share Main Page

    *login required*

    :return: Get all Shared Notes
    '''
    global tags, currentTheme
    currentTheme = current_user.settings

    getposts = []
    for post in current_user.relations:
        post.body = json.loads(post.body)
        post.body.update(id=post.id)
        getposts.append(post.body)

    getposts.reverse()

    return render_template('index.html', theme=themes[currentTheme], allposts=getposts, tags=tags, title='Home')
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/share/<int:note_id>/<string:email>', methods=['GET'])
@login_required
def shareNoteById(note_id, email):
    '''Share Note By Id

    *login required*

    :return:  Using AJAX to get note data by id, and check note's owner. Then validate the provided email before insert into shares database.
    '''
    note = getNoteById(note_id)

    if note:
        getUser = User.query.filter_by(email=email.lower()).first()
        
        if getUser:
            memberExist = Share.query.filter_by(post_id=note_id, user_id=getUser.id).first() is not None
            
            if memberExist:
                print('Error: Member already added')
                return '1'
                
            note.shareto.append(getUser)
            db.session.commit()
        
            print('Note shared to new member')
            return json.dumps({'email': getUser.email, 'id': getUser.id})
    
    print("Error: Member not found or no access")
    return '0'
    
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/sharedel/<int:getPost_id>/<int:getUser_id>', methods=['GET'])
@login_required
def delMemberByNoteId(getPost_id, getUser_id):
    '''Delete Shared Member (Id) By Note Id

    *login required*

    :return: Get note data by id, and validate by checking note's owner, then delete column by id from shares database.
    '''
    owner = NoteOwner(getPost_id)
    member = None
    
    if owner:
        member = Share.query.filter_by(post_id=getPost_id, user_id=getUser_id).first()
    
    if member is not None:
        db.session.delete(member)
        db.session.commit()
        print("Deleted member access")
        return 'Deleted member'
    
    print("Error: Member not found or no access")
    return 'Denied'

# -------------------------------------------------------------------------------------------------------------------------
@app.route('/writeAccess/<int:note_id>/<string:type>', methods=['GET'])
@login_required
def noteWriteAccess(note_id, type):
    '''Write Access Modifier

    *login required*

    :return: Using AJAX to modify note's writeAllowed value from database. Use getNoteById() to validate.
    '''
    note = getNoteById(note_id, True)
    if note:
        if type == 'true':
            note.writeAllowed = True
        else:
            note.writeAllowed = False
            events.revokeAccess()

        db.session.commit()

    return ''

# -------------------------------------------------------------------------------------------------------------------------
# ----- User login & Registation / Logout
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Login Function

    :return:Get radio form "login-option" to route functions to Login, Logout or Registration


    sign-in
    +++++++

    :return: Get user's input email and password, then validate and authenticate the user.


    sign-up
    +++++++

    :return: Get user's filled form data, then validate and create a new user.


    reset-login
    +++++++++++

    :return: Get user's input email, then validate the email on file and send a reset password email to the user's email.
    '''
        # if user logged in, go to main home page
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # get post data of radio button 'login-option'
    option = request.form.get('login-option')
    form = LoginForm()
    form.login_message = ""

    # if radio is sign-in, autheticate user
    if (option == "sign-in"):
    
        # validate form
        if form.validate_on_submit():
            print('validating')
            # look at first result first()
            user = User.query.filter_by(email=form.email.data).first()

            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('index'))

            #login_user(user, remember=form.remember_me.data)
            login_user(user)

            # return to page before user got asked to login
            next_page = request.args.get('next')

            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')

            return redirect(next_page)

        print('unable to login')
        return render_template('welcome.html', form=form)

    # if sign-up validate registration form and create user
    elif (option == "sign-up"):
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(email=form.email.data.lower(
            ), firstname=form.firstname.data, lastname=form.lastname.data)
            user.set_password(form.password.data)
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                print("\n FAILED entry: {}\n".format(json.dumps(data)))
                print(e)
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        return render_template('welcome.html', form=form, loginOption=option)

    # reset-login
    elif (option == "reset-login"):
        form = ResetForm()
        flash('reset function not set yet')
        return render_template('welcome.html', form=form, loginOption=option)

    return render_template('welcome.html', form=form)
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/logout')
@login_required
def logout():
    '''Logout Function

    *login required*

    :return: Log the user out
    '''
    logout_user()
    return redirect(url_for('index'))
# -------------------------------------------------------------------------------------------------------------------------
# ----- Admin & skrunkworks stuff
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/db')
@login_required
def showdb():
    if current_user.email == "admin":
        Users = User.query.all()
        Posts = Post.query.order_by(Post.id.desc()).all()
        Shares = Share.query.all()
        for post in Posts:
            post.body = post.body[0:100]

        return render_template('result.html', Users=Users, Posts=Posts, shares=Shares)

    return redirect(url_for('index'))
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/delshareid/<int:id>', methods=['GET'])
@login_required
def delShareId(id):
    if current_user.email == "admin":
        shared = AllPosts.query.filter_by(id=id).first()
        if shared is None:
            return "id not found"
        else:
            db.session.delete(shared)
            db.session.commit()

        return redirect(url_for('showdb'))

    return redirect(url_for('index'))
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/delid/<int:id>', methods=['GET'])
@login_required
def delID(id):
    if current_user.email == "admin":
        user = User.query.filter_by(id=id).first()
        if user is None:
            return "id not found"
        else:
            db.session.delete(user)
            db.session.commit()

        return redirect(url_for('showdb'))

    return redirect(url_for('index'))
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/db_init')
def fillCheck():
    db.create_all()
    user = User.query.first()
    if user is not None:
        return str(user.email)
    addadmin()
    return redirect(url_for('showdb'))

def addadmin():
    admin = User(firstname='admin', lastname='sidenote', email='admin')
    admin.set_password('1234')
    
    user1 = User(firstname='tai', lastname='huynh', email='tai@mail.com')
    user1.set_password('1234')
    
    user2 = User(firstname='tai', lastname='huynh 2', email='tai2@mail.com')
    user2.set_password('1234')
    
    try:
        db.session.add(admin)
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
    except Exception as e:
        return "FAILED entry: "+str(e)
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/db_clearposts')
@login_required
def clearPosts():
    if current_user.email == "admin":
        Post.query.delete()
        db.session.commit()
        return redirect(url_for('showdb'))

    return redirect(url_for('index'))
# -------------------------------------------------------------------------------------------------------------------------
@app.route('/db_addposts')
@login_required
def addDB():
    if current_user.email == "admin":
        db.session.bulk_insert_mappings(
            Post,
            [
                dict(
                    body=genPosts(),
                    user_id=current_user.id
                )
                for i in range(random.randint(10, 30))
            ],
        )
        db.session.commit()

        return redirect(url_for('showdb'))

    return redirect(url_for('index'))
# -------------------------------------------------------------------------------------------------------------------------


def genPosts():
    global icons
    rName = random_generator(8)
    rIcons = random.choice(list(icons.keys()))
    rTagn = random.randint(1, 5)
    rTag = random.sample(tags, rTagn)
    post = {
        'title': rName,
        'icon': rIcons,
        'tags': listToString(rTag),
        'body': sing_sen_maker()+' '+sing_sen_maker()+' '+sing_sen_maker()
    }
    return json.dumps(post)


icons = {
    'image': themes[currentTheme]['btnBrush'],
    'event_available': themes[currentTheme]['btnCheckbox'],
    'event_note': themes[currentTheme]['btnNote']
}

tags = ['#Important', '#Untagged', '#school', '#homework', '#cmpe131', '#python',
        '#funstuff', '#cs_stuff', '#nothing', '#html', '#css', '#js', '#home', '#ok']


def sing_sen_maker():
    s_nouns = ["A dude", "My mom", "The king", "Some guy",
               "A cat with rabies", "A sloth", "Your homie", "My gardener", "Superman"]
    p_nouns = ["These dudes", "Both of my moms", "All the kings of the world", "Some guys", "All of a cattery's cats",
               "The multitude of sloths living under your bed", "Your homies", "Like, these, like, all these people", "Supermen"]
    s_verbs = ["eats", "kicks", "gives", "treats", "meets with", "creates", "hacks",
               "configures", "spies on", "meows on", "flees from", "tries to automate", "explodes"]
    p_verbs = ["eat", "kick", "give", "treat", "meet with", "create", "hack",
               "configure", "spy on", "meow on", "flee from", "try to automate", "explode"]
    infinitives = ["to make a pie.", "for no apparent reason.", "because the sky is green.",
                   "for fun.", "to make an babies.", "to know more about archeology."]
    '''Makes a random senctence from the different parts of speech. Uses a SINGULAR subject'''
    return listToString([random.choice(s_nouns), random.choice(s_verbs), random.choice(s_nouns).lower() or random.choice(p_nouns).lower(), random.choice(infinitives)])


def listToString(s, delimeter=' '):
    str1 = " "
    return (delimeter.join(str(v) for v in s))


def random_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))
