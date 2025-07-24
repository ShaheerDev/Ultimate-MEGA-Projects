import os

from flask import Flask, abort, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Boolean
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from functools import wraps
from forms import RegisterForm, LoginForm, CreateItemForm, CommentForm
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import stripe
import smtplib

load_dotenv()

stripe.api_key = os.environ.get('API_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
ckeditor = CKEditor(app)
Bootstrap5(app)

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

class Products(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=False, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    image_url: Mapped[str] = mapped_column(String(600), nullable=False)
    about: Mapped[str] = mapped_column(String(700), nullable=False)
    comments = relationship("Comment", back_populates="product")

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    comments = relationship("Comment", back_populates="comment_author")

class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    product_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("products.id"))
    product = relationship("Products", back_populates="comments")

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 2:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    query = request.args.get('q')
    if query:
        items = Products.query.filter(
            (Products.name.ilike(f"%{query}%")) |
            (Products.about.ilike(f"%{query}%")) |
            (Products.description.ilike(f"%{query}%"))
        ).all()
    else:
        items = Products.query.all()
    return render_template("index.html", items=items, search_query=query)

@app.route("/buy/<int:item_id>", methods=["GET", "POST"])
def buy(item_id):
    product = db.session.get(Products, item_id)
    print(f"Looking for item with ID: {item_id}")
    print(f"Found: {product}")
    if not product:
        abort(404)

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))

        new_comment = Comment(
            text=comment_form.comment_text.data,
            comment_author=current_user,
            product=product
        )

        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("buy", item_id=item_id))
    return render_template("buy.html", product=product, form=comment_form)

@app.route("/add-to-cart/<int:item_id>", methods=["GET", "POST"])
def add_to_cart(item_id):
    if 'cart' not in session:
        session["cart"] = []
    session["cart"].append(item_id)
    session.modified = True
    return redirect(url_for('home'))

@app.route("/cart")
def cart():
    cart = session.get('cart', [])
    cart_items = Products.query.filter(Products.id.in_(cart)).all()
    total_price = sum(item.price for item in cart_items)
    return render_template("cart.html", items=cart_items, total=total_price)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("register.html", form=form, current_user=current_user)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))

    return render_template("login.html", form=form, current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/new-item", methods=["GET", "POST"])
@admin_only
def add_new_item():
    form = CreateItemForm()
    if form.validate_on_submit():
        new_item = Products(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            image_url=form.image_url.data,
            about=form.about.data
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("new-item.html", form=form, current_user=current_user)

@app.route("/remove-item/<int:item_id>")
def remove_item_cart(item_id):
    cart = session.get('cart', [])

    if item_id in cart:
        cart.remove(item_id)
        session['cart'] = cart
    cart_items = Products.query.filter(Products.id.in_(cart)).all()
    total_price = sum(item.price for item in cart_items)
    return render_template("cart.html", items=cart_items, total=total_price)

@app.route("/edit-post/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    item = db.get_or_404(Products, item_id)
    edit_form = CreateItemForm(
        name=item.name,
        description=item.description,
        price=item.price,
        image_url=item.image_url,
        about=item.about
    )
    if edit_form.validate_on_submit():
        item.name = edit_form.name.data
        item.description = edit_form.description.data
        item.price = edit_form.price.data
        item.image_url = edit_form.image_url.data
        item.about = edit_form.about.data

        db.session.commit()
        return redirect(url_for("buy", item_id=item.id))
    return render_template("edit-item.html", form=edit_form, is_edit=True, current_user=current_user)

@app.route("/cart-checkout", methods=["GET", "POST"])
def cart_checkout():
    item_id = request.form.get("item_ids")
    print("Received item_ids:", item_id)  # Debugging line

    if not item_id:
        flash("Your cart is empty or something went wrong.")
        return redirect(url_for("cart"))

    item_ids = [int(item_id)]
    selected_items = Products.query.filter(Products.id.in_(item_ids)).all()

    line_items = []
    for item in selected_items:
        line_items.append({
            'price_data': {
                'currency': 'pkr',
                'unit_amount': item.price * 100,
                'product_data': {
                    'name': item.name,
                },
            },
            'quantity': 1,
        })

    if not line_items:
        flash("No valid items to process.")
        return redirect(url_for("cart"))

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode='payment',
        success_url=url_for('success', _external=True),
        cancel_url=url_for('cancel', _external=True),
        shipping_address_collection={
            'allowed_countries': ['PK']
        },
        shipping_options=[{
            'shipping_rate_data': {
                'type': 'fixed_amount',
                'fixed_amount': {'amount': 50000, 'currency': 'pkr'},
                'display_name': 'Standard Delivery',
                'delivery_estimate': {
                    'minimum': {'unit': 'business_day', 'value': 3},
                    'maximum': {'unit': 'business_day', 'value': 7},
                }
            }
        }],
        customer_email=current_user.email if current_user.is_authenticated else None,
    )
    return redirect(checkout_session.url, code=303)
@app.route('/success')
def success():
    session["cart"] = []
    return render_template("payment-successful.html")

@app.route('/cancel')
def cancel():
    return "<h1>Payment Canceled ❌</h1>"

@app.route("/delete/<int:item_id>")
@admin_only
def delete_item(item_id):
    item_to_delete = db.get_or_404(Products, item_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)