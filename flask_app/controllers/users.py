from flask import Flask, render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
import re 

bcrypt = Bcrypt(app)


# DISPLAY ROUTES
# _________________________________________________________________________________________________

# LOGIN REG PAGE___________________________________________________________________________________
@app.route('/')
def user():
    if 'user_id' in session:
            return redirect('/dashboard')
    print('displaying home page')
    return render_template("login_reg.html")






# ACTION ROUTES
# ________________________________________________________________________________________________

# REGISTER USER TO DB_____________________________________________________________________________
@app.route('/create_user', methods=['POST'])
def create_user():
    print('send to validation then use save model')
    if not User.validate_info(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data= {
    'first_name' : request.form['first_name'],
    'last_name' : request.form['last_name'],
    'email' : request.form['email'],
    'password' : pw_hash,
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

# LET USER LOGIN_________________________________________________________________________________
@app.route('/login' , methods = ['POST'])
def login():
    data= {
    'email' : request.form['email'],
    }

    print('ran query to grab info based on email')
    if not User.validate_login(request.form):
        flash("Invalid Email/Password")
        return redirect("/")
    user = User.get_by_email(data)
    if not user:
        return redirect ('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

# CLEAR SESSION LOG OUT__________________________________________________________________________
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')


