from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class WorkoutForm(FlaskForm):
    title = StringField('Workout Title', validators=[DataRequired()])
    workInterval = RadioField('Set Interval', choices=[(15,'15 seconds'), (30,'30 seconds'), (45,'45 seconds'), (60,'60 seconds')], default=15, coerce=int, validators=[DataRequired()])
    restInterval = RadioField('Rest Interval', choices=[(10,'10 seconds'), (15,'15 seconds'), (20,'20 seconds'), (25,'25 seconds')], default=10, coerce=int, validators=[DataRequired()])
    workoutBlock = TextAreaField('Workouts (Each on seperate line)', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ProgressForm(FlaskForm):
    date = StringField('Title or Date', validators=[DataRequired()])
    report = TextAreaField('Progress Entry (Reflect on your growth!)', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(name=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
