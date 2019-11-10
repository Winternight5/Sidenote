from flask import render_template, flash, redirect, url_for, request, jsonify, json, session
from app import app, db, events
from app.forms import LoginForm, RegistrationForm, ResetForm
from app.models import User, Post, shares
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import random, string, html, re, uuid

themes = {
    'day': {
        'browser':'#ffc400',
        'switch':'Dark Mode',
        'nav':'amber accent-3',
        'note':'amber lighten-4',
        'background':'yellow lighten-5',
        'button1':'amber lighten-2',
        'btnBrush':'green accent-4',
        'btnCheckbox':'light-blue darken-3',
        'btnNote':'orange accent-2',
        'indicator':'#ffc400',
        'indicatorActive':'#424242',
        'font':'black-text',
        'font_header':'black-text',
        'c1':'yellow lighten-3',
        'c2':'light-blue lighten-3',
        'c3':'red lighten-4',
        'warning':'red darken-4',
    },
    'dark': {
        'browser':'#212121',
        'switch':'Day Mode',
        'nav':'grey darken-4',
        'note':'grey darken-3',
        'background':'black',
        'button1':'indigo darken-2',
        'btnBrush':'green accent-4',
        'btnCheckbox':'light-blue darken-3',
        'btnNote':'orange accent-2',
        'indicator':'#424242',
        'indicatorActive':'#bdbdbd',
        'font':'grey-text text-lighten-2',
        'font_header':'grey-text text-lighten-5',
        'c1':'yellow lighten-3',
        'c2':'light-blue lighten-3',
        'c3':'red lighten-4',
        'warning':'red darken-4',
    }
}

currentTheme = 'day'

#-------------------------------------------------------------------------------------------------------------------------
#----- Index
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/')
@app.route('/index')
@login_required
def index():
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
#-------------------------------------------------------------------------------------------------------------------------
#----- Theme & Styles
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/changetheme', methods=['GET'])
@login_required
def changetheme():
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
    return render_template('todo.html', theme=themes[currentTheme], post=None, title='List') 
    
#-------------------------------------------------------------------------------------------------------------------------
#----- Create & Delete Notes / Modify all type of nodes
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/newnote')
@login_required
def newnote():
    return render_template('post.html', theme=themes[currentTheme], post=None, title='Note') 
    
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/savenote', methods=['POST'])
@login_required
def saveNewNote():  
    title = request.form.get('title')
    tags = request.form.get('tags')
    body = request.form.get('content')
    
    # generate new note array
    data = noteData(title, None, tags, body)
    newNote = Post()
    # convert noteData to json
    newNote.body = json.dumps(data)
    newNote.user_id = current_user.id
    #newNote.share = current_user
        
    saveToDB(newNote)
    
    return redirect(url_for('index'))
    
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/savenote/<int:id>', methods=['POST'])
@login_required
def saveNoteById(id):  
    idExists = db.session.query(Post.id).filter_by(id=id).scalar() is not None
    if idExists:
        title = request.form.get('title')
        tags = request.form.get('tags')
        body = request.form.get('content')
        
        owner = NoteOwner(id)
        
        # generate new note array
        data = noteData(title, None, tags, body)
        # get current note by ID (it's linked with current_user)
        currentPost = getNoteById(id, owner)
        
        # only allow owner to write or shared note with write access
        if owner or not owner and currentPost.writeAllowed:
            # convert noteData to json
            currentPost.body = json.dumps(data)
            
            saveToDB(currentPost)
            
    if owner:    
        return redirect(url_for('index'))
    else:
        return redirect(url_for('shared'))
#-------------------------------------------------------------------------------------------------------------------------
def noteData(title, bgcolor, tags, body, canvas = False):
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
    
#-------------------------------------------------------------------------------------------------------------------------
def saveToDB(note):
    try:
        db.session.add(note)
        db.session.commit()
    except Exception as e:
        print("\n FAILED entry: {}\n")
        print(e)

#-------------------------------------------------------------------------------------------------------------------------
@app.route('/editnote/<int:id>', methods=['GET'])
@login_required
def editnote(id):
    # return True or False
    # True = get from owner
    # False = get from sharing
    owner = NoteOwner(id)
    
    note = getNoteById(id, owner)
    
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
            
            # edit to do list
            if note.body['icon'] == 'event_available':
                pageUrl = 'todo.html'
                pageTitle = 'List'
                
            # edit to do list
            elif note.body['icon'] == 'brush':
                currentRoom = session['room'] = 'c'+str(id)
                
                if currentRoom not in events.datas:
                    events.datas[currentRoom] = json.loads(note.imgUrl) 
                pageUrl = 'canvas.html'
                pageTitle = 'Canvas'
                
            # edit note
            else:
                pageUrl = 'post.html'
                pageTitle = 'Note'
                
            return render_template(pageUrl, theme=themes[currentTheme], post=note, title=pageTitle, room=session.get('room')) 

    return redirect(url_for('index'))
#-------------------------------------------------------------------------------------------------------------------------
def NoteOwner(id):
    noteOwner = Post.query.filter_by(id=id, user_id=current_user.id).scalar() is not None

    return noteOwner
    
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/delnote/<int:id>', methods=['GET'])
@login_required
def delNoteById(id):
    post = getNoteById(id)
    if post is None:
        print("note not found or no access")
    else:
        db.session.delete(post)
        db.session.commit()
        
    return redirect(url_for('index'))
    
#-------------------------------------------------------------------------------------------------------------------------
def getNoteById(id, owner=True):
    note = None
    
    if owner:
        note = Post.query.filter_by(id=id, user_id=current_user.id).first()
                
    else:
        for eachNote in current_user.relations:
            if eachNote.id == id:
                note = eachNote
    
    return note
    
#-------------------------------------------------------------------------------------------------------------------------
#----- Handwriting/drawing Note
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/newCanvas')
@login_required
def newCanvas():
    session['room'] = str(current_user.email)
        
    return render_template('canvas.html', room=session['room'], theme=themes[currentTheme], post=None, title='Canvas')

#-------------------------------------------------------------------------------------------------------------------------
def saveCanvas(title, tags, thumbnail, JSONData):
    print('saving')
    if title is not None:
        data = noteData(title, None, tags, thumbnail, True)

        # generate new note array
        newNote = Post()
        # convert noteData to json
        newNote.body = json.dumps(data)
        newNote.imgUrl = json.dumps(JSONData)
        newNote.user_id = current_user.id
        saveToDB(newNote)
        return True
        
    return False
    
#-------------------------------------------------------------------------------------------------------------------------
def saveCanvasById(id, title, tags, thumbnail, JSONData):  
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
    global tags, currentTheme
    currentTheme = current_user.settings
        
    getposts = []
    for post in current_user.relations:
        post.body = json.loads(post.body)
        post.body.update(id=post.id)
        getposts.append(post.body)
        
    getposts.reverse()
    
    return render_template('index.html', theme=themes[currentTheme], allposts=getposts, tags=tags, title='Home')
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/share/<int:note_id>/<string:email>', methods=['GET'])
@login_required
def shareNoteById(note_id, email):
    
    note = getNoteById(note_id)
    
    if note:
        getUser = User.query.filter_by(email=email.lower()).first()
        if getUser:
            note.shareto.append(getUser)
            db.session.commit()
        
        print('Note is now shared')
        
    return redirect(url_for('index'))
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/writeAccess/<int:note_id>/<string:type>', methods=['GET'])
@login_required
def noteWriteAccess(note_id, type):
    
    note = getNoteById(note_id, True)
    if note:
        if type == 'true':
            note.writeAllowed = True
        else:
            note.writeAllowed = False

        db.session.commit()
        
    return ''
    
#-------------------------------------------------------------------------------------------------------------------------
#----- User login & Registation / Logout
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
	# if user logged in, go to main home page
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	# get post data of radio button 'login-option'
	option = request.form.get('login-option')
	form = LoginForm()

	# if radio is sign-in, autheticate user
	if (option == "sign-in"):
		print(form.email.data)
		print(form.email.data)
		print(form.email.data)
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
			user = User(email=form.email.data.lower(), firstname=form.firstname.data, lastname=form.lastname.data)
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
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
#-------------------------------------------------------------------------------------------------------------------------
#----- Admin & skrunkworks stuff
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/db')
@login_required
def showdb():
    if current_user.email == "admin":
        Users = User.query.all()
        Posts = Post.query.order_by(Post.id.desc()).all()
        Shares = [] #shares.query.all()
        for post in Posts:
            post.body = post.body[0:150]
            
        return render_template('result.html', Users=Users, Posts=Posts, shares=Shares)
    
    return redirect(url_for('index'))
#-------------------------------------------------------------------------------------------------------------------------
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
#-------------------------------------------------------------------------------------------------------------------------
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
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/db_init')
def fillCheck():
    user = User.query.first()
    if not user is None:
        return str(user.email)
    addadmin()
    return redirect(url_for('addadmin'))
    
def addadmin():
    admin = User(firstname='admin', lastname='sidenote', email='admin')
    admin.set_password('1234')
    try:
        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        return "FAILED entry: "+str(e)
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/db_clearposts')
@login_required
def clearPosts():
    if current_user.email == "admin":
        Post.query.delete()
        db.session.commit()
        return redirect(url_for('showdb'))
        
    return redirect(url_for('index'))
#-------------------------------------------------------------------------------------------------------------------------
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
                for i in range(random.randint(10,30))
            ],
        )
        db.session.commit()
    
        return redirect(url_for('showdb'))
        
    return redirect(url_for('index'))
#-------------------------------------------------------------------------------------------------------------------------
def genPosts():
    global icons
    rName = random_generator(8)
    rIcons = random.choice(list(icons.keys()))
    rTagn = random.randint(1,5)
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

tags = ['#Important','#Untagged','#school','#homework','#cmpe131','#python','#funstuff','#cs_stuff','#nothing','#html','#css','#js','#home','#ok']

def sing_sen_maker():
    s_nouns = ["A dude", "My mom", "The king", "Some guy", "A cat with rabies", "A sloth", "Your homie", "My gardener", "Superman"]
    p_nouns = ["These dudes", "Both of my moms", "All the kings of the world", "Some guys", "All of a cattery's cats", "The multitude of sloths living under your bed", "Your homies", "Like, these, like, all these people", "Supermen"]
    s_verbs = ["eats", "kicks", "gives", "treats", "meets with", "creates", "hacks", "configures", "spies on", "meows on", "flees from", "tries to automate", "explodes"]
    p_verbs = ["eat", "kick", "give", "treat", "meet with", "create", "hack", "configure", "spy on", "meow on", "flee from", "try to automate", "explode"]
    infinitives = ["to make a pie.", "for no apparent reason.", "because the sky is green.", "for fun.", "to make an babies.", "to know more about archeology."]
    '''Makes a random senctence from the different parts of speech. Uses a SINGULAR subject'''
    return listToString([random.choice(s_nouns), random.choice(s_verbs), random.choice(s_nouns).lower() or random.choice(p_nouns).lower(), random.choice(infinitives)])
    
def listToString(s, delimeter = ' '): 
    str1 = " " 
    return (delimeter.join(str(v) for v in s))
    
def random_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))