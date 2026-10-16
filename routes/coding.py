from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from database.db import db
from routes.auth import login_required
from bson import ObjectId
from datetime import datetime

coding_bp = Blueprint('coding', __name__)

@coding_bp.route('/')
@login_required(role='student')
def index():
    topics = db.coding_problems.distinct("topic")
    problems = list(db.coding_problems.find())
    return render_template('student/coding.html', topics=topics, problems=problems)

@coding_bp.route('/problem/<problem_id>', methods=['GET', 'POST'])
@login_required(role='student')
def problem(problem_id):
    problem = db.coding_problems.find_one({"_id": ObjectId(problem_id)})
    
    if request.method == 'POST':
        code = request.form.get('code')
        language = request.form.get('language')
        
        db.coding_submissions.insert_one({
            "student_id": ObjectId(session['user_id']),
            "problem_id": ObjectId(problem_id),
            "problem_title": problem['title'],
            "code": code,
            "language": language,
            "status": "Submitted",
            "date": datetime.now()
        })
        
        db.progress.update_one(
            {"student_id": ObjectId(session['user_id'])},
            {"$inc": {"coding_attempted": 1}}
        )
        
        flash('Code submitted successfully!', 'success')
        return redirect(url_for('coding.index'))
        
    return render_template('student/coding_problem.html', problem=problem)
