from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    grade = db.Column(db.String(10))
    target_exam = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.String(10), nullable=True)
    exam = db.Column(db.String(20), nullable=True)
    difficulty = db.Column(db.String(10), default="easy")
    url = db.Column(db.String(500), nullable=False)
    resource_type = db.Column(db.String(20), default="other")  # pdf, youtube, other
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), nullable=False)
    exam = db.Column(db.String(20), nullable=False)
    difficulty = db.Column(db.String(10), default="easy")
    prompt = db.Column(db.Text, nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    options = db.Column(db.Text, nullable=False)  # comma-separated options
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class StudyPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    item_type = db.Column(db.String(20), nullable=False)  # resource / quiz
    ref_id = db.Column(db.Integer, nullable=False)
    extra_score = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class WeeklyStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    week_start = db.Column(db.Date, nullable=False)
    resources_completed = db.Column(db.Integer, default=0)
    quizzes_attempted = db.Column(db.Integer, default=0)
    quizzes_correct = db.Column(db.Integer, default=0)
    study_hours = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_accuracy(self):
        if self.quizzes_attempted == 0:
            return 0
        return (self.quizzes_correct / self.quizzes_attempted) * 100