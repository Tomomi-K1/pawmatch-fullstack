from flask import Flask, redirect, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension


from models import db, connect_db
from config_info import ACCESS_TOKEN, SECRET_KEY

# create the app
app = Flask(__name__)
# configure the postgresql database, relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///furmily_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = SECRET_KEY

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage"""
 

    return render_template('base.html')

