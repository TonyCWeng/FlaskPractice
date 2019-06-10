from flask import render_template, url_for, flash, redirect
from blog import app, db, bcrypt
from blog.forms import RegistrationForm, LoginForm
from blog.models import User, Post

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
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been successfully created.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'Successfully logged in.', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login failed. Username and password do not match', 'danger')
    return render_template('login.html', title='Login', form=form)
