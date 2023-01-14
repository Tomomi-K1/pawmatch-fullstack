from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length

class Signup(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password =PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    password =PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class UserPreference(FlaskForm):
    pet_type = SelectField('Type of Pet')
    breed = SelectField('Breed')
    size = SelectField('Size')
    gender = SelectField('Gender')
    age = SelectField('Age')
    good_with_children = BooleanField('Good with Children')
    house_trained = BooleanField('House trained')
    special_need = BooleanField('Special need')
    zipcode = IntegerField('Zipcode', validators=[DataRequired()])

class Comment(FlaskForm):
    comment = TextAreaField('Comment')

