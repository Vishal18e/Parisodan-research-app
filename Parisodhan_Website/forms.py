from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Parisodhan_Website.models import User

class Registration(FlaskForm):
    username=StringField(label='Username', validators=[DataRequired(), Length(min=2, max=20)])
    email=StringField(label='Email', validators=[DataRequired(), Email()])
    password=PasswordField(label='Password', validators=[DataRequired()])
    confirm_password=PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField(label='Sign Up')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Try a different Username.')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Try a different Email.')



class Login(FlaskForm):
    email=StringField(label='Email', validators=[DataRequired(), Email()])
    password=PasswordField(label='Password', validators=[DataRequired()])
    remember=BooleanField(label='Remember Me')
    submit=SubmitField(label='Sign In')
