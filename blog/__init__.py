from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asfdhafhjo123123as'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# redirects non-logged in user to the login page, should they attempt to access
# a protected route.
login_manager.login_view = 'login'
# change message class to info, a bootstrap class, to give it some bootstrap styling.
login_manager.login_message_category = 'info'

# Our routes.py already imports app from this file, so in order to
# prevent circular imports, we must import from blog after the app lines above.
from blog import routes