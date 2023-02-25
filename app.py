from flask import Flask, redirect, render_template, request, flash, redirect, session, g
import flask
import json
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests, random
from datetime import datetime
import threading
from flask_cors import CORS
import os

from models import db, connect_db, User, UserPreference, FavoritePet, MaybePet, FavoriteOrg, Comment
from forms import UserForm, LoginForm, UserPreferenceForm, CommentForm
from config_info import API_KEY,API_SECRET, SECRET_KEY

# create the app
app = Flask(__name__)
CORS(app)

# configure the postgresql database, relative to the app instance folder
# app.config['SECRET_KEY'] = SECRET_KEY
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', SECRET_KEY)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///furmily_db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql:///furmily_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
# ============ API call requirements ======================#
def get_token():
    res = requests.post('https://api.petfinder.com/v2/oauth2/token', data={'grant_type':'client_credentials', 'client_id': API_KEY, 'client_secret': API_SECRET})
    # ACCESS_TIME = datetime.now()
    data=res.json()
    # ACCESS_TOKEN = data['access_token']
    return data['access_token']

ACCESS_TOKEN = get_token()
print(ACCESS_TOKEN)

API_BASE_URL = 'https://api.petfinder.com/v2'
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# token expires in 3600, but this api does not provide refresh token. 
# I decied to call get_token function in each view function that requires API call so that we can avoid running into issue.
# but below are possible solutions

# from stackoverflow https://stackoverflow.com/questions/2697039/python-equivalent-of-setinterval

# def setInterval(func,time):
#     e = threading.Event()
#     while not e.wait(time):
#         func()

# setInterval(get_token,3600)
# option1 - maybe I can get datestamp when I get access token. Then if(ACCESS_TOKEN), check datetime to see if it's past 3600 seconds. if so, we need to get new token.
# option2 - petfinder API wrapper for login support :https://github.com/aschleg/petpy

# ==========================================================#

CURR_USER_KEY = 'curr_user'
pets_list= []
orgs_list = []

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

    form = UserForm()

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

        return redirect('/questions')

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
            return redirect("/questions")
        else:
            flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():

    do_logout()

    flash('You have logged out successfully', 'success')
    return redirect('/home')

@app.route('/users/profile/<int:user_id>', methods=['GET', 'POST'])
def show_edit_user(user_id):
    
    if not g.user or g.user.id != user_id:
        flash('Please log in')
        return redirect('/login')
    
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)

    if form.validate_on_submit():
        user.updateUser(form.username.data, form.email.data, form.password.data)

        db.session.commit()

        flash('Your Info was Successfully Updated!', 'success')

        return render_template('user_profile.html', form = form, user=user)
    
    return render_template('user_profile.html', form = form, user=user)

# ============================================================#
#========= End of User Signup & Login & Logout & User info update ===============#
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
    if g.user:
        return redirect('/questions')
    
    return render_template('home.html')

# ================ Show all Fav and maybe pet =================================
@app.route('/pets/users/<int:user_id>')
def user_page(user_id):
    """show user profile including preference, favorite pets, maybe pets saved"""
    
    ACCESS_TOKEN = get_token()
    print(f'view funcition uwer_page :{ACCESS_TOKEN}')

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/home")
    # do I need to put if g.user_id does not equal  to user_id?


    form=CommentForm()

    user = User.query.get_or_404(user_id)
    # userとFavoritepetの関係がModelで設定されていればもっと簡単にできるはず。
    fav_pets_id = [pet.pet_id for pet in FavoritePet.query.filter_by(user_id = g.user.id)]
    fav_pets =[]
    for pet_id in fav_pets_id:
        try:
            response = requests.get(f'{API_BASE_URL}/animals/{pet_id}', headers=headers)
            data = response.json()
            fav_pets.append(data['animal'])

        except KeyError:
            print(f'{pet_id} does not exit anymore')
            FavoritePet.query.filter_by(pet_id = pet_id).delete()
            db.session.commit()
        #  ここにTry and error でもしすでにPET IDが消えている場合の対応をする


    comments = Comment.query.filter_by(user_id = g.user.id)

       
    maybe_pets_id = [pet.pet_id for pet in MaybePet.query.filter_by(user_id = g.user.id)]
    maybe_pets =[]
    for pet_id in maybe_pets_id:
        try:
            response = requests.get(f'{API_BASE_URL}/animals/{pet_id}', headers=headers)
            data = response.json()
            maybe_pets.append(data['animal'])
        except KeyError:
            print(f'{pet_id} does not exit anymore')
            MaybePet.query.filter_by(pet_id = pet_id).delete()
            db.session.commit()
    # make api calls to get data for each pets and store that in dictionary
    # each rendered animal will have comments section, delete button    

    return render_template('users_pets.html', user=user, fav_pets=fav_pets, maybe_pets=maybe_pets, comments = comments, form=form)


#============= Get user's preference and show result ======================= 
@app.route('/questions', methods=["GET", "POST"])
def show_questions():

    ACCESS_TOKEN = get_token()
    print(f'view funcition show_questions :{ACCESS_TOKEN}')

    form = UserPreferenceForm()

    if form.validate_on_submit():
        # if user not logged in, how do I do this?
        
        user_pref = UserPreference(# raise
        user_id = g.user.id,
        pet_type = form.pet_type.data,
        size = form.size.data,
        gender = form.gender.data,
        age = form.age.data,
        # good_with_children = 'true' if form.good_with_children.data == True else 'false',
        # house_trained = 'true' if form.house_trained.data == True else 'false',
        # special_need = 'true' if form.special_need.data == True else 'false',
        zipcode = form.zipcode.data)

        
        db.session.add(user_pref)
        db.session.commit()

        response = requests.get(f'{API_BASE_URL}/animals', headers=headers, params={'type': user_pref.pet_type, 'size': user_pref.size, 'gender': user_pref.gender, 'age': user_pref.age, 'location': user_pref.zipcode, 'limit': 50, 'status': 'adoptable'})
        match_data = response.json()
        list_of_animals = match_data['animals']

          # ここでデータをSimplyfyしてpets_listにappendしたらどうか？
        #   この時にOrgIDからOrg NameとURLを取得しておく

        for animal in list_of_animals:
            if len(animal['photos']) ==0:
                list_of_animals.remove(animal)
        
        if len(list_of_animals) == 0 :
            flash('No Match Found. Please Try Again.', 'danger')
            return redirect('/questions')
        elif len(list_of_animals) > 10:
            list_of_animals= random.sample(list_of_animals, 10) # randomly choose 10 from the list and make new list
            return render_template('match_result.html', list_of_animals=list_of_animals)            
        
        return render_template('match_result.html', list_of_animals=list_of_animals)

    return render_template('questions.html', form=form)

# =============adding pets to Favorite or Maybe========================
@app.route('/likes', methods=['POST'])
def add_fav():
    received_data=request.get_json()
    print(f"received_data{received_data}")
    return_data = {
        'status':'success',
        'message': f'received:{received_data["animal"]}'

    }

    # =====this logic is not working why???========
    all_fav=FavoritePet.query.all()# get users fav pet, if aleady exist, don't add no action
    if FavoritePet.query.filter_by(pet_id=received_data['animal']) in all_fav:
        return_data = {
        'status':'already in database',
        'message': f'received:{received_data["animal"]}'
        }
        
        return flask.Response(response=json.dumps(return_data), status=201)
         
    else:

        # ここでpets_listの中からpetを探して、fav pet table に追加
        # for loop 内で FavoritePet(pet info) db.session.add(favpet)までいれる 
        # 追加する情報は？
        # pet_id
        # imgurl
        # pet_name
        # pet_description
        # location_city
        # location_state
        # organization_id
        # org name
        # org url 
        
        favPet = FavoritePet(
        pet_id = received_data['animal'],
        user_id = g.user.id)

        db.session.add(favPet)
        db.session.commit()

        return flask.Response(response=json.dumps(return_data), status=201)

@app.route('/maybe', methods=['POST'])
def add_maybe():
    received_data=request.get_json()
    print(f"received_data{received_data}")
    return_data = {
        'status':'success',
        'message': f'received:{received_data["animal"]}'
    }

    all_maybe=MaybePet.query.all()
    if MaybePet.query.filter_by(pet_id=received_data['animal']) in all_maybe:
        return_data = {
        'status':'already in database',
        'message': f'received:{received_data["animal"]}'
        }

        return flask.Response(response=json.dumps(return_data), status=201)

    maybePet = MaybePet(
    pet_id = received_data['animal'],
    user_id = g.user.id)

    db.session.add(maybePet)
    db.session.commit()

    return flask.Response(response=json.dumps(return_data), status=201)


# ============= DELETE user's favorite & maybe pet===========================
@app.route('/delete-fav', methods=['POST'])
def delete_fav():
    received_data=request.get_json()
    print(f"received_data{received_data}")
    return_data = {
        'status':'successfully deleted',
        'message': f'received:{received_data["animal"]}'
    }

    FavoritePet.query.filter_by(pet_id=received_data['animal']).delete()
    db.session.commit()

    return flask.Response(response=json.dumps(return_data), status=201)

@app.route('/delete-maybe', methods=['POST'])
def delete_maybe():
    received_data=request.get_json()
    print(f"received_data{received_data}")
    return_data = {
        'status':'successfully deleted',
        'message': f'received:{received_data["animal"]}'
    }

    MaybePet.query.filter_by(pet_id=received_data['animal']).delete()
    db.session.commit()

    return flask.Response(response=json.dumps(return_data), status=201)

# ================add user comments of a pet to DB ===========================
@app.route('/comments/<int:pet_id>', methods=['POST'])
def add_pet_comments(pet_id):
    received_data=request.get_json()
    print(f"received_data{received_data}")
    return_data = {
        'status':'successful',
        'message': f'received:pet_id {received_data["animal"]}, comment:{received_data["comment"]}'
    }

    comment = Comment(
        user_id=g.user.id,
        pet_id =pet_id,
        comment=received_data['comment']
    )

    db.session.add(comment)
    db.session.commit()

    return flask.Response(response=json.dumps(return_data), status=201)


# ==============org search ==============================
@app.route('/org-search', methods=['GET'])
def show_search_page():
    
    return render_template('org_search.html')

@app.route('/org-results', methods=['GET'])
def org_search_result():
    
    ACCESS_TOKEN = get_token()
    f'view funcition irg_search_result :{ACCESS_TOKEN}'
    orgs_list = []

    user_query = request.args.get('q')
    response = requests.get(f'{API_BASE_URL}/organizations', headers=headers, params={'query': user_query})
    data = response.json()
    orgs = data['organizations']
    print(f'user_query:{user_query} orgs:{orgs}')
    
    orgs_list =[{'id': org['id'], 'name': org['name'], 'phone': org['phone'], 'city': org['address']['city'], 'state': org['address']['state'], 'url': org['url'], 'img_url': org['photos'][0]['small'] if len(org['photos']) != 0 else "None" } for org in orgs]
    
    print(f'orgs_list:{orgs_list}')

    return render_template('org_results.html', user_query=user_query, orgs_list=orgs)
    
    