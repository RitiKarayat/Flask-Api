from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import current_user, login_required
from .models import Post, User, Comment, Like
from . import db

views = Blueprint('views',__name__)

@views.route('/')
@views.route('/home')
@login_required
def home():
    posts = Post.query.all()

    return render_template('home.html',user=current_user,posts=posts)

@views.route('/create-post',methods=['GET','POST'])
@login_required
def create_post():
    if request.method=='POST':
        text = request.form.get('text')
        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text,author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post Created', category='success')
            return redirect(url_for('views.home'))
        
    return render_template('create_post.html',user=current_user)


@views.route('/delete-post/<int:id>')
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash('Post Does not exist', category='error')
    elif current_user.id != post.user.id:
        flash('You cannot delete this post', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post Deleted', category='success')
    return redirect(url_for('views.home'))
    
@views.route('/posts/<username>')
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('The user does not exists',category='error')
        return redirect(url_for('views.home'))
    #posts = user.posts
    return render_template('posts.html',user=current_user,posts=user.posts,username=username)

@views.route('/create-comment/<post_id>', methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')
    if not text:
        flash('Comment cannot be empty', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(text=text,author=current_user.id,post_id=post_id)
            db.session.add(comment)
            db.session.commit()
    
    return redirect(url_for('views.home'))

@views.route('/delete-comment/<comment_id>')
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if not comment:
        flash('Comment does not exist', category='error')
    elif current_user.id == comment.author or current_user.id == comment.post.author:
        db.session.delete(comment)
        db.session.commit()
    else:
        flash('You cannot delete this comment', category='error')

    return redirect(url_for('views.home'))

@views.route('/like-post/<post_id>', methods=['GET'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id)
    like = Like.query.filter_by(author=current_user.id,post_id=post_id).first()
    if not post:
        flash('Post does not exist',category='error')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    
    return redirect(url_for('views.home'))

@views.route('/update-post/<post_id>',methods=['GET','POST'])
@login_required
def update_post(post_id):
    if request.method=='POST':
        post = Post.query.filter_by(id=post_id).first()
        if not post:
            flash('Post does not exist', category='error')
        else:
            text = request.form.get('text')
            if not text:
                flash('Post cannot be empty', category='error')
            else:
                post.text = text
                db.session.commit()
                flash('Post Updated', category='success')
                return redirect(url_for('views.home'))
        
    return render_template('update_post.html',user=current_user)
    
    

