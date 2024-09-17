from flask_sqlalchemy import SQLAlchemy
from flask_injector import inject
from app.models.user import Post,User



class PostService:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_all(self):
        return Post.query.all()
    
    def get_all_AuthorPosts(self,user_id):
        return Post.query.filter_by(user_id=user_id)

    def create(self, title, content,user_id):
        post = Post(title=title, content=content,user_id=user_id)
        self.db.session.add(post)
        self.db.session.commit()

    def get_by_id(self, id):
        return Post.query.filter_by(id=id).first()

    def update(self, post, title, content):
        post.title = title
        post.content = content
        self.db.session.commit()

    def delete(self, post):
        self.db.session.delete(post)
        self.db.session.commit()
        
        
    def add_like(self, post_id, user_id):
        post = self.get_by_id(post_id)
        user = User.query.get(user_id)

        if post and user:
            if not self.has_liked_post(post_id, user_id):  # If the user hasn't liked the post
                user.liked_posts.append(post)  # Add post to user's liked posts
                post.likes += 1  # Increment like count
                self.db.session.commit()

    def remove_like(self, post_id, user_id):
        post = self.get_by_id(post_id)
        user = User.query.get(user_id)

        if post and user:
            if self.has_liked_post(post_id, user_id):  # If the user has liked the post
                user.liked_posts.remove(post)  # Remove post from user's liked posts
                post.likes -= 1  # Decrement like count
                self.db.session.commit()

    def has_liked_post(self, post_id, user_id):
        post = self.get_by_id(post_id)
        user = User.query.get(user_id)

        if post and user:
            return post.liked_users.filter_by(id=user_id).first() is not None
        return False

    def toggle_like(self, post_id, user_id):
        if self.has_liked_post(post_id, user_id):
            self.remove_like(post_id, user_id)
        else:
            self.add_like(post_id, user_id)