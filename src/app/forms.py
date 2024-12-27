from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from src.app.models import User
from flask_login import current_user


class FormSignup(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=12)])
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max= 24)])
    password_confirmation = PasswordField('Password confirmation', validators=[DataRequired(), Length(min=6, max=24), EqualTo('password')])
    submit_button_signup = SubmitField('Create account')

    def validate_password(self, password):
        password = password.data
        special_characters = '!@#$%&?'
        letters = 'abcdefghijklmnopqrstuvwxyz'
        if any(i in letters for i in password) == False:
            raise ValidationError('Your password must contain a letter.')
        if any(char.isdigit() for char in password) == False:
            raise ValidationError('Your password must contain at least one number')
        elif any(i in special_characters for i in password) == False:
            raise ValidationError('Your password must contain at least one special character.')
        

    def validate_username(self, username):
        if ' ' in username.data:
            raise ValidationError('Your username cannot contain any spaces.')
        usern = User.query.filter_by(username=username.data).first()
        if usern:
            raise ValidationError('This username already exists.')

    def validate_email(self, email):
        userm = User.query.filter_by(email=email.data).first()
        if userm:
            raise ValidationError('E-mail already in use.')


class FormLogin(FlaskForm):
    account = StringField('Username', validators=[DataRequired(), Length(min= 4, max= 32)]) or EmailField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max= 24)])
    remember_data = BooleanField('Remember me')
    submit_button_login = SubmitField('Login')


class FormAddBrand(FlaskForm):
    brand_name = StringField('Brand', validators=[DataRequired(), Length(min=3, max=24)])

class FormAddCategory(FlaskForm):
    category_name = StringField('Category', validators=[DataRequired(), Length(min=3, max=24)])

class FormAddProduct(FlaskForm):
    product_name = StringField('Product', validators=[DataRequired(), Length(min=3, max=24)])
    product_price = FloatField('Price', validators=[DataRequired()])
    product_brand = SelectField('Brand', validators=[DataRequired()])
    product_category = SelectField('Category', validators=[DataRequired()])