"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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
  return redirect('/users')

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

  return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
  user = User.query.get(user_id)
  return render_template('user.html', user=user)

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

  return redirect('/users')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
  user = User.query.get_or_404(user_id)
  db.session.delete(user)
  db.session.commit()
  return redirect('/users')