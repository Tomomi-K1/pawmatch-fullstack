from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password =PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    password =PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class UserPreferenceForm(FlaskForm):
    pet_type = SelectField('Type of Pet', choices=[ ("Dog", "Dog"), ("Cat","Cat"), ("Rabbit", "Rabbit"), ("Bird", "Bird"), ("Small & Furry","Small & Furry")])
    size = SelectField('Size', choices=[('small','Small'), ('medium','Medium'), ('large','Large'), ('xlarge','XLarge')])
    gender = SelectField('Gender',choices=[('male','Male'), ('female','Female')])
    age = SelectField('Age', choices=[('baby','Baby'), ('young','Young'), ('adult','Adult'), ('senior','Senior')])
    zipcode = IntegerField('Zipcode', validators=[DataRequired()])

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])

