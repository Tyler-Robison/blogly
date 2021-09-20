"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
from operator import attrgetter

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickensrawesome"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home_page():
    """Redirects to users page"""

    posts = Post.query.all()
    sorted_posts = sorted(posts, key=attrgetter('created_at'), reverse=True)

    return render_template('home.html', posts=sorted_posts)


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404


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
    post_list = Post.query.filter(Post.posted_by == user_id).all()

    return render_template('detail.html', user=user, post_list=post_list)


@app.route('/users/<user_id>/edit')
def edit_user(user_id):
    """Displays current user details and allows you to edit"""

    user = User.query.get_or_404(user_id)

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
    user = User.query.get_or_404(user_id)

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

    user = User.query.get_or_404(user_id)
    user.delete_user()

    return redirect('/users')

# routes involving posts


@app.route('/users/<user_id>/posts/new')
def add_post(user_id):
    """Displays form needed to add a post from a specific user"""

    user = User.query.get_or_404(user_id)

    tags = Tag.query.all()

    return render_template('create_post.html', user=user, tags=tags)


@app.route('/users/<user_id>/posts/new', methods=["POST"])
def process_add_post(user_id):
    """Processes form info and creates a new post"""

    title = request.form['post-title']
    content = request.form['post-content']

    tag_list = request.form.getlist('tags')
    tag_ids = [int(num) for num in tag_list]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    # import pdb
    # pdb.set_trace()

    try:
        Post.add_post(title, content, int(user_id), tags)
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
    tags = post.tags_with_post

    return render_template('post_detail.html', post=post, tags=tags)


@app.route('/posts/<post_id>/edit')
def edit_post(post_id):
    """Allows you to edit post"""

    post = Post.query.get_or_404(post_id)
    tags = post.tags_with_post

    all_tags = Tag.query.all()

    return render_template('edit_post.html', post=post, tags=tags, all_tags=all_tags)


@app.route('/posts/<post_id>/edit', methods=["POST"])
def process_edit_post(post_id):
    """Processes editing of post"""

    title = request.form['edit-title']
    content = request.form['edit-content']

    tag_list = request.form.getlist('tags')
    tag_ids = [int(num) for num in tag_list]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post = Post.query.get_or_404(post_id)

    # import pdb
    # pdb.set_trace()

    try:
        post.edit_post(title, content, tags)
    except:
        db.session.rollback()
        flash('title and content must be filled in')
        return redirect(f'/posts/{post_id}/edit')

    return redirect(f'/posts/{post_id}')


@app.route('/posts/<post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Deletes a post"""

    post = Post.query.get_or_404(post_id)
    post.delete_post()

    # re-direct somewhere else
    return redirect('/users')

# routes for tags


@app.route('/tags')
def list_tags():
    """Lists all tags"""

    tags = Tag.list_tags()

    return render_template('tags.html', tags=tags)


@app.route('/tags/<tag_id>')
def tag_detail(tag_id):
    """Shows detail about a tag"""

    tag = Tag.query.filter(Tag.id == int(tag_id)).first()

    posts = tag.posts_with_tag

    return render_template('tag_detail.html', tag=tag, posts=posts)


@app.route('/tags/new')
def add_tag():
    """Adds a new tag"""

    return render_template('new_tag.html')


@app.route('/tags/new', methods=["POST"])
def process_new_tag():
    """Process new tag"""

    tag_name = request.form['new-tag']

    try:
        Tag.add_tag(tag_name)
    except:
        db.session.rollback()
        flash('tag name must be filled in')
        return redirect('/tags/new')

    return redirect('/tags')


@app.route('/tags/<tag_id>/edit')
def edit_tag(tag_id):
    """Shows page to edit tag"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('edit_tag.html', tag=tag)


@app.route('/tags/<tag_id>/edit', methods=["POST"])
def process_edit_tag(tag_id):
    """Processes tag editing"""

    tag = Tag.query.get_or_404(tag_id)

    tag_name = request.form['edit-tag']

    try:
        tag.edit_tag(tag_name)
    except:
        db.session.rollback()
        flash('tag name must be filled in')
        return redirect(f'/tags/{tag_id}/edit')

    return redirect('/tags')


@app.route('/tags/<tag_id>/delete')
def delete_tag(tag_id):
    """Deletes a tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.delete_tag()

    return redirect('/tags')
