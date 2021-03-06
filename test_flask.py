from unittest import TestCase

from app import app
from models import db, User, Post, Tag, PostTag

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
        """Add sample users, posts and tags"""

        User.query.delete()

        user = User(first_name='Bobby', last_name='Smith')
        db.session.add(user)
        db.session.commit()

        post1 = Post(title='example1', content='content example1', posted_by=1)
        post2 = Post(title='example2', content='content example2', posted_by=1)
        db.session.add_all([post1, post2])
        db.session.commit()

        tag1 = Tag(tag_name='Exercise')
        tag2 = Tag(tag_name='Outdoors')
        db.session.add_all([tag1, tag2])
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_homepage(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Home Page</h1>', html)


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
            client.post("/users/new", data={
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

    def test_add_post(self):
        """Tests that we can add a post"""
        with app.test_client() as client:   
            client.post('/users/1/posts/new', data={
                'post-title': 'Hiking trails',
                'post-content': 'What are the best trails?',
                'tags': ['1', '2']
            }, follow_redirects=True)    

            resp = client.get('/posts/3')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Hiking trails', html)  
            self.assertIn('What are the best trails?', html)  

    def test_delete_post(self):
        """Tests that we can delete a post"""    
        with app.test_client() as client:
            client.post('/posts/1/delete)', follow_redirects=True)

            resp = client.get('/posts/1', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('content example1', html)  
            #Should be getting re-directed to my 404 content not found page.

            # self.assertIn('Page Not Found', html)
            # If we do get re-directed then this line should pass. 


            

            
