from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL

class AddNewCafe(FlaskForm):
  name = StringField("Cafe Name", validators=[DataRequired()])
  map_url = StringField("Map URL", validators=[DataRequired(), URL()])
  img_url = StringField("Image URL", validators=[DataRequired(), URL()])
  location = StringField("Location", validators=[DataRequired()])
  seats = StringField("Seats", validators=[DataRequired()])
  has_toilet = SelectField("Has Toilet?", choices=["Yes", "No"], validators=[DataRequired()])
  has_wifi = SelectField("Has Wifi?", choices=["Yes", "No"], validators=[DataRequired()])
  has_sockets = SelectField("Has Sockets?", choices=["Yes", "No"], validators=[DataRequired()])
  can_take_calls = SelectField("Can Take Calls?", choices=["Yes", "No"], validators=[DataRequired()])
  coffee_price = StringField("Coffee Price", validators=[DataRequired()])
  submit = SubmitField("Submit")