"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickensrawesome"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()


@app.route('/')
def home_page():
    """Redirects to users page"""

    return redirect('/users')

# @app.errorhandler(404)
# def page_not_found(e):
#     """Show 404 NOT FOUND page."""

#     return render_template('404.html'), 404    


@app.route('/users')
def user_page():
    """Displays a list of all users"""

    users = User.list_users()

    return render_template('users.html', users=users)


@app.route('/users/new')
def new_user():
    """Displays form to add new user"""

    return render_template('new.html')


@app.route('/users/new', methods=["POST"])
def create_users():
    """Adds new user to db then redirects back to users page"""

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    profile_pic = request.form['profile-img']
    profile_pic = profile_pic if profile_pic else None

    try:
        User.add_user(first_name, last_name, profile_pic)
    except:
        db.session.rollback()
        flash('First and Last name must be filled out and unique')
        return redirect('/users/new')

    flash('User created!')
    return redirect('/users')


@app.route('/users/<user_id>')
def user_detail(user_id):
    """Displays user details"""

    user = User.query.get_or_404(user_id)
    # post_list = Post.get_posts(user_id)
    post_list = Post.query.filter(Post.posted_by == user_id).all()
    # import pdb
    # pdb.set_trace()


    return render_template('detail.html', user=user, post_list=post_list)


@app.route('/users/<user_id>/edit')
def edit_user(user_id):
    """Displays current user details and allows you to edit"""

    user = User.query.filter(User.id == user_id).first()

    return render_template('edit.html', user=user)


@app.route('/users/<user_id>/edit', methods=["POST"])
def process_edit_user(user_id):
    """Processes the edit form then redirects back to user list"""

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    profile_pic = request.form['profile-img']
    profile_pic = profile_pic if profile_pic else None

    # import pdb
    # pdb.set_trace()
    user = User.query.filter(User.id == user_id).first()

    try:
        user.edit_user(first_name, last_name, profile_pic)
    except:
        db.session.rollback()
        flash('First and Last name must be filled out and unique')
        return redirect(f'/users/{user_id}/edit')

    return redirect('/users')


@app.route('/users/<user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes the user"""

    user = User.query.filter(User.id == user_id).first()
    user.delete_user()

    return redirect('/users')

# routes involving posts


@app.route('/users/<user_id>/posts/new')
def add_post(user_id):
    """Displays form needed to add a post from a specific user"""

    user = User.query.get_or_404(user_id)

    return render_template('create_post.html', user=user)


@app.route('/users/<user_id>/posts/new', methods=["POST"])
def process_add_post(user_id):
    """Processes form info and creates a new post"""

    title = request.form['post-title']
    content = request.form['post-content']

    try:
        Post.add_post(title, content, int(user_id))
    except:
        db.session.rollback()
        flash('title and content must be filled in')
        return redirect(f'/users/{user_id}/posts/new')

    flash('Post created!')
    return redirect('/users')

@app.route('/posts/<post_id>')
def show_post(post_id):
    """Displays title and content of post"""

    
    post = Post.query.filter(Post.id == post_id).first()

    return render_template('post_detail.html', post=post)    

@app.route('/posts/<post_id>/edit')
def edit_post(post_id):
    """Allows you to edit post"""

    post = Post.query.filter(Post.id == post_id).first()

    return render_template('edit_post.html', post=post)

@app.route('/posts/<post_id>/edit', methods=["POST"])
def process_edit_post(post_id):
    """Processes editing of post"""

    title = request.form['edit-title']
    content = request.form['edit-content']

    
    post = Post.query.filter(Post.id == post_id).first()

    # problem line, try in terminal -> need posted_by.first_name etc.
    # posted_by = User.query.filter(User.id == post_id).first()

    # import pdb
    # pdb.set_trace()

    try:
        post.edit_post(title, content)
    except:        
        db.session.rollback()
        flash('title and content must be filled in')
        return redirect(f'/posts/{post_id}/edit')

    return redirect(f'/posts/{post_id}')    

@app.route('/posts/<post_id>/delete', methods=["POST"])
def delete_post(post_id):

    post = Post.query.filter(Post.id == post_id).first()
    post.delete_post()

    #re-direct somewhere else
    return redirect('/users')