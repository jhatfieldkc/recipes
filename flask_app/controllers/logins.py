from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.login import Login
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():

    return render_template('/index.html')

@app.route('/user/create', methods = ['POST'])
def create_user():

    if not Login.validate_form(request.form):
        return redirect('/')

    user_id =Login.create_user(request.form)

    session['user_id'] = user_id
    session['email'] = request.form['email']
    session['first_name'] = request.form['first_name']

    return redirect('/recipes')

@app.route('/user/login', methods = ['POST'])
def login_user():

    users = Login.get_user_by_email(request.form)
    print(users)

    if len(users) != 1:
        flash("Incorrect Email.")
        return redirect('/')

    user = users[0]

    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash("Incorrect Password")
        return redirect('/')

    session['user_id'] = user['id']
    session['first_name'] = user['first_name']
    session['email'] = user['email']

    return redirect('/recipes')

@app.route('/logout')
def log_out():
    session.clear()
    return redirect('/')