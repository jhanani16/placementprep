from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from database.db import db
from routes.auth import login_required
from bson import ObjectId

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required(role='admin')
def dashboard():
    stats = {
        "total_students": db.users.count_documents({"role": "student"}),
        "total_aptitude": db.aptitude_questions.count_documents({}),
        "total_coding": db.coding_problems.count_documents({}),
        "total_companies": db.companies.count_documents({}),
        "total_mock_tests": db.mock_results.count_documents({})
    }
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/students')
@login_required(role='admin')
def students():
    student_list = list(db.users.find({"role": "student"}))
    return render_template('admin/students.html', students=student_list)

@admin_bp.route('/aptitude', methods=['GET', 'POST'])
@login_required(role='admin')
def aptitude():
    if request.method == 'POST':
        # Add question
        data = {
            "question": request.form.get('question'),
            "options": [request.form.get('opt1'), request.form.get('opt2'), request.form.get('opt3'), request.form.get('opt4')],
            "answer": request.form.get('answer'),
            "explanation": request.form.get('explanation'),
            "category": request.form.get('category'),
            "difficulty": request.form.get('difficulty')
        }
        db.aptitude_questions.insert_one(data)
        flash('Question added successfully', 'success')
        return redirect(url_for('admin.aptitude'))
        
    questions = list(db.aptitude_questions.find())
    return render_template('admin/aptitude.html', questions=questions)

@admin_bp.route('/aptitude/delete/<q_id>')
@login_required(role='admin')
def delete_aptitude(q_id):
    db.aptitude_questions.delete_one({"_id": ObjectId(q_id)})
    flash('Question deleted.', 'success')
    return redirect(url_for('admin.aptitude'))

@admin_bp.route('/coding', methods=['GET', 'POST'])
@login_required(role='admin')
def coding():
    if request.method == 'POST':
        data = {
            "title": request.form.get('title'),
            "description": request.form.get('description'),
            "difficulty": request.form.get('difficulty'),
            "topic": request.form.get('topic'),
            "example_input": request.form.get('example_input'),
            "example_output": request.form.get('example_output'),
            "constraints": request.form.get('constraints'),
            "expected_approach": request.form.get('expected_approach')
        }
        db.coding_problems.insert_one(data)
        flash('Problem added successfully', 'success')
        return redirect(url_for('admin.coding'))
        
    problems = list(db.coding_problems.find())
    return render_template('admin/coding.html', problems=problems)

@admin_bp.route('/coding/delete/<p_id>')
@login_required(role='admin')
def delete_coding(p_id):
    db.coding_problems.delete_one({"_id": ObjectId(p_id)})
    flash('Problem deleted.', 'success')
    return redirect(url_for('admin.coding'))

@admin_bp.route('/interview', methods=['GET', 'POST'])
@login_required(role='admin')
def interview():
    if request.method == 'POST':
        data = {
            "question": request.form.get('question'),
            "category": request.form.get('category'),
            "model_answer": request.form.get('model_answer'),
            "difficulty": request.form.get('difficulty')
        }
        db.interview_questions.insert_one(data)
        flash('Question added', 'success')
        return redirect(url_for('admin.interview'))
        
    questions = list(db.interview_questions.find())
    return render_template('admin/interview.html', questions=questions)

@admin_bp.route('/interview/delete/<q_id>')
@login_required(role='admin')
def delete_interview(q_id):
    db.interview_questions.delete_one({"_id": ObjectId(q_id)})
    flash('Question deleted.', 'success')
    return redirect(url_for('admin.interview'))

@admin_bp.route('/companies', methods=['GET', 'POST'])
@login_required(role='admin')
def companies():
    if request.method == 'POST':
        data = {
            "name": request.form.get('name'),
            "description": request.form.get('description'),
            "job_roles": request.form.get('job_roles'),
            "skills": request.form.get('skills'),
            "eligibility": request.form.get('eligibility'),
            "selection_process": request.form.get('selection_process'),
            "difficulty": request.form.get('difficulty'),
            "frequently_asked": request.form.get('frequently_asked'),
            "interview_questions": request.form.get('interview_questions')
        }
        db.companies.insert_one(data)
        flash('Company added', 'success')
        return redirect(url_for('admin.companies'))
        
    companies = list(db.companies.find())
    return render_template('admin/companies.html', companies=companies)

@admin_bp.route('/companies/delete/<c_id>')
@login_required(role='admin')
def delete_company(c_id):
    db.companies.delete_one({"_id": ObjectId(c_id)})
    flash('Company deleted.', 'success')
    return redirect(url_for('admin.companies'))

@admin_bp.route('/resources', methods=['GET', 'POST'])
@login_required(role='admin')
def resources():
    if request.method == 'POST':
        data = {
            "title": request.form.get('title'),
            "description": request.form.get('description'),
            "category": request.form.get('category'),
            "content": request.form.get('content'),
            "date_added": request.form.get('date_added')
        }
        db.resources.insert_one(data)
        flash('Resource added', 'success')
        return redirect(url_for('admin.resources'))
        
    resources = list(db.resources.find())
    return render_template('admin/resources.html', resources=resources)

@admin_bp.route('/resources/delete/<r_id>')
@login_required(role='admin')
def delete_resource(r_id):
    db.resources.delete_one({"_id": ObjectId(r_id)})
    flash('Resource deleted.', 'success')
    return redirect(url_for('admin.resources'))
