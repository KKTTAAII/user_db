"""Blogly application."""

from types import MethodDescriptorType
from flask import Flask, request, render_template, redirect, flash, url_for
from models import db, connect_db, User, Post, Tag, PostTag
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
    return render_template("/user_templates/home.html", users=users)

@app.route("/homepage")
def show_homepage():
    """Show homepage"""
    all_tags = Tag.query.all()
    all_posts = Post.query.order_by(Post.created_at.desc()).limit(5)
    return render_template("/post_templates/home.html", all_posts=all_posts, all_tags=all_tags)

@app.route("/newform")
def form():
    """Show a new user form"""
    return render_template("/user_templates/form.html")

#Uer routes

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
    return render_template("/user_templates/details.html", user=user, posts=posts)


@app.route("/user/<int:user_id>/edit")
def edit_user(user_id):
    """Show edit page"""
    user = User.query.get_or_404(user_id)
    return render_template("/user_templates/edit.html", user=user)


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
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("The user has been deleted")
    return redirect("/homepage")

#post routes

@app.route("/user/<int:user_id>/posts/new")
def show_post_form(user_id):
    """Show a new post form"""
    user = User.query.get_or_404(user_id)
    all_tags = Tag.query.all()
    return render_template("/post_templates/form.html", user=user, all_tags=all_tags)

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

    tag_names = request.form.getlist("tag_name")

    for name in tag_names:
        tag = Tag.query.filter_by(name=name).first()
        tag_id = tag.id
        post_tags = PostTag(post_id=new_post.id, tag_id=tag_id)
        db.session.add(post_tags)
        db.session.commit()

    return redirect(f"/user/{user_id}")

@app.route("/post/<int:post_id>")
def show_post(post_id):
    """Show post per post id"""
    post = Post.query.get_or_404(post_id)
    return render_template("/post_templates/details.html", post=post)

@app.route("/post/<int:post_id>/edit")
def edit_post(post_id):
    """Show edit page"""
    post = Post.query.get_or_404(post_id)
    all_tags = Tag.query.all()
    return render_template("/post_templates/edit.html", post=post, all_tags=all_tags)

@app.route("/post/<int:post_id>/edit", methods=["POST"])
def update_post(post_id):
    """Update post info"""
    post = Post.query.get_or_404(post_id)

    post.title = request.form["title"]
    post.content = request.form["content"]
    post.userid = post.userid

    db.session.add(post)
    db.session.commit()

    tag_names = request.form.getlist("tag_name")
    db.session.query(PostTag).filter(PostTag.post_id==post_id).delete()

    for name in tag_names:
        tag_id = Tag.query.filter_by(name=name).first().id
    
        updated_tags = PostTag(post_id=post_id, tag_id=tag_id)
        db.session.add(updated_tags)
        db.session.commit()
        
    return redirect(f"/post/{post_id}")

@app.route("/post/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("The post has been deleted")
    return redirect("/")

#tag routes

@app.route("/tags")
def list_tags():
    """Show a list of all tags"""
    all_tags = Tag.query.all()
    return render_template("/tag_templates/home.html", all_tags=all_tags)

@app.route("/tags/<int:tag_id>")
def list_tags_details(tag_id):
    """Show posts title with the tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("/tag_templates/details.html", tag=tag)

@app.route("/tags/new")
def tag_form():
    """Show a new tag form"""
    return render_template("/tag_templates/form.html")

@app.route("/tags/new", methods=["POST"])
def create_tag():
    """Show a new tag"""
    name = request.form["name"]
    new_tag = Tag(name=name)

    db.session.add(new_tag)
    db.session.commit()

    return redirect(f"/tags/{new_tag.id}")

@app.route("/tags/<int:tag_id>/edit")
def tag_edit(tag_id):
    """Show tag edit page"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("/tag_templates/edit.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def update_tag(tag_id):
    """Show tag edit page"""
    tag = Tag.query.get_or_404(tag_id)

    tag.name = request.form["name"]

    db.session.add(tag)
    db.session.commit()
    return redirect(f"/tags/{tag.id}")

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash("The tag has been deleted")
    return redirect("/tags")

  