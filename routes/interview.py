from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from database.db import db
from routes.auth import login_required
from bson import ObjectId

interview_bp = Blueprint('interview', __name__)

@interview_bp.route('/')
@login_required(role='student')
def index():
    categories = db.interview_questions.distinct("category")
    questions = list(db.interview_questions.find())
    
    # Get user bookmarks
    user_bookmarks = db.bookmarks.find_one({"student_id": ObjectId(session['user_id'])}) or {"questions": []}
    
    return render_template('student/interview.html', categories=categories, questions=questions, bookmarks=user_bookmarks['questions'])

@interview_bp.route('/bookmark/<question_id>', methods=['POST'])
@login_required(role='student')
def bookmark(question_id):
    user_id = ObjectId(session['user_id'])
    
    bookmark_doc = db.bookmarks.find_one({"student_id": user_id})
    if not bookmark_doc:
        db.bookmarks.insert_one({"student_id": user_id, "questions": [question_id]})
    else:
        if question_id in bookmark_doc['questions']:
            db.bookmarks.update_one({"student_id": user_id}, {"$pull": {"questions": question_id}})
        else:
            db.bookmarks.update_one({"student_id": user_id}, {"$push": {"questions": question_id}})
            
    return redirect(url_for('interview.index'))
