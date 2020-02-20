"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = 'https://topgear.com.my/sites/default/files/default_images/avatar-default.png'

class User(db.Model):
  __tablename__ = "users"

  @property
  def full_name(self):
    return f"{self.first_name} {self.last_name}"

  id = db.Column(
    db.Integer,
    primary_key=True,
    autoincrement=True
  )
  first_name = db.Column(
    db.Text,
    nullable=False
  )
  last_name = db.Column(
    db.Text,
    nullable=False
  )
  image_url = db.Column(
    db.Text,
    nullable=False,
    default=DEFAULT_IMAGE_URL
  )

  posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

class Post(db.Model):
  __tablename__ = "posts"

  id = db.Column(
    db.Integer,
    primary_key=True,
    autoincrement=True
  )

  title = db.Column(
    db.Text,
    nullable=False
  )

  content = db.Column(
    db.Text,
    nullable=False
  )

  created_at = db.Column(
    db.DateTime,
    nullable=False,
    default=datetime.datetime.now
  )

  user_id = db.Column(
    db.Integer,
    db.ForeignKey('users.id')
  )

  @property
  def getTime(self):
    return self.created_at.strftime('%a %b %d %Y, %I:%M %p')

def connect_db(app):
  db.app = app
  db.init_app(app)