from flask import render_template, request, flash, redirect, url_for
from src.app import app, users_database, bcrypt
from src.app.models import User
from src.app.forms import FormLogin, FormSignup
from flask_login import login_user, logout_user, login_required


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit() and 'submit_button_login' in request.form:
        user = User.query.filter_by(username=form_login.account.data).first()
        email = User.query.filter_by(email=form_login.account.data).first()
        par_next = request.args.get('next')
        if email and bcrypt.check_password_hash(email.password, form_login.password.data):
            login_user(email, remember=form_login.remember_data.data)
            flash(f'Welcome, {form_login.account.data}', 'alert-success')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        elif user and bcrypt.check_password_hash(user.password, form_login.password.data):
            login_user(user, remember=form_login.remember_data.data)
            flash(f'Welcome, {form_login.account.data}', 'alert-success')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Login failed. User or password incorrect.', 'alert-danger')
    
    return render_template('login.html', form_login=form_login)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form_signup = FormSignup()
    if form_signup.validate_on_submit() and 'submit_button_signup' in request.form:
        crypt_password = bcrypt.generate_password_hash(form_signup.password.data)
        user = User(username=form_signup.username.data, email=form_signup.email.data, password=crypt_password)
        users_database.session.add(user)
        users_database.session.commit()
        flash(f'Account created. You can log-in now as {form_signup.username.data} ({form_signup.email.data})', 'alert-success')
        return redirect(url_for('home'))
    return render_template('signup.html', form_signup=form_signup)

@app.route('/inventory', methods=['GET'])
@login_required
def inventory():
    return render_template('index.html')