from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class RegisterForm(FlaskForm):
    name = StringField(label = 'Username', validators=[DataRequired(), Length(1,64)])
    email= StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    cover_photo = FileField('Cover Photo', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField(label='Registrar')

class LoginForm(FlaskForm):
    email= StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Iniciar sesión')