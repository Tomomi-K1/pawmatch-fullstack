from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SelectField, IntegerField, RadioField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password =PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    password =PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class UserPreferenceForm(FlaskForm):
    pet_type = RadioField('Type of Pet')
    # breed = SelectField('Breed')
    size = RadioField('Size', choices=[('sm','small'), ('md','medium'), ('lg','large'), ('xlg','xlarge')])
    gender = RadioField('Gender',choices=[('m','male'), ('f','female'), ('u','unknown')])
    age = RadioField('Age', choices=[('baby','baby'), ('young','young'), ('adult','adult'), ('senior','senior')])
    good_with_children = BooleanField('Good with Children')
    house_trained = BooleanField('House trained')
    special_need = BooleanField('Special need')
    zipcode = IntegerField('Zipcode', validators=[DataRequired()])

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment')

