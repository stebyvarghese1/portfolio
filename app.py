from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'),
                               'favicon_icon_1766679969783.png', mimetype='image/png')

app.config['SECRET_KEY'] = 'steby_secret_key_2025'

# Database configuration - use PostgreSQL if DATABASE_URL is set, otherwise fallback to SQLite
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # SQL Alchemy requires postgresql:// instead of postgres://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(500))
    image_url = db.Column(db.String(500))
    link = db.Column(db.String(500))

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50)) # e.g., Programming, Frameworks

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(100), nullable=False)
    institution = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50))

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_url = db.Column(db.String(500))
    about_image_url = db.Column(db.String(500))
    name = db.Column(db.String(100))
    tagline = db.Column(db.String(200))

# Routes
@app.route('/')
def index():
    projects = Project.query.all()
    skills = Skill.query.all()
    education = Education.query.all()
    profile = Profile.query.first()
    return render_template('index.html', projects=projects, skills=skills, education=education, profile=profile)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('admin'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    projects = Project.query.all()
    skills = Skill.query.all()
    education = Education.query.all()
    profile = Profile.query.first()
    current_admin = User.query.get(session['user_id'])
    return render_template('admin.html', projects=projects, skills=skills, education=education, profile=profile, current_admin=current_admin)

@app.route('/admin/profile/update', methods=['POST'])
def update_profile():
    if 'user_id' not in session: return redirect(url_for('login'))
    profile = Profile.query.first()
    if not profile:
        profile = Profile()
        db.session.add(profile)
    
    profile.photo_url = request.form.get('photo_url')
    profile.about_image_url = request.form.get('about_image_url')
    
    db.session.commit()
    flash('Profile updated successfully')
    return redirect(url_for('admin'))

@app.route('/admin/project/add', methods=['POST'])
def add_project():
    if 'user_id' not in session: return redirect(url_for('login'))
    new_project = Project(
        title=request.form.get('title'),
        description=request.form.get('description'),
        technologies=request.form.get('technologies'),
        image_url=request.form.get('image_url'),
        link=request.form.get('link')
    )
    db.session.add(new_project)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/project/delete/<int:id>')
def delete_project(id):
    if 'user_id' not in session: return redirect(url_for('login'))
    project = Project.query.get(id)
    if project:
        db.session.delete(project)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/skill/add', methods=['POST'])
def add_skill():
    if 'user_id' not in session: return redirect(url_for('login'))
    name = request.form.get('name')
    category = request.form.get('category')
    if name:
        new_skill = Skill(name=name, category=category)
        db.session.add(new_skill)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/skill/delete/<int:id>')
def delete_skill(id):
    if 'user_id' not in session: return redirect(url_for('login'))
    skill = Skill.query.get(id)
    if skill:
        db.session.delete(skill)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/education/add', methods=['POST'])
def add_education():
    if 'user_id' not in session: return redirect(url_for('login'))
    degree = request.form.get('degree')
    institution = request.form.get('institution')
    duration = request.form.get('duration')
    if degree and institution:
        new_edu = Education(degree=degree, institution=institution, duration=duration)
        db.session.add(new_edu)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/education/delete/<int:id>')
def delete_education(id):
    if 'user_id' not in session: return redirect(url_for('login'))
    edu = Education.query.get(id)
    if edu:
        db.session.delete(edu)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/credentials/update', methods=['POST'])
def update_credentials():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    new_username = request.form.get('username')
    new_password = request.form.get('password')
    
    if new_username:
        # Check if username is taken by another user
        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user and existing_user.id != user.id:
            flash('Username already taken')
            return redirect(url_for('admin'))
        user.username = new_username
        
    if new_password:
        user.password = generate_password_hash(new_password)
        
    db.session.commit()
    flash('Credentials updated successfully')
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Migrations for existing PostgreSQL databases
        try:
            # Increase password length
            db.session.execute(db.text('ALTER TABLE "user" ALTER COLUMN password TYPE VARCHAR(500)'))
            # Increase project field lengths
            db.session.execute(db.text('ALTER TABLE project ALTER COLUMN title TYPE VARCHAR(200)'))
            db.session.execute(db.text('ALTER TABLE project ALTER COLUMN technologies TYPE VARCHAR(500)'))
            db.session.execute(db.text('ALTER TABLE project ALTER COLUMN image_url TYPE VARCHAR(500)'))
            db.session.execute(db.text('ALTER TABLE project ALTER COLUMN link TYPE VARCHAR(500)'))
            
            db.session.execute(db.text('ALTER TABLE profile ADD COLUMN IF NOT EXISTS about_image_url VARCHAR(500)'))
            db.session.commit()
        except Exception as e:
            print(f"Migration notice: {e}")
            db.session.rollback()
            
        # Ensure at least one Profile record exists
        if not Profile.query.first():
            db.session.add(Profile(
                photo_url='/static/img/favicon_icon_1766679969783.png',
                about_image_url='/static/img/favicon_icon_1766679969783.png',
                name='STEBY VARGHESE',
                tagline='Aspiring Agentic AI Developer & MCA Candidate'
            ))
            db.session.commit()

        # Create default admin if not exists
        if not User.query.filter_by(username='admin').first():
            hashed_pw = generate_password_hash('admin123')
            admin_user = User(username='admin', password=hashed_pw)
            db.session.add(admin_user)
            
            # Seed initial data from resume
            # Education
            db.session.add(Education(degree='Master of Computer Applications (Pursuing)', institution='CCSIT of Calicut University', duration='2024 - 2026'))
            db.session.add(Education(degree='Bachelor of Computer Applications', institution='Yuvakshetra institute of management studies', duration='2021 - 2024'))
            
            # Skills
            skills_data = [
                ('Python', 'Programming'), ('HTML', 'Programming'), ('CSS', 'Programming'),
                ('Flask', 'Frameworks'), ('Django', 'Frameworks'), ('Kivy', 'Frameworks'),
                ('UI/UX Design', 'Tools'), ('Figma', 'Tools'), ('VS Code', 'Tools')
            ]
            for name, cat in skills_data:
                db.session.add(Skill(name=name, category=cat))
            
            # Projects
            db.session.add(Project(
                title='Virtual Mouse Using Hand Gestures',
                description='Real-time computer vision–driven virtual mouse using MediaPipe and OpenCV.',
                technologies='Python, OpenCV, MediaPipe',
                image_url='https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&q=80&w=800',
                link='#'
            ))
            db.session.add(Project(
                title='Open-source SOC Platform',
                description='Security Operations Center platform with real-time threat monitoring and AI-based detection.',
                technologies='Flask, Flask-SocketIO, MongoDB, NLP',
                image_url='https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=800',
                link='#'
            ))
            db.session.add(Project(
                title='Camdroid',
                description='Mobile app transforming smartphone into a wireless webcam with QR pairing.',
                technologies='Python, Kivy, Socket',
                image_url='https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&q=80&w=800',
                link='#'
            ))

            # Initial Profile
            db.session.add(Profile(
                photo_url='/static/img/favicon_icon_1766679969783.png',
                about_image_url='/static/img/favicon_icon_1766679969783.png',
                name='STEBY VARGHESE',
                tagline='Aspiring Agentic AI Developer & MCA Candidate'
            ))
            
            db.session.commit()
            
    app.run(debug=True)
