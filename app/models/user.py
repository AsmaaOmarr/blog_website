from flask_login import UserMixin
from app import db



# Association table for likes
likes_table = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='reader')
    
    # 1 to many each author has many posts
    posts = db.relationship('Post', backref='author', lazy=True)
    
    # Many-to-many post can have many likes and user can make many likes
    liked_posts = db.relationship(
        'Post',
        secondary=likes_table,  # Links to the likes_table
        backref=db.backref('liked_users', lazy='dynamic')  # Back reference for querying liked users on Post
    )

    def __repr__(self):
        return f'<User {self.username}>'
    
    
class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.Column(db.Integer, default=0) 
    
