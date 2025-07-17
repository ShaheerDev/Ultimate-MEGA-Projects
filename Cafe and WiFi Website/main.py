from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Boolean
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import DataRequired, Email, Length, URL, InputRequired
from forms import AddNewCafe

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Your Secret Key'

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'Your DataBase URL'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    all_cafes = db.session.query(Cafe).all()
    return render_template("index.html", cafes=all_cafes)

@app.route("/add-cafe", methods=["GET", "POST"])
def add_cafe():
    form = AddNewCafe()
    if form.validate_on_submit():
        def to_bool(value):
            return value.lower() == "yes"
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            seats=form.seats.data,
            has_toilet=to_bool(form.has_toilet.data),
            has_wifi=to_bool(form.has_wifi.data),
            has_sockets=to_bool(form.has_sockets.data),
            can_take_calls=to_bool(form.can_take_calls.data),
            coffee_price=form.coffee_price.data

        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_cafe.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
