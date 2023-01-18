from flask import Flask, redirect, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests

from models import db, connect_db, User, UserPreference, FavoritePet, MaybePet, FavoriteOrg, Comment
from forms import SignupForm, LoginForm, UserPreferenceForm, CommentForm
from config_info import API_KEY,API_SECRET, SECRET_KEY

# create the app
app = Flask(__name__)

# configure the postgresql database, relative to the app instance folder
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///furmily_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

# db.create_all()


# ============ API call requirements ======================#
def get_token():
    res = requests.post('https://api.petfinder.com/v2/oauth2/token', data={'grant_type':'client_credentials', 'client_id': API_KEY, 'client_secret': API_SECRET})
    data=res.json()
    return data['access_token']

ACCESS_TOKEN = get_token()
# option1 - maybe I can get datestamp when I get access token. Then if(ACCESS_TOKEN), check datetime to see if it's past 3600 seconds. if so, we need to get new token.

# option2 - petfinder API wrapper for login support :https://github.com/aschleg/petpy

API_BASE_URL = 'https://api.petfinder.com/v2'
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# ==========================================================#

CURR_USER_KEY = 'curr_user'

# ============================================================#
#=== signup/login/logout g.user & Session assign handling ====#
# ============================================================#
# this will run before every request."before_request" =Register a function to run before each request.
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
        # g is an object for storing data during the application context of a running Flask web app. By adding the user to g, we can use user info anywhere.

    else:
        g.user = None


def do_login(user):
    """Log in user."""
    # user is put in session
    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

# ============ Sing Up User  ======================#
@app.route('/signup', methods=["GET", "POST"])
def signup():
    """
    Handle user signup.Create new user and add to DB. Redirect to home page.If form not valid, present form. If the there already is a user with that username: flash message
    and re-present form.
    """
    # make sure no one is logged in before signup
    do_logout()

    form = SignupForm()

    if form.validate_on_submit():
        try:
            user =User.signup(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
            db.session.commit()
        
        except IntegrityError:
            flash("Username already taken", 'danger')

        do_login(user)

        return redirect('/home')

    else:
        return render_template('signup.html', form=form)

# ============ LOG IN User  ======================#
@app.route("/login", methods=["GET", "POST"])
def login():
    """user login page"""
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            username=form.username.data,
            password=form.password.data
        )

        if user:
            do_login(user)
            return redirect("/home")
        else:
            flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():

    do_logout()

    flash('You have logged out successfully', 'success')
    return redirect('/home')

# ============================================================#
#========= End of User Signup & Login & Logout ===============#
# ============================================================#


@app.route("/")
def root():
    """Homepage"""
    return redirect('/home')

@app.route('/home')
def home():
    #===== show adoptable pet available, but need to think of way to count all available animals since API show only up to 100. 
    # res = requests.get(f'{API_BASE_URL}/animals', headers=headers, params={'status': 'adoptable'})
    # data=res.json()
    # num =len(data['animals'])
    return render_template('home.html')


@app.route('/users/<int:user_id>')
def user_page(user_id):
    """show user profile including preference, favorite pets, maybe pets saved"""

    user = User.query.get_or_404(user_id)

    return render_template('user_profile.html', user=user)

@app.route('/questions', methods=["GET", "POST"])
def show_questions():

    form = UserPreferenceForm()

    res = requests.get(f'{API_BASE_URL}/types', headers=headers)
    data = res.json()
    pet_types =[(item['name'], item['name']) for item in data['types']]
    form.pet_type.choices = pet_types

    if form.validate_on_submit():
        # if user not logged in, how do I do this?
        pet_type = form.pet_type.data
        size = form.size.data
        gender = form.gender.data
        age = form.age.data
        good_with_children = form.good_with_children.data
        house_trained = form.house_trained.data
        special_need = form.special_need.data
        zipcode = form.zipcode.data
    

        response = requests.get(f'{API_BASE_URL}/types', headers=headers, params={'type': pet_type, 'size': size, 'gender': gender, 'age': age, 'good_with_children': good_with_children, 'house_trained':house_trained, 'special_needs':special_need, 'zipcode': zipcode})
        data = response.json()
        raise

    #     return render_template('/your_matches.html' )

    return render_template('questions.html', form=form)

    """show questions to get users preference"""





