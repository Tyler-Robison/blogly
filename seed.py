"""Seed file to make sample data for pets db."""

from models import User, db
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

# Add new objects to session, so they'll persist
db.session.add(ted)
db.session.add(tyler)
db.session.add(bobby)

# Commit--otherwise, this never gets saved!
db.session.commit()