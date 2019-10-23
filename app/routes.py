from flask import render_template, flash, redirect, url_for, request, jsonify, json
from app import app, db
from app.forms import LoginForm, RegistrationForm, ResetForm
from app.models import User, Post, AllPosts
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import random, string, html, re

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
#----- Theme & Styles
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/')
@app.route('/index')
@login_required
def index():
    global tags, currentTheme
    if current_user.is_authenticated:
        if current_user.settings is not None:
            currentTheme = current_user.settings
        else:
            current_user.settings = 'day'
        
    getposts = []
    for post in current_user.post:
        getposts.append(json.loads(post.body))
        
    #print(html.unescape(getposts[43]['body']))
    getposts.reverse()
    return render_template('index.html', theme=themes[currentTheme], allposts=getposts, tags=tags, title='Home')
#-------------------------------------------------------------------------------------------------------------------------
#----- Theme & Styles
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/changetheme', methods=['GET'])
def changetheme():
    global currentTheme
    currentTheme = 'dark' if current_user.settings == 'day' else 'day'
    current_user.settings = currentTheme
    db.session.commit()
    return redirect(url_for('index'))
#-------------------------------------------------------------------------------------------------------------------------
#----- Create / Modify / Delete Notes
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/newpost')
def newpost():
    return render_template('post.html', theme=themes[currentTheme], title='New Post') 
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/savepost', methods=['POST'])
def savepost():
    tags = request.form.get('tags')
    post = { 
        'title': request.form.get('title'),
        'icon': 'event_note',
        'tags': '' if tags is None else tags,
        'body': request.form.get('content')
    }
    print(request.form.get('tags'))
    
    newPost = Post()
    newPost.body = json.dumps(post)
    newPost.user_id = current_user.id
    #newPost.share = current_user
    
    try:
        db.session.add(newPost)
        db.session.commit()
    except Exception as e:
        print("\n FAILED entry: {}\n".format(json.dumps(newPost)))
        print(e)
        
    return redirect(url_for('index'))
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
			user = User(email=form.email.data, firstname=form.firstname.data, lastname=form.lastname.data)
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
def logout():
    logout_user()
    return redirect(url_for('index'))
#-------------------------------------------------------------------------------------------------------------------------
#----- Admin & skrunkworks stuff
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/db')
def showdb():
    Users = User.query.all()
    Posts = Post.query.order_by(Post.id.desc()).all()
    PostsAll = AllPosts.query.all()
    return render_template('result.html', Users=Users, Posts=Posts, AllPosts=PostsAll)
    
@app.route('/delid/<int:id>', methods=['GET'])
def delID(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return "id not found"
    else:
        db.session.delete(user)
        db.session.commit()
    data = User.query.all()
    return render_template('result.html', data=data)
        
@app.route('/delpost/<int:id>', methods=['GET'])
def delPostById(id):
    post = Post.query.filter_by(id=id).first()
    if post is None:
        return "id not found"
    else:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('showdb'))
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
def clearPosts():
    Post.query.delete()
    db.session.commit()
    return redirect(url_for('showdb'))
#-------------------------------------------------------------------------------------------------------------------------
@app.route('/db_addposts')
def addDB():
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
    'brush': themes[currentTheme]['btnBrush'],
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