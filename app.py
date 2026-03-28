from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, jsonify, session
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import random

app = Flask(__name__)

database_url = os.environ.get("DATABASE_URL")
if database_url:
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
else:
    database_url = "sqlite:///kisanseva.db"  # local run

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# ------- DATABASE MODELS -------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(15))
    location = db.Column(db.String(100))
    farm_size = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    pest_analyses = db.relationship('PestAnalysis', backref='user', lazy=True)
    forum_posts = db.relationship('ForumPost', backref='user', lazy=True)
    marketplace_listings = db.relationship('MarketplaceListing', backref='user', lazy=True)

class PestAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_path = db.Column(db.String(200))
    pest_detected = db.Column(db.String(100))
    confidence = db.Column(db.Integer)
    treatment_plan = db.Column(db.Text)
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)

class CropCalendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100))
    season = db.Column(db.String(50))
    planting_month = db.Column(db.String(20))
    harvest_month = db.Column(db.String(20))
    region = db.Column(db.String(50))
    tips = db.Column(db.Text)

class ForumPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    category = db.Column(db.String(50))
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    replies = db.relationship('ForumReply', backref='post', lazy=True)

class ForumReply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class MarketplaceListing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(200))
    category = db.Column(db.String(50))
    price = db.Column(db.Float)
    description = db.Column(db.Text)
    image_path = db.Column(db.String(200))
    stock = db.Column(db.Integer)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ------- STATIC DATA -------
PEST_DATABASE = {
    'Aphids': {
        'name_en': 'Aphids',
        'name_hi': 'माहू',
        'description': 'Small insects that suck plant sap and cause leaves to curl.',
        'treatments': [
            'Spray neem oil solution (5ml/L)',
            'Use yellow sticky traps',
            'Release ladybugs (natural predators)'
        ],
        'prevention': 'Avoid over-fertilizing and plant marigolds nearby.'
     },
    'Leaf Blight': {
        'name_en': 'Leaf Blight',
        'name_hi': 'पत्ती झुलसा',
        'description': 'Fungal disease causing brown leaf spots and wilting.',
        'treatments': [
            'Remove infected leaves',
            'Apply copper-based fungicide',
            'Ensure airflow between plants'
        ],
        'prevention': 'Avoid overhead irrigation and rotate crops yearly.'
    },
    'Caterpillar': {
        'name_en': 'Caterpillar',
        'name_hi': 'सुंडी',
        'description': 'Larvae feeding on leaves and stems of various crops.',
        'treatments': [
            'Use Bt spray or neem-based pesticide',
            'Handpick early-stage larvae',
            'Install pheromone traps'
        ],
        'prevention': 'Use solar insect traps and natural repellents.'
    }
}

CROP_CALENDAR_DATA = [
    {'crop': 'Wheat', 'season': 'Rabi', 'plant': 'Oct-Nov', 'harvest': 'Mar-Apr', 'region': 'Punjab, Haryana'},
    {'crop': 'Rice', 'season': 'Kharif', 'plant': 'Jun-Jul', 'harvest': 'Oct-Nov', 'region': 'Punjab, WB'},
    {'crop': 'Cotton', 'season': 'Kharif', 'plant': 'Apr-May', 'harvest': 'Oct-Dec', 'region': 'Gujarat, Punjab'},
]

# ------- ROUTES -------
@app.route('/')
def index():
    username = session.get('user')
    return render_template('login_landing.html', username=username)

@app.route('/dashboard')
def dashboard():
    if not session.get('user_id'):
        return redirect(url_for('login_register'))
    user = User.query.get(session['user_id'])
    analyses = PestAnalysis.query.filter_by(user_id=user.id).order_by(PestAnalysis.analyzed_at.desc()).limit(3).all()
    listings = MarketplaceListing.query.filter_by(user_id=user.id).all()
    return render_template('dashboard.html', user=user, analyses=analyses, listings=listings, username=session.get('user'))

# ------- LOGIN / REGISTER -------
@app.route('/login_register', methods=['GET', 'POST'])
def login_register():
    if request.method == 'POST':
        action = request.form.get('action')

        # ---- REGISTER ----
        if action == 'register':
            username = request.form['username']
            email = request.form['email']
            password = generate_password_hash(request.form['password'])

            if User.query.filter_by(email=email).first():
                flash('Email already registered.')
                return redirect(url_for('login_register'))
            if User.query.filter_by(username=username).first():
                flash('Username already exists.')
                return redirect(url_for('login_register'))

            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login_register'))

        # ---- LOGIN ----
        elif action == 'login':
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                session['user'] = user.username
                session['user_id'] = user.id
                flash('Login successful!')
                return redirect(url_for('index'))
            else:
                flash('Invalid credentials! Try again.')

    return render_template('login_register.html', username=session.get('user'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    flash('Logged out successfully!')
    return redirect(url_for('index'))

# ---- AI PEST DIAGNOSIS -------
@app.route('/ai-pest-diagnosis', methods=['GET', 'POST'])
def ai_pest_diagnosis():
    if request.method == 'POST':
        # ---------- IMAGE ----------
        file = request.files.get('image')
        if not file or file.filename == '':
            return jsonify({'error': 'No image selected'}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # ---------- AI DATA FROM FRONTEND ----------
        pest_name = request.form.get('pest_name')
        confidence = request.form.get('confidence')
        treatments = request.form.getlist('treatments[]')
        description = request.form.get('description')
        prevention = request.form.get('prevention')

        # ---------- FALLBACK (offline/demo mode) ----------
        if not pest_name or pest_name not in PEST_DATABASE:
            pest_name = random.choice(list(PEST_DATABASE.keys()))
            pest_info = PEST_DATABASE[pest_name]
            confidence = random.randint(88, 98)
            treatments = pest_info['treatments']
            description = pest_info['description']
            prevention = pest_info['prevention']
        else:
            pest_info = PEST_DATABASE.get(pest_name, {})

        # ---------- SAVE TO DB ----------
        if session.get('user_id'):
            analysis = PestAnalysis(
                user_id=session['user_id'],
                image_path=filepath,
                pest_detected=pest_name,
                confidence=int(confidence),
                treatment_plan=str(treatments)
            )
            db.session.add(analysis)
            db.session.commit()

        # ---------- RESPONSE ----------
        return jsonify({
            'pest_name': pest_info.get('name_en', pest_name),
            'confidence': confidence,
            'description': description,
            'treatments': treatments,
            'prevention': prevention
        })

    # ---------- PAGE ----------
    return render_template('ai_pest_diagnosis.html', username=session.get('user'))


@app.route('/crop-calendar')
def crop_calendar():
    season = request.args.get('season', 'All')
    if season == 'All':
        crops = CROP_CALENDAR_DATA
    else:
        crops = [c for c in CROP_CALENDAR_DATA if c['season'] == season]
    return render_template('crop_calendar.html', crops=crops, username=session.get('user'))

@app.route('/roi-calculator', methods=['GET', 'POST'])
def roi_calculator():
    results = None
    if request.method == 'POST':
        farm_size = float(request.form.get('farm_size', 1))
        pesticide_cost = float(request.form.get('pesticide_cost', 5000))
        trap_cost = float(request.form.get('trap_cost', 3000))

        annual_pesticide_cost = pesticide_cost * 3
        trap_total = trap_cost * farm_size
        lifespan = 5
        savings_year = annual_pesticide_cost - (trap_total / lifespan)
        total_savings = savings_year * lifespan
        roi = (total_savings / trap_total) * 100

        results = {
            'farm_size': farm_size,
            'annual_cost': annual_pesticide_cost,
            'investment': trap_total,
            'annual_savings': savings_year,
            'total_savings': total_savings,
            'roi_percentage': round(roi, 2),
            'payback_period': round(trap_total / savings_year, 1)
        }
    return render_template('roi_calculator.html', results=results, username=session.get('user'))

@app.route('/knowledge-exchange', methods=['GET', 'POST'])
def knowledge_exchange():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form.get('category', 'general')

        post = ForumPost(user_id=session.get('user_id', 1),
                         title=title, content=content, category=category)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!')
        return redirect(url_for('knowledge_exchange'))

    posts = ForumPost.query.order_by(ForumPost.created_at.desc()).all()
    return render_template('knowledge_exchange.html', posts=posts, username=session.get('user'))

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    if request.method == 'POST':
        reply = ForumReply(post_id=post.id,
                           user_id=session.get('user_id', 1),
                           content=request.form['reply'])
        db.session.add(reply)
        db.session.commit()
        flash('Reply added!')
        return redirect(url_for('view_post', post_id=post.id))
    return render_template('view_post.html', post=post, username=session.get('user'))

@app.route('/marketplace')
def marketplace():
    category = request.args.get('category', 'all')
    if category == 'all':
        listings = MarketplaceListing.query.order_by(MarketplaceListing.created_at.desc()).all()
    else:
        listings = MarketplaceListing.query.filter_by(category=category).all()
    return render_template('marketplace.html', listings=listings, username=session.get('user'))

@app.route('/marketplace/add', methods=['GET', 'POST'])
def add_listing():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        price = float(request.form['price'])
        description = request.form['description']
        stock = int(request.form['stock'])
        location = request.form['location']

        listing = MarketplaceListing(
            user_id=session.get('user_id', 1),
            title=title, category=category, price=price,
            description=description, stock=stock, location=location
        )
        db.session.add(listing)
        db.session.commit()
        flash('Listing added successfully!')
        return redirect(url_for('marketplace'))
    return render_template('add_listing.html', username=session.get('user'))

@app.route('/language_support')
def language_support():
    return render_template('language_support.html', username=session.get('user'))

@app.route('/product_details')
def product_details():
    return render_template('product_details.html', username=session.get('user'))

if __name__ != "__main__":
    with app.app_context():
        db.create_all()