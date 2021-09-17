"""Seed file to make sample data for pets db."""

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add user
ted = User(first_name='Ted', last_name='Morris', profile_pic='https://a-z-animals.com/media/2019/11/Duck-isolated.jpg')
tyler = User(first_name='Tyler', last_name='Robison')
bobby = User(first_name='Bobby', last_name='BooYah')
mike = User(first_name='Mike', last_name='Jones', profile_pic='https://images.freeimages.com/images/large-previews/ce3/puppies-1-1308839.jpg')
samantha = User(first_name='Samantha', last_name='McCarthy', profile_pic='https://images.freeimages.com/images/large-previews/294/tomatoes-1326096.jpg')

# Add posts
p1 = Post(title='My cat is cute', content='Oh god he is so cute!!!',created_at='2012-09-16 22:24:03.77707', posted_by=1)
p2 = Post(title='My dog is small', content='Look how small he is',created_at='2013-09-16 22:24:03.77707', posted_by=1)
p3 = Post(title='Need help', content='Need help moving',created_at='2014-09-16 22:24:03.77707', posted_by=2)
p4 = Post(title='hiking', content='Best hikes?',created_at='2015-09-16 22:24:03.77707', posted_by=3)
p5 = Post(title='exercise', content='fave routines?',created_at='2016-09-16 22:24:03.77707', posted_by=3)
p6 = Post(title='Math is hard', content='Need tutor',created_at='2017-09-16 22:24:03.77707', posted_by=3)
p7 = Post(title='No more cereal', content='I ate it all',created_at='2018-09-16 22:24:03.77707', posted_by=4)
p8 = Post(title='Running advice', content='Need to go fast!',created_at='2019-09-16 22:24:03.77707', posted_by=4)
p9 = Post(title='Dating advice', content='Need help',created_at='2020-09-16 22:24:03.77707', posted_by=4)
p10 = Post(title='I like turtles', content='They are are great',created_at='2021-09-16 22:24:03.77707', posted_by=5)


# Add new objects to session, so they'll persist
db.session.add_all([ted, tyler, bobby, mike, samantha])
db.session.commit()

# Post for has foreign key ref to User so have to commit users first or will get error
db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10])
db.session.commit()