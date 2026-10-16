# Placement Preparation Platform

A comprehensive web application designed to help college students prepare for campus placements, featuring aptitude tests, coding challenges, interview preparation, mock tests, company profiles, resources, and resume building.

## Tech Stack
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5, Jinja2 Templates
- **Backend**: Python Flask
- **Database**: MongoDB (via PyMongo)
- **Authentication**: Session-based, Werkzeug Password Hashing

## Setup Instructions (Windows)

1. **Install Python**: Make sure Python (3.8+) is installed on your system.
2. **Install MongoDB**: Ensure you have a local MongoDB instance running on port `27017` or update the `.env` file with your MongoDB Atlas URI.
3. **Clone/Download the Project**: Navigate to the project directory in your terminal/command prompt.

### 4. Setup Virtual Environment
Run the following commands in the project directory:

```bash
python -m venv venv
venv\Scripts\activate
```

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables
A `.env` file is already created. By default, it uses:
```
MONGO_URI=mongodb://localhost:27017/placement_db
SECRET_KEY=super_secret_key_change_in_production
```
Make sure your MongoDB server is running if using `localhost`.

### 7. Seed Database (Optional but recommended)
Run the seed script to populate the database with sample data and create the default admin account:
```bash
python seed.py
```
**Admin Credentials:**
- Email: `admin@example.com`
- Password: `admin123`

### 8. Run the Application
```bash
python app.py
```
The application will start running at `http://127.0.0.1:5000/`.

## Features
- **Student Dashboard**: Track progress and recent activity.
- **Aptitude Practice**: Categorized quizzes with automatic scoring.
- **Coding Practice**: Solve algorithms and submit code.
- **Interview Preparation**: HR and Technical questions with model answers.
- **Mock Tests**: Full-length tests combining different topics.
- **Company Profiles**: Info on selection processes and commonly asked questions.
- **Study Resources**: Notes and roadmaps.
- **Resume Builder**: Generate a quick formatted resume.
- **Admin Dashboard**: Full CRUD management over all platform content.
