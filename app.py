"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'goldtree9'

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def root():
  posts = Post.query.all()
  print(posts)
  return render_template('posts.html', posts=posts)

@app.route('/users')
def users():
  users = User.query.order_by(User.last_name, User.first_name).all()
  return render_template('index.html', users=users)

@app.route('/users/new', methods=["GET"])
def add_user_form():
  return render_template('new_user.html')

@app.route('/users/new', methods=["POST"])
def add_user():
  first_name = request.form["first_name"]
  last_name = request.form["last_name"]
  image_url = request.form["image_url"] or None
  
  new_user = User(
    first_name = first_name,
    last_name = last_name,
    image_url = image_url
  )
  
  db.session.add(new_user)
  db.session.commit()
  flash("User Created!")
  return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
  user = User.query.get(user_id)
  posts = user.posts
  print(posts)
  return render_template('user.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
  user = User.query.get(user_id)

  return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
  user = User.query.get(user_id)
  
  user.first_name = request.form["first_name"]
  user.last_name = request.form["last_name"]
  user.image_url = request.form["image_url"]

  db.session.commit()
  flash("User Edited!")
  return redirect('/users')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
  user = User.query.get_or_404(user_id)
  db.session.delete(user)
  db.session.commit()
  flash("User Deleted!")
  return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
  user = User.query.get(user_id)
  return render_template('new_post.html', user_id=user_id, user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post(user_id):
  post = Post(
    title=request.form["title"],
    content=request.form["content"],
    user_id=user_id
  )
  db.session.add(post)
  db.session.commit()
  flash("Post Created!")
  return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
  post = Post.query.get(post_id)

  return render_template('post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
  post = Post.query.get(post_id)

  return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
  post = Post.query.get(post_id)

  post.title = request.form["title"]
  post.content = request.form["content"]
  flash("Post Edited!")
  db.session.commit()

  return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
  post = Post.query.get(post_id)
  db.session.delete(post)
  db.session.commit()
  flash("Post Deleted!")
  return redirect('/users')