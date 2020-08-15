from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, current_app, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app import db
from app.main import bp
from app.main.forms import EditProfileForm, PostForm
from app.models import User, Post
from app.quote import get_quote


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.index'))
        
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
    if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
         if posts.has_prev else None

    quote = current_app.config['QUOTE_OF_THE_DAY']

    return render_template('index.html', title='Home Page', form=form,
                           posts=posts.items, quote=quote,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>/')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)



@bp.route('/edit_profile/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@bp.route('/about')
def about():
    return render_template('about.html')


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/update_post', methods=['POST'])
def update_post():
    post = Post.query.filter_by(id=request.form['id']).first()
    post.body = request.form['body']

    db.session.commit()

    return jsonify({'result': 'success'})


@bp.route('/delete_post', methods=['POST'])
def delete_post():
    Post.query.filter_by(id=request.form['id']).delete()
    db.session.commit()
    return jsonify({'result': 'success', 'redirect': url_for('main.index')})