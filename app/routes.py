from flask import render_template, flash, redirect, url_for, request, jsonify, json
from app import app, db
from app.forms import LoginForm, RegistrationForm, ResetForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

		
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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user')
def usersDB():
    data = User.query.all()
    return render_template('result.html', data=data)
    
@app.route('/delid')
def delID():
    id = request.args.get('id')
    user = User.query.filter_by(id=id).first()
    if user is None:
        return "id not found"
    else:
        db.session.delete(user)
        db.session.commit()
    data = User.query.all()
    return render_template('result.html', data=data)
    
@app.route('/add')
def addDB():
    admin = User(firstname='admin', lastname='sidenotes', email='admin@example.com')
    admin.set_password('1234')
    try:
        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        return "FAILED entry: "+str(e)
    return "admin created";