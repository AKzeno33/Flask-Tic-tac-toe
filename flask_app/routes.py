from flask import render_template, redirect, url_for, flash, request, current_app
from flask_app import app, db, bcrypt, mail
from flask_app.forms import SignupForm, LoginForm, UpdateAccountForm, ResetPasswordForm, ResetRequestForm
from flask_app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import secrets
from itsdangerous import URLSafeTimedSerializer
import os
from flask_mail import Message
from flask_app.models import User


def generate_token(data):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(data)

def verify_reset_token(token, expiration=1800):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token, max_age=expiration)
        return data
    except:
        return None


@app.route('/')
@app.route('/index')
@login_required
def index():
    if current_user.is_authenticated:
        return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('game'))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            first_search = request.args.get('next')
            return redirect(first_search) if first_search else redirect(url_for('game'))
            flash('Logged in successfully!', 'success')
        else:
            flash('Login unsucessful. please check what you typing', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/game')
@login_required
def game():
    if current_user.is_authenticated:
        return render_template('game.html')


def save_picture(form_picture):
    random_hex = secret.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/chick', picture_fn)
    form_picture.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if current_user.is_authenticated:
        form = UpdateAccountForm()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
                current_user.username = form.username.data()
                current_user.email = form.email.data()
                db.session.commit()
                flash('you have update your account')
                return redirect(url_for('account'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
            image_file = url_for('static', filename= 'Cat/' + current_user.image_file) 
        return render_template('account.html', title='Account', form=form)


@app.errorhandler(404)
def errors_404(error):
    return render_template('error/404.html'), 404

@app.errorhandler(403)
def errors_403(error):
    return render_template('error/403.html'), 403

@app.errorhandler(500)
def errors_500(error):
    return render_template('error/500.html'), 500


@app.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = generate_token({'user_id': user.id})
        flash('An email has been sent with instructions to reset your passsword')
        reset_url = url_for('reset_password_request', token=token, _external=True)
        return redirect(url_for('login'))
    return render_template('resetRequest.html', title='Reset Password', form=form)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        token = generate_token({'email' : email})
        reset_url = url_for('reset_password_confirm', token=token, _external=True)
        subject = 'Reset your Password'
        body = f'Click the link below to reset your password:{reset_url}'
        recipients = [email]

        msg = Message(subject=subject, body=body, recipients=recipients)
        flash('An email with instructions to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template('resetRequest.html')

@app.route('/reset_password_confirm/<token>', methods=['GET', 'POST'])
def reset_password_confirm(token):
    data = verify_reset_token(token)
    if data:
        if request.method == 'POST':
            new_password = request.form.get('new_password')
            flash('Your passowrd has been successfully been reset', 'success')
            return redirect(url_for('login'))
        return render_template('reset_token.html')
    else:
        flash('Token is invalid', 'danger')
        return redirect(url_for('login'))