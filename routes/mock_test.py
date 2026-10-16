from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from database.db import db
from routes.auth import login_required
from bson import ObjectId
from datetime import datetime

mock_test_bp = Blueprint('mock_test', __name__)

@mock_test_bp.route('/')
@login_required(role='student')
def index():
    tests = list(db.mock_tests.find())
    return render_template('student/mock_test.html', tests=tests)

@mock_test_bp.route('/take/<test_id>', methods=['GET', 'POST'])
@login_required(role='student')
def take_test(test_id):
    test = db.mock_tests.find_one({"_id": ObjectId(test_id)})
    
    if request.method == 'POST':
        score = 0
        total = len(test['questions'])
        
        for i, q in enumerate(test['questions']):
            ans = request.form.get(f'q_{i}')
            if ans == q['answer']:
                score += 1
                
        result_id = db.mock_results.insert_one({
            "student_id": ObjectId(session['user_id']),
            "test_id": ObjectId(test_id),
            "test_title": test['title'],
            "score": score,
            "total": total,
            "percentage": (score/total)*100 if total > 0 else 0,
            "date": datetime.now()
        }).inserted_id
        
        db.progress.update_one(
            {"student_id": ObjectId(session['user_id'])},
            {"$inc": {"mock_tests_completed": 1}}
        )
        
        return redirect(url_for('mock_test.result', result_id=result_id))
        
    return render_template('student/quiz.html', questions=test['questions'], category=test['title'], is_mock=True)

@mock_test_bp.route('/result/<result_id>')
@login_required(role='student')
def result(result_id):
    result = db.mock_results.find_one({"_id": ObjectId(result_id)})
    return render_template('student/mock_result.html', result=result)
