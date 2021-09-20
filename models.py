"""Models for Blogly."""

from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from werkzeug.utils import redirect
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model"""

    __tablename__ = "users" 

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)

    first_name = db.Column(db.Text,
                    nullable=False,
                    unique=True)        

    last_name = db.Column(db.Text,
                    nullable=False,
                    unique=True)   

    profile_pic = db.Column(db.String,
                default='https://images.freeimages.com/images/large-previews/b3d/flowers-1375316.jpg')             

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")            

    @classmethod
    def add_user(cls, first_name, last_name, profile_pic):
        """adds a new user"""

        if first_name == '':
            first_name = None

        if last_name == '':
            last_name = None

        new_user = User(first_name = first_name, last_name = last_name, profile_pic = profile_pic)


     
        db.session.add(new_user)
        db.session.commit()   
      

    @classmethod
    def list_users(cls):
        """lists users"""  

        return cls.query.all()                        

    def edit_user(self, first_name, last_name, profile_pic):
        """Edits current user"""

        if first_name == '':
            first_name = None

        if last_name == '':
            last_name = None

        if profile_pic == None:
            profile_pic = 'https://images.freeimages.com/images/large-previews/b3d/flowers-1375316.jpg'
        self.first_name = first_name
        self.last_name = last_name
        self.profile_pic = profile_pic

        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        """Deletes current user"""

        # 
        user = User.query.filter(User.id == self.id).first()
        db.session.delete(user)
        print('*****************************************************************************')
        print('deleting')

        db.session.commit()

class Post(db.Model):
    """Post model"""        

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)

    title = db.Column(db.Text,
                    nullable=False)        

    content = db.Column(db.Text,
                    nullable=False)   

    created_at = db.Column(db.DateTime,
                    nullable=False,
                    default=datetime.datetime.now) 

    posted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  

    tags_with_post = db.relationship('Tag', 
                                    secondary='posts_tags',
                                    backref='posts')

    # post_tags = db.relationship("PostTag", backref="post", cascade="all, delete-orphan")                                        
  

    @classmethod
    def add_post(cls, title, content, posted_by):
        """Adds a new post"""    

        if title == '':
            title = None

        if content == '':
            content = None      

                  

        new_post = Post(title=title, content=content, posted_by=posted_by)

        # import pdb
        # pdb.set_trace() 

        db.session.add(new_post)
        db.session.commit()    

    
    def edit_post(self, title, content):
        """Adds a new post"""    

        if title == '':
            title = None

        if content == '':
            content = None      
  

        self.title = title
        self.content = content

        db.session.add(self)
        db.session.commit()       

    def delete_post(self):
        """Deletes post"""    

        post = Post.query.filter(Post.id == self.id).first()
        db.session.delete(post)

        db.session.commit()

class Tag(db.Model):
    """Tag Model"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)

    tag_name = db.Column(db.Text, nullable=False, unique=True) 

    posts_with_tag = db.relationship('Post', 
                                    secondary='posts_tags',
                                    backref='tags')
                         

    @classmethod
    def list_tags(cls):
        """lists tags"""  

        return cls.query.all()   

    @classmethod
    def add_tag(cls, tag_name):
        """Adds a new Tag"""

        if tag_name == '':
            tag_name = None     

        new_tag = Tag(tag_name=tag_name)

        db.session.add(new_tag)
        db.session.commit()
        
    def edit_tag(self, tag_name):
        """Edits a tag"""

        if tag_name == '':
            tag_name = None      

        self.tag_name = tag_name

        db.session.add(self)
        db.session.commit()    

    def delete_tag(self):
        """Deletes a tag"""  

        tag = Tag.query.filter(Tag.id == self.id).first()
        db.session.delete(tag)

        db.session.commit()  

class PostTag(db.Model):
    """A PostTag joins together a Post and a Tag"""

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)









    


