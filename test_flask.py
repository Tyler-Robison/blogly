from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserTestCase(TestCase):
    """Tests routes"""

    def setUp(self):
        """Add sameple users"""

        User.query.delete()

        user = User(first_name='Bobby', last_name='Smith')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_homepage(self):
        with app.test_client() as client:
            resp = client.get("/")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, 'http://localhost/users')

    def test_follow_redirect(self):
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>User List</h1>', html)


    def test_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Bobby', html)

    def test_add_user(self):
        with app.test_client() as client:
            resp = client.post("/users/new", data={
                'first-name' : 'Ted',
                'last-name' : 'Jones',
                'profile-img' : 'https://images.freeimages.com/images/large-previews/b3d/flowers-1375316.jpg'
            }, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>User List</h1>', html)
            self.assertIn('Ted', html)

    def test_default_img(self):
        """Post request with blank img, then get request to user detail page to make sure default image loads."""
        with app.test_client() as client:
            resp = client.post("/users/new", data={
                'first-name' : 'Ted',
                'last-name' : 'Jones',
                'profile-img' : ''
            }, follow_redirects=True)

            resp = client.get("/users/2")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>User Info</h1>', html)
            self.assertIn('https://images.freeimages.com/images/large-previews/b3d/flowers-1375316.jpg', html)
            self.assertIn('Ted', html)     

    def test_delete_user(self):
        """Tests that we can delete a user"""   
        with app.test_client() as client:    
            resp = client.post("/users/1/delete", follow_redirects=True) 
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>User List</h1>', html)
            self.assertNotIn('Bobby', html)

            

            
