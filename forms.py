from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SelectField, IntegerField, RadioField
from wtforms.validators import DataRequired, Email, Length

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password =PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    password =PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class UserPreferenceForm(FlaskForm):
    pet_type = RadioField('Type of Pet', choices=[ ("Dog", "Dog"), ("Cat","Cat"), ("Rabbit", "Rabbit"), ("Small & Furry","Small & Furry"), ("Horse", "Horse"), ("Bird", "Bird"), ("Scales, Fins & Other", "Scales, Fins & Other"), ("Barnyard","Barnyard")])
    # breed = SelectField('Breed')
    size = RadioField('Size', choices=[('small','small'), ('medium','medium'), ('large','large'), ('xlarge','xlarge')])
    gender = RadioField('Gender',choices=[('male','male'), ('female','female'), ('unknown','unknown')])
    age = RadioField('Age', choices=[('baby','baby'), ('young','young'), ('adult','adult'), ('senior','senior')])
    # good_with_children = BooleanField('Good with Children', default =False)
    # house_trained = BooleanField('House trained', default =False)
    # special_need = BooleanField('Special need', default =False)
    zipcode = IntegerField('Zipcode', validators=[DataRequired()])

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])

