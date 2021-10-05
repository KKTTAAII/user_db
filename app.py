"""Blogly application."""

from types import MethodDescriptorType
from flask import Flask, request, render_template, redirect, flash, url_for
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "evieiscute"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def list_users():
    """Shows list of all users in db"""
    users = User.query.order_by(User.first_name, User.last_name).all()
    return render_template("home.html", users=users)


@app.route("/newform")
def form():
    """Show a new user form"""
    return render_template("new_user_form.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    """Pull user info to make user details page"""
    first = request.form["first_name"]
    last = request.form["last_name"]
    img = request.form["img_url"]

    new_user = User(first_name=first, last_name=last, image_url=img)

    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/user/{new_user.id}")


@app.route("/user/<int:user_id>")
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.userid == user_id).all()
    return render_template("user_details.html", user=user, posts=posts)


@app.route("/user/<int:user_id>/edit")
def edit_user(user_id):
    """Show edit page"""
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.route("/user/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    """Update user info"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["img_url"]

    db.session.add(user)
    db.session.commit()

    return redirect(f"/user/{user.id}")


@app.route("/user/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete user"""
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    flash("The user has been deleted")
    return redirect("/")


@app.route("/user/<int:user_id>/posts/new")
def show_post_form(user_id):
    """Show a new post form"""
    user = User.query.get_or_404(user_id)
    return render_template("addpost.html", user=user)


@app.route("/user/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Add a new post"""
    user = User.query.get_or_404(user_id)

    title = request.form["title"]
    content = request.form["content"]
    userid = user_id

    new_post = Post(title=title, content=content, userid=user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/user/{user_id}")


@app.route("/post/<int:post_id>")
def show_post(post_id):
    """Show post per post id"""
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)


@app.route("/post/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete post"""
    post = Post.query.get_or_404(post_id)
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    flash("The post has been deleted")
    return redirect("/")


@app.route("/post/<int:post_id>/edit")
def edit_post(post_id):
    """Show edit page"""
    post = Post.query.get_or_404(post_id)
    return render_template("editpost.html", post=post)


@app.route("/post/<int:post_id>/edit", methods=["POST"])
def update_post(post_id):
    """Update post info"""
    post = Post.query.get_or_404(post_id)

    post.title = request.form["title"]
    post.content = request.form["content"]
    post.userid = post.userid

    db.session.add(post)
    db.session.commit()

    return redirect(f"/post/{post_id}")
