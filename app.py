from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')
app.config['SECRET_KEY'] = 'a_super_secret_key'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    images = db.relationship('Image', backref='user', lazy=True)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    images = Image.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', images=images)

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'image' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('profile'))
    file = request.files['image']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('profile'))
    if file:
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}-{filename}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
        new_image = Image(filename=unique_filename, user_id=current_user.id)
        db.session.add(new_image)
        db.session.commit()
        flash('Image uploaded successfully!', 'success')
        return redirect(url_for('profile'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete_image/<int:image_id>')
@login_required
def delete_image(image_id):
    image = Image.query.get_or_404(image_id)
    if image.user_id != current_user.id:
        flash('You do not have permission to delete this image.', 'danger')
        return redirect(url_for('profile'))
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
    db.session.delete(image)
    db.session.commit()
    flash('Image deleted successfully.', 'success')
    return redirect(url_for('profile'))

@app.route('/image/<filename>')
def image(filename):
    image = Image.query.filter_by(filename=filename).first_or_404()
    return render_template('image.html', image=image)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
