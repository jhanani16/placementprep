from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from database.db import db
from routes.auth import login_required
from bson import ObjectId
from datetime import datetime

aptitude_bp = Blueprint('aptitude', __name__)

@aptitude_bp.route('/')
@login_required(role='student')
def index():
    categories = db.aptitude_questions.distinct("category")
    return render_template('student/aptitude.html', categories=categories)

@aptitude_bp.route('/quiz/<category>', methods=['GET', 'POST'])
@login_required(role='student')
def quiz(category):
    if request.method == 'POST':
        user_id = ObjectId(session['user_id'])
        score = 0
        total = 0
        
        # Calculate score
        for key, value in request.form.items():
            if key.startswith('q_'):
                q_id = ObjectId(key.split('_')[1])
                question = db.aptitude_questions.find_one({"_id": q_id})
                if question and question['answer'] == value:
                    score += 1
                total += 1
        
        # Save result
        result_id = db.quiz_results.insert_one({
            "student_id": user_id,
            "category": category,
            "score": score,
            "total": total,
            "percentage": (score/total)*100 if total > 0 else 0,
            "date": datetime.now()
        }).inserted_id
        
        # Update progress
        db.progress.update_one(
            {"student_id": user_id},
            {"$inc": {"aptitude_attempted": 1}}
        )
        
        return redirect(url_for('aptitude.result', result_id=result_id))
        
    questions = list(db.aptitude_questions.find({"category": category}))
    return render_template('student/quiz.html', questions=questions, category=category)

@aptitude_bp.route('/result/<result_id>')
@login_required(role='student')
def result(result_id):
    result = db.quiz_results.find_one({"_id": ObjectId(result_id)})
    return render_template('student/quiz_result.html', result=result)
