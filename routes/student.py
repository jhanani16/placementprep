from flask import Blueprint, render_template, session
from database.db import db
from routes.auth import login_required
from bson import ObjectId

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard')
@login_required(role='student')
def dashboard():
    user_id = ObjectId(session['user_id'])
    
    # Get user progress
    progress = db.progress.find_one({"student_id": user_id}) or {}
    
    # Get recent tests
    recent_quizzes = list(db.quiz_results.find({"student_id": user_id}).sort("date", -1).limit(5))
    
    # Coding submissions
    coding_subs = list(db.coding_submissions.find({"student_id": user_id}).sort("date", -1).limit(5))
    
    return render_template('student/dashboard.html', 
                           progress=progress, 
                           recent_quizzes=recent_quizzes,
                           coding_subs=coding_subs)
