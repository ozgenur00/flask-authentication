from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from flask_wtf import FlaskForm



class LoginForm(FlaskForm):
    """Login form"""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)],)
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=20)],)


class RegisterForm(FlaskForm):
    """User registration form"""

    username = StringField("Username", validators=[InputRequired(), Length(min=2, max=20)],)
    password = StringField("Password", validators=[InputRequired(), Length(min=8, max=20)],)
    email = StringField("Email", validators=[InputRequired(), Length(max=50)],)
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)],)
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)],)


class FeedbackForm(FlaskForm):
    """adding Feedback form"""

    title = StringField("Title", validators=[InputRequired(), Length(max=50)],)
    content = StringField("Content", validators=[InputRequired()],)

class DeleteForm(FlaskForm):
    """Delete form"""