# ============================================================
#  TechBlog — Flask Blog & Admin Panel
#  Author   : ZERO (Sobhan) — https://github.com/zeroux-dev
#  Telegram : @fesqhli  (https://t.me/fesqhli)
#  License  : MIT — keep this notice when you use or copy this code
#  Copyright (c) 2025-2026 ZERO (Sobhan)
# ============================================================
import os
import secrets
import click
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import (SQLALCHEMY_DATABASE_URI, SECRET_KEY, UPLOAD_FOLDER,
                    ALLOWED_IMAGE_EXTENSIONS, MAX_CONTENT_LENGTH)
from models import db, User, Post, Comment, PostLike, CommentLike, CommentReport
from sqlalchemy import or_, func
import math
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


def allowed_image(filename):
    """Only accept real image extensions for uploads."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
    

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def estimate_reading_time(text):
    if not text: return 1
    return math.ceil(len(text.split()) / 200)
app.jinja_env.globals.update(estimate_reading_time=estimate_reading_time)

@app.context_processor
def inject_categories():
    try:
        categories = db.session.query(Post.category).distinct().all()
        category_list = [c[0] for c in categories if c[0]]
        return dict(all_categories=category_list)
    except:
        return dict(all_categories=[])

@app.route('/')
def index():
    query = request.args.get('q')
    category_filter = request.args.get('category')
    posts_query = Post.query
    title = "آخرین نوشته‌ها"
    if category_filter:
        posts_query = posts_query.filter_by(category=category_filter)
        title = f"دسته بندی: {category_filter}"
    if query:
        posts_query = posts_query.filter(or_(Post.title.ilike(f'%{query}%'), Post.content.ilike(f'%{query}%')))
        title = f"جستجو: {query}"
    posts = posts_query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts, page_title=title)

@app.route('/read/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'GET':
        post.views += 1
        db.session.commit()
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('برای ارسال نظر لطفاً وارد شوید.')
            return redirect(url_for('login'))
        comment_body = request.form.get('body')
        if comment_body:
            db.session.add(Comment(body=comment_body, post_id=post.id, user_id=current_user.id))
            db.session.commit()
            return redirect(url_for('post_detail', post_id=post.id))
    user_liked = False
    if current_user.is_authenticated:
        user_liked = PostLike.query.filter_by(user_id=current_user.id, post_id=post.id).first() is not None
    return render_template('post.html', post=post, user_liked=user_liked)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category') or 'عمومی'
        image_file = None
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '' and allowed_image(file.filename):
                filename = secure_filename(file.filename)
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_file = filename
        post = Post(title=title, content=content, category=category, image_file=image_file, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_post.html', title='نوشتن پست')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            # --- ثبت زمان آخرین بازدید ---
            user.last_login = datetime.utcnow()
            db.session.commit()
            # -----------------------------
            return redirect(url_for('index'))
        else:
            flash('نام کاربری یا رمز عبور اشتباه است.')
    return render_template('login.html')

# ... (بقیه کدها ثابت) ...

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        # 1. بررسی نام کاربری
        if User.query.filter_by(username=username).first(): 
            flash('این نام کاربری قبلاً گرفته شده است.')
            return redirect(url_for('register'))
            
        # 2. بررسی ایمیل (اگر وارد شده باشد)
        if email and User.query.filter_by(email=email).first():
            flash('این ایمیل قبلاً ثبت شده است.')
            return redirect(url_for('register'))
            
        # 3. بررسی موبایل (اگر وارد شده باشد)
        if phone and User.query.filter_by(phone=phone).first():
            flash('این شماره موبایل قبلاً ثبت شده است.')
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(request.form.get('password'), method='scrypt')
        
        profile_pic = None
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file.filename != '' and allowed_image(file.filename):
                filename = secure_filename(file.filename)
                filename = f"user_{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile_pic = filename

        new_user = User(
            username=username,
            password=hashed_pw,
            email=email,
            phone=phone,
            gender=request.form.get('gender'),
            profile_pic=profile_pic,
            last_login=datetime.utcnow()
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template('register.html')
# --- ریست پسورد کاربر توسط ادمین ---
@app.route('/admin/user/<int:user_id>/reset_pass', methods=['POST'])
@login_required
def admin_reset_password(user_id):
    if current_user.username != 'admin': abort(403)
    user = User.query.get_or_404(user_id)
    
    # رمز موقت تصادفی (امن‌تر از رمز ثابت)
    temp_password = secrets.token_urlsafe(8)
    user.password = generate_password_hash(temp_password, method='scrypt')
    db.session.commit()

    flash(f'رمز عبور موقت کاربر {user.username}: {temp_password}', 'success')
    return redirect(url_for('admin_user_detail', user_id=user.id))


# ... (بقیه کدها) ...

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and current_user.username != 'admin': abort(403)
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.category = request.form.get('category')
        db.session.commit()
        return redirect(url_for('post_detail', post_id=post.id))
    return render_template('create_post.html', title='ویرایش', post=post)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and current_user.username != 'admin': abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/post/<int:post_id>/like')
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    like = PostLike.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    if like: db.session.delete(like)
    else: db.session.add(PostLike(user_id=current_user.id, post_id=post.id))
    db.session.commit()
    return redirect(url_for('post_detail', post_id=post.id))

@app.route('/comment/<int:comment_id>/like')
@login_required
def like_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    like = CommentLike.query.filter_by(user_id=current_user.id, comment_id=comment.id).first()
    if like: db.session.delete(like)
    else: db.session.add(CommentLike(user_id=current_user.id, comment_id=comment.id))
    db.session.commit()
    return redirect(url_for('post_detail', post_id=comment.post.id))

@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post.id 
    if current_user.username == 'admin' or current_user == comment.post.author or current_user == comment.author:
        db.session.delete(comment)
        db.session.commit()
    else: abort(403)
    return redirect(url_for('post_detail', post_id=post_id))

@app.route('/comment/<int:comment_id>/report', methods=['POST'])
@login_required
def report_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    reason = request.form.get('reason')
    if reason:
        existing = CommentReport.query.filter_by(user_id=current_user.id, comment_id=comment.id).first()
        if not existing:
            db.session.add(CommentReport(reason=reason, user_id=current_user.id, comment_id=comment.id))
            db.session.commit()
            flash('گزارش ارسال شد.', 'success')
    return redirect(url_for('post_detail', post_id=comment.post.id))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.username != 'admin': abort(403)
    stats = {
        'users': User.query.count(),
        'posts': Post.query.count(),
        'comments': Comment.query.count(),
        'views': db.session.query(func.sum(Post.views)).scalar() or 0,
        'reports_count': CommentReport.query.count(),
        'categories_count': db.session.query(Post.category).distinct().count()
    }
    recent_users = User.query.order_by(User.id.desc()).limit(5).all()
    reports = CommentReport.query.order_by(CommentReport.date_reported.desc()).all()
    return render_template('admin_dashboard.html', stats=stats, reports=reports, recent_users=recent_users, now=datetime.now())

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.username != 'admin': abort(403)
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/user/<int:user_id>')
@login_required
def admin_user_detail(user_id):
    if current_user.username != 'admin': abort(403)
    user = User.query.get_or_404(user_id)
    return render_template('admin_user_detail.html', user=user)

@app.route('/admin/report/<int:report_id>/delete', methods=['POST'])
@login_required
def delete_report(report_id):
    if current_user.username != 'admin': abort(403)
    report = CommentReport.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/categories')
@login_required
def admin_categories():
    if current_user.username != 'admin': abort(403)
    categories = db.session.query(Post.category, func.count(Post.id)).group_by(Post.category).all()
    return render_template('admin_categories.html', categories=categories)

@app.route('/admin/category/delete', methods=['POST'])
@login_required
def delete_category():
    if current_user.username != 'admin': abort(403)
    cat_name = request.form.get('category_name')
    posts = Post.query.filter_by(category=cat_name).all()
    for post in posts: post.category = 'عمومی'
    db.session.commit()
    return redirect(url_for('admin_categories'))

@app.route('/admin/category/rename', methods=['POST'])
@login_required
def rename_category():
    if current_user.username != 'admin': abort(403)
    old_name = request.form.get('old_name')
    new_name = request.form.get('new_name')
    if new_name:
        posts = Post.query.filter_by(category=old_name).all()
        for post in posts: post.category = new_name
        db.session.commit()
    return redirect(url_for('admin_categories'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.cli.command('init-db')
@click.option('--admin-password', envvar='ADMIN_PASSWORD', prompt=True, hide_input=True,
              confirmation_prompt=True, help='Password for the "admin" account')
def init_db(admin_password):
    """Create all tables and the admin user:  flask --app app init-db"""
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        db.session.add(User(username='admin',
                            password=generate_password_hash(admin_password, method='scrypt')))
        db.session.commit()
    click.echo('Database is ready. Admin user: admin')


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1', port=5009)
