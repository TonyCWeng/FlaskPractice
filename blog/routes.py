from flask import render_template, url_for, flash, redirect, request
from blog import app, db, bcrypt
from blog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from blog.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required

posts = [
    {
        'author': 'Corey House',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'May 29, 2019'
    },
    {
        'author': 'Jane House',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'May 29, 2019'
    }
]


@app.route('/')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been successfully created.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Check if such a user exists, then check that the passwords match
        if user is None or not bcrypt.check_password_hash(user.password, form.password.data):
            flash(f'Login failed. Username and password do not match', 'danger')
            return render_template('login.html', title='Login', form=form)
        flash('Successfully logged in.', 'success')
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out.', 'success')
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account information has been successfully updated.', 'success')
        # Post/Redirect/Get Pattern. Basically, after successfully posting a request,
        # refreshing the page would cause a resubmission of the same successful
        # post request unless we finish our submission with a redirect to a get request.
        return redirect(url_for('account'))
    image_file = url_for('static', filename=f'profile_images/{current_user.image_file}' )
    return render_template('account.html', title='My Account', 
                            image_file=image_file, 
                            form=form)