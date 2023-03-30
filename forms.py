from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired




class LoginForm(FlaskForm):
    username = StringField(' Vartotojas  :  ', validators=[InputRequired()])
    password = PasswordField('Slaptažodis:', validators=[InputRequired()])



class RegistrationForm(FlaskForm):
    username = StringField(' Vartotojas  :  ', validators=[InputRequired()])
    password = PasswordField('Slaptažodis:', validators=[InputRequired()])