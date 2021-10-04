"""Blogly application."""

from types import MethodDescriptorType
from flask import Flask, request, render_template,  redirect, flash, url_for
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "evieiscute"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def list_users():
    """Shows list of all users in db"""
    users = User.query.order_by(User.first_name, User.last_name).all()
    return render_template('home.html', users=users)

@app.route('/newform')
def form():
    """Show a new user form"""
    return render_template('new_user_form.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """Pull user info to make user details page"""
    first = request.form["first_name"]
    last = request.form["last_name"]
    img = request.form["img_url"]

    new_user  = User(first_name=first, last_name=last, image_url=img)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/user/{new_user.id}")

@app.route("/user/<int:user_id>")
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)

@app.route("/user/<int:user_id>/edit")
def edit_user(user_id):
    """Show edit page"""
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user = user)

@app.route("/user/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    """Update user info"""
    user = User.query.get_or_404(user_id)
    first = request.form["first_name"]
    last = request.form["last_name"]
    img = request.form["img_url"]

    user.first_name = first
    user.last_name = last
    user.image_url = img

    db.session.add(user)
    db.session.commit()

    return redirect("/")

@app.route("/user/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete user"""
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    flash("The user has been deleted")
    return redirect("/")
