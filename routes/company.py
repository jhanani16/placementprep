from flask import Blueprint, render_template, request
from database.db import db
from routes.auth import login_required

company_bp = Blueprint('company', __name__)

@company_bp.route('/')
@login_required(role='student')
def index():
    search = request.args.get('search', '')
    if search:
        companies = list(db.companies.find({"name": {"$regex": search, "$options": "i"}}))
    else:
        companies = list(db.companies.find())
    return render_template('student/companies.html', companies=companies, search=search)
