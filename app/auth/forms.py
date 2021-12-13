from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.core import Label
from wtforms.widgets import ColorInput
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

class RegisterForm(FlaskForm):
    name = StringField(label = 'Username', validators=[DataRequired(), Length(1,64)])
    email= StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    description = TextAreaField(label = 'Description', validators=[DataRequired(), Length(1,140)])
    profile_picture = FileField(label = 'Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    cover_photo = FileField(label = 'Cover Photo', validators=[FileAllowed(['jpg', 'png'])])
    profile_color = StringField(label = 'Profile color', widget=ColorInput(), default='#051318')
    submit = SubmitField(label='Sign up')

class LoginForm(FlaskForm):
    email= StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')