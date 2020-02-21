# Import Libraries
from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

# Confifure Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'goldtree9'
debug = DebugToolbarExtension(app)

# Connect TO PostgreSQL
connect_db(app)

# Root Route
@app.route('/')
def root():
  posts = Post.query.all()
  print(posts)
  return render_template('posts/posts.html', posts=posts)

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

# User Routes
# 1. List all users
@app.route('/users')
def users():
  users = User.query.order_by(User.last_name, User.first_name).all()
  return render_template('users/users.html', users=users)

# 2. Show Form to create a new user 
@app.route('/users/new', methods=["GET"])
def add_user_form():
  return render_template('users/new_user.html')

# 3. Create a new user
@app.route('/users/new', methods=["POST"])
def add_user():
  # Get values from the form
  first_name = request.form["first_name"]
  last_name = request.form["last_name"]
  image_url = request.form["image_url"]
  
  new_user = User(
    first_name = first_name,
    last_name = last_name,
    image_url = image_url
  )
  
  db.session.add(new_user)
  db.session.commit()

  flash("User Created!")
  return redirect('/users')

# 4. Display user info
@app.route('/users/<int:user_id>')
def show_user(user_id):
  user = User.query.get(user_id)
  return render_template('users/user.html', user=user)

# 5. Show form to edit user info
@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
  user = User.query.get(user_id)
  return render_template('users/edit_user.html', user=user)

# 6. Edit user info
@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
  user = User.query.get(user_id)
  
  user.first_name = request.form["first_name"]
  user.last_name = request.form["last_name"]
  user.image_url = request.form["image_url"]

  db.session.commit()
  flash("User Edited!")
  return redirect('/users')

# 7. Delete a User
@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
  user = User.query.get_or_404(user_id)
  db.session.delete(user)
  db.session.commit()
  flash("User Deleted!")
  return redirect('/users')

# Posts Route
# 1. Form to Create a new post
@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
  user = User.query.get(user_id)
  tags = Tag.query.all()
  return render_template('posts/new_post.html', user=user, tags=tags)

# 2. Create a new post
@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post(user_id):
  user = User.query.get_or_404(user_id)
  tag_ids = [int(num) for num in request.form.getlist("tags")]
  tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

  post = Post(
    title=request.form["title"],
    content=request.form["content"],
    user = user,
    tags = tags
  )

  db.session.add(post)
  db.session.commit()
  flash("Post Created!")
  
  return redirect(f'/users/{user_id}')

# 3. Show post details 
@app.route('/posts/<int:post_id>')
def show_post(post_id):
  post = Post.query.get(post_id)

  return render_template('posts/post.html', post=post)

# 4. Show form to edit post
@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
  
  post = Post.query.get(post_id)
  tags = Tag.query.all()
  return render_template('posts/edit_post.html', post=post, tags=tags)

# 5. Edit post
@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
  post = Post.query.get(post_id)

  post.title = request.form["title"]
  post.content = request.form["content"]

  tags_ids = [int(num) for num in request.form.getlist("tags")]
  post.tags = Tag.query.filter(Tag.id.in_(tags_ids)).all()

  db.session.commit()
  return redirect(f'/users/{post.user_id}')

# 6. Delete Post
@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
  
  post = Post.query.get(post_id)
  
  db.session.delete(post)
  db.session.commit()
  flash("Post Deleted!")
  
  return redirect('/users')

# Tag Routes
# 1. Lists all tags, with links to the tag detail page.
@app.route('/tags')
def show_tags():
  tags = Tag.query.all()
  return render_template('tags/tags.html', tags=tags)

# 2. Show detail about a tag. Have links to edit form and to delete.
@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
  tag = Tag.query.get_or_404(tag_id)
  return render_template('tags/tag.html', tag=tag)

# 3. Shows a form to add a new tag.
@app.route('/tags/new')
def new_tag_form():
  return render_template('tags/new_tag.html')

# 4. Process add form, adds tag, and redirect to tag list.
@app.route('/tags/new', methods=["POST"])
def new_tag():
  tag = Tag(name=request.form["name"])

  db.session.add(tag)
  db.session.commit()

  return redirect('/tags')

# 5. Show edit form for a tag.
@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
  tag = Tag.query.get(tag_id)

  return render_template('tags/edit_tag.html', tag=tag)

# 6. Process edit form, edit tag, and redirects to the tags list.
@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
  tag = Tag.query.get(tag_id)

  tag.name = request.form["name"]

  db.session.commit()
  return redirect("/tags")

# 7. Delete a tag.
@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
  tag = Tag.query.get(tag_id)

  db.session.delete(tag)
  db.session.commit()

  return redirect("/tags")