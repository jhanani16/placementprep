from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from database.db import db
from routes.auth import login_required
from bson import ObjectId

resume_bp = Blueprint('resume', __name__)

@resume_bp.route('/', methods=['GET', 'POST'])
@login_required(role='student')
def index():
    user_id = ObjectId(session['user_id'])
    
    if request.method == 'POST':
        resume_data = {
            "student_id": user_id,
            "objective": request.form.get('objective'),
            "education": request.form.get('education'),
            "skills": request.form.get('skills'),
            "projects": request.form.get('projects'),
            "certifications": request.form.get('certifications'),
            "achievements": request.form.get('achievements')
        }
        
        db.resumes.update_one({"student_id": user_id}, {"$set": resume_data}, upsert=True)
        flash('Resume updated successfully!', 'success')
        return redirect(url_for('resume.index'))
        
    resume = db.resumes.find_one({"student_id": user_id}) or {}
    user = db.users.find_one({"_id": user_id})
    return render_template('student/resume.html', resume=resume, user=user)
