from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, URLField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")

class CreateItemForm(FlaskForm):
    name = StringField("Item Name", validators=[DataRequired()])
    description = CKEditorField("Item Description", validators=[DataRequired()])
    price = IntegerField("Item Price", validators=[DataRequired()])
    image_url = URLField("Picture URL", validators=[DataRequired()])
    about = CKEditorField("Item About", validators=[DataRequired()])
    submit = SubmitField("Submit")

class CommentForm(FlaskForm):
    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")

