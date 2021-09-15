"""Models for Blogly."""

from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model"""

    __tablename__ = "users" 

    @classmethod
    def add_user(cls, first_name, last_name, profile_pic):
        """adds a new user"""

        new_user = User(first_name = first_name, last_name = last_name, profile_pic = profile_pic)

     
        db.session.add(new_user)
        db.session.commit()   
      

    @classmethod
    def list_users(cls):
        """lists users"""  

        return cls.query.all()      



    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)

    first_name = db.Column(db.String(20),
                    nullable=False,
                    unique=True)        

    last_name = db.Column(db.String(20),
                    nullable=False,
                    unique=True)   

    profile_pic = db.Column(db.String,
                default='https://images.freeimages.com/images/large-previews/b3d/flowers-1375316.jpg')                               

    def edit_user(self, first_name, last_name, profile_pic):
        """Edits current user"""

        if profile_pic == None:
            profile_pic = 'https://images.freeimages.com/images/large-previews/b3d/flowers-1375316.jpg'
        self.first_name = first_name
        self.last_name = last_name
        self.profile_pic = profile_pic
        # import pdb
        # pdb.set_trace()
    

        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        """Deletes current user"""

        User.query.filter(User.id == self.id).delete()

        db.session.commit()



