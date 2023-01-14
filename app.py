from flask import Flask, redirect, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
import requests


from models import db, connect_db
from forms import Signup, Login, UserPreference, Comment
from config_info import API_KEY,API_SECRET, SECRET_KEY

# create the app
app = Flask(__name__)
# configure the postgresql database, relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///furmily_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.create_all()

app.config['SECRET_KEY'] = SECRET_KEY

def get_token():
    res = requests.post('https://api.petfinder.com/v2/oauth2/token', data={'grant_type':'client_credentials', 'client_id': API_KEY, 'client_secret': API_SECRET})
    data=res.json()
    return data['access_token']

ACCESS_TOKEN = get_token()

# ============ API call requirements ======================#
API_BASE_URL = 'https://api.petfinder.com/v2'
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage"""

    #===== show adoptable pet available, but need to think of way to count all available animals since API show only up to 100. 
    # res = requests.get(f'{API_BASE_URL}/animals', headers=headers, params={'status': 'adoptable'})
    # data=res.json()
    # num =len(data['animals'])
    return render_template('base.html')

@app.route("/signup")
def signup():
    """user signup page"""
    form = Signup()
    return render_template('signup.html', form=form)

@app.route("/login")
def login():
    """user login page"""
    form = Login()
    return render_template('login.html', form=form)



