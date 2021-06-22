from app import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request
from forms import RegistrationForm, LoginForm
from models import User
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def home():
    return render_template('home.html', title='Home')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has just created!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Log in successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('profile'))
    return render_template('login.html', title='Login', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    flash('You have just logged out!', 'success')
    return redirect(url_for('home'))


@app.route('/profile/')
@login_required
def profile():
    return render_template("profile.html")
