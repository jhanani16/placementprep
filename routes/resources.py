from flask import Blueprint, render_template, request
from database.db import db
from routes.auth import login_required

resources_bp = Blueprint('resources', __name__)

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
