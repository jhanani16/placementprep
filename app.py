import os
from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import db
from functools import wraps
from bson import ObjectId
from datetime import datetime
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# ---------------------------------------------------------
# AUTHENTICATION DECORATOR
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# BLUEPRINTS
# ---------------------------------------------------------
auth_bp = Blueprint('auth', __name__)
student_bp = Blueprint('student', __name__)
aptitude_bp = Blueprint('aptitude', __name__)
coding_bp = Blueprint('coding', __name__)
interview_bp = Blueprint('interview', __name__)
mock_test_bp = Blueprint('mock_test', __name__)
company_bp = Blueprint('company', __name__)
resources_bp = Blueprint('resources', __name__)
resume_bp = Blueprint('resume', __name__)
admin_bp = Blueprint('admin', __name__)

# ==========================================
# AUTH ROUTES
# ==========================================
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

# ==========================================
# STUDENT DASHBOARD ROUTES
# ==========================================
@student_bp.route('/dashboard')
@login_required(role='student')
def dashboard():
    user_id = ObjectId(session['user_id'])
    progress = db.progress.find_one({"student_id": user_id}) or {}
    recent_quizzes = list(db.quiz_results.find({"student_id": user_id}).sort("date", -1).limit(5))
    coding_subs = list(db.coding_submissions.find({"student_id": user_id}).sort("date", -1).limit(5))
    return render_template('student/dashboard.html', progress=progress, recent_quizzes=recent_quizzes, coding_subs=coding_subs)

# ==========================================
# APTITUDE ROUTES
# ==========================================
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
        for key, value in request.form.items():
            if key.startswith('q_'):
                q_id = ObjectId(key.split('_')[1])
                question = db.aptitude_questions.find_one({"_id": q_id})
                if question and question['answer'] == value:
                    score += 1
                total += 1
        
        result_id = db.quiz_results.insert_one({
            "student_id": user_id,
            "category": category,
            "score": score,
            "total": total,
            "percentage": (score/total)*100 if total > 0 else 0,
            "date": datetime.now()
        }).inserted_id
        
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

# ==========================================
# CODING ROUTES
# ==========================================
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

# ==========================================
# INTERVIEW ROUTES
# ==========================================
@interview_bp.route('/')
@login_required(role='student')
def index():
    categories = db.interview_questions.distinct("category")
    questions = list(db.interview_questions.find())
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

# ==========================================
# MOCK TEST ROUTES
# ==========================================
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

# ==========================================
# COMPANY ROUTES
# ==========================================
@company_bp.route('/')
@login_required(role='student')
def index():
    search = request.args.get('search', '')
    if search:
        companies = list(db.companies.find({"name": {"$regex": search, "$options": "i"}}))
    else:
        companies = list(db.companies.find())
    return render_template('student/companies.html', companies=companies, search=search)

# ==========================================
# RESOURCES ROUTES
# ==========================================
@resources_bp.route('/')
@login_required(role='student')
def index():
    search = request.args.get('search', '')
    if search:
        resources = list(db.resources.find({"title": {"$regex": search, "$options": "i"}}))
    else:
        resources = list(db.resources.find())
    categories = db.resources.distinct("category")
    return render_template('student/resources.html', resources=resources, search=search, categories=categories)

# ==========================================
# RESUME ROUTES
# ==========================================
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

# ==========================================
# ADMIN ROUTES
# ==========================================
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


# ---------------------------------------------------------
# REGISTRATION & MAIN
# ---------------------------------------------------------
app.register_blueprint(auth_bp)
app.register_blueprint(student_bp, url_prefix='/student')
app.register_blueprint(aptitude_bp, url_prefix='/aptitude')
app.register_blueprint(coding_bp, url_prefix='/coding')
app.register_blueprint(interview_bp, url_prefix='/interview')
app.register_blueprint(mock_test_bp, url_prefix='/mock_test')
app.register_blueprint(company_bp, url_prefix='/companies')
app.register_blueprint(resources_bp, url_prefix='/resources')
app.register_blueprint(resume_bp, url_prefix='/resume')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
