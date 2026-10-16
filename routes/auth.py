from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import db
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def login_required(role=None):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in first.', 'danger')
                return redirect(url_for('auth.login'))
            if role and session.get('role') != role:
                flash('Unauthorized access.', 'danger')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        college = request.form.get('college')
        department = request.form.get('department')
        year = request.form.get('year')
        phone = request.form.get('phone')

        if db.users.find_one({"email": email}):
            flash('Email already registered', 'danger')
            return redirect(url_for('auth.register'))
        
        hashed_password = generate_password_hash(password)
        
        user_id = db.users.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password,
            "college": college,
            "department": department,
            "year": int(year),
            "phone": phone,
            "role": "student"
        }).inserted_id
        
        # Initialize progress tracking
        db.progress.insert_one({
            "student_id": user_id,
            "aptitude_attempted": 0,
            "coding_attempted": 0,
            "mock_tests_completed": 0
        })

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = db.users.find_one({"email": email})
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['role'] = user['role']
            session['name'] = user['name']
            
            if user['role'] == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('student.dashboard'))
        else:
            flash('Invalid email or password', 'danger')
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('auth.login'))
