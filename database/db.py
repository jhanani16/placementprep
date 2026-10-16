from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
try:
    db = client.get_default_database()
except Exception:
    db = client['placement_db']
if db is None:
    db = client['placement_db']

# Optional: Access specific collections if needed globally, but better accessed via db.collection_name
users = db.users
aptitude_questions = db.aptitude_questions
quiz_results = db.quiz_results
coding_problems = db.coding_problems
coding_submissions = db.coding_submissions
interview_questions = db.interview_questions
mock_tests = db.mock_tests
mock_results = db.mock_results
companies = db.companies
resources = db.resources
resumes = db.resumes
bookmarks = db.bookmarks
progress = db.progress
