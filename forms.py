from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms import validators
from wtforms.fields.simple import TextAreaField
from wtforms.validators import InputRequired


class RegisterUserForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()])
    email = EmailField('Email', validators = [InputRequired()])
    first_name = StringField('First Name', validators = [InputRequired()])
    last_name = StringField('Last Name', validators = [InputRequired()])

class LoginUserForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()])

class UserFeedback(FlaskForm):
    title = StringField('Title', validators = [InputRequired()])
    content = TextAreaField('Content', validators = [InputRequired()])