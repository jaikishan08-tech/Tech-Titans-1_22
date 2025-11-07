from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, date, timedelta
from models import db, User, Resource, Question, StudyPlan, Progress, WeeklyStats
import random
import re
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///edutrack.db'
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/pdfs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'pdf'}

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def detect_resource_type(url):
    """Detect resource type from URL"""
    url_lower = url.lower()
    if 'youtube.com' in url_lower or 'youtu.be' in url_lower:
        return 'youtube'
    elif url_lower.endswith('.pdf') or 'pdf' in url_lower:
        return 'pdf'
    else:
        return 'other'

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_pdf(file):
    """Save uploaded PDF file and return the URL path"""
    if file and allowed_file(file.filename):
        # Create uploads directory if it doesn't exist
        upload_folder = app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        # Secure the filename
        filename = secure_filename(file.filename)
        # Add timestamp to avoid conflicts
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        
        # Save file
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Return URL path (relative to static folder)
        return url_for('static', filename=f'pdfs/{filename}')
    return None

def get_week_start(date_obj):
    """Get the Monday of the week for a given date"""
    days_since_monday = date_obj.weekday()
    return date_obj - timedelta(days=days_since_monday)

def update_weekly_stats(user_id):
    """Update or create weekly stats for the current week"""
    today = date.today()
    week_start = get_week_start(today)
    
    # Get or create weekly stats
    weekly_stat = WeeklyStats.query.filter_by(
        user_id=user_id,
        week_start=week_start
    ).first()
    
    if not weekly_stat:
        weekly_stat = WeeklyStats(
            user_id=user_id,
            week_start=week_start
        )
        db.session.add(weekly_stat)
    
    # Calculate stats for this week
    week_end = week_start + timedelta(days=6)
    
    # Resources completed this week
    resources = Progress.query.filter(
        Progress.user_id == user_id,
        Progress.item_type == 'resource',
        Progress.timestamp >= datetime.combine(week_start, datetime.min.time()),
        Progress.timestamp <= datetime.combine(week_end, datetime.max.time())
    ).count()
    
    # Quizzes attempted this week
    quizzes = Progress.query.filter(
        Progress.user_id == user_id,
        Progress.item_type == 'quiz',
        Progress.timestamp >= datetime.combine(week_start, datetime.min.time()),
        Progress.timestamp <= datetime.combine(week_end, datetime.max.time())
    ).all()
    
    quizzes_attempted = len(quizzes)
    quizzes_correct = sum(1 for q in quizzes if q.extra_score == 1)
    
    weekly_stat.resources_completed = resources
    weekly_stat.quizzes_attempted = quizzes_attempted
    weekly_stat.quizzes_correct = quizzes_correct
    # Estimate study hours (1 resource = 0.5 hours, 1 quiz = 0.25 hours)
    weekly_stat.study_hours = (resources * 0.5) + (quizzes_attempted * 0.25)
    
    db.session.commit()
    return weekly_stat

# Initialize database
@app.cli.command('init-db')
def init_db():
    """Initialize database with sample data"""
    with app.app_context():
        # Create all tables including WeeklyStats
        db.create_all()
        print("✓ All database tables created")
        
        # Add resource_type column if it doesn't exist (migration)
        try:
            from sqlalchemy import inspect, text
            inspector = inspect(db.engine)
            
            try:
                columns = [col['name'] for col in inspector.get_columns('resource')]
                if 'resource_type' not in columns:
                    with db.engine.begin() as conn:
                        conn.execute(text('ALTER TABLE resource ADD COLUMN resource_type VARCHAR(20) DEFAULT "other"'))
                    print("✓ Added resource_type column to resource table")
            except Exception:
                pass
            
            # Verify WeeklyStats table
            try:
                inspector.get_columns('weekly_stats')
                print("✓ WeeklyStats table verified")
            except Exception:
                db.create_all()
                print("✓ WeeklyStats table created")
        except Exception as e:
            print(f"Migration note: {e}")
            db.create_all()
    
    # Create admin user
    if not User.query.filter_by(email='admin@edutrack.local').first():
        admin = User(
            name='Admin',
            email='admin@edutrack.local',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
    
    # Create student user
    if not User.query.filter_by(email='student@edutrack.local').first():
        student = User(
            name='Student',
            email='student@edutrack.local',
            password_hash=generate_password_hash('student123'),
            grade='12',
            target_exam='JEE'
        )
        db.session.add(student)
    
    # Add sample resources
    if Resource.query.count() == 0:
        resources = [
            Resource(title='Algebra Basics', subject='Math', grade='10', difficulty='easy', url='https://youtube.com/watch?v=example1', resource_type='youtube'),
            Resource(title='Organic Chemistry', subject='Chemistry', exam='JEE', difficulty='medium', url='https://youtube.com/watch?v=example2', resource_type='youtube'),
            Resource(title='Physics Mechanics', subject='Physics', exam='NEET', difficulty='hard', url='https://youtube.com/watch?v=example3', resource_type='youtube'),
        ]
        db.session.add_all(resources)
    
    # Add sample questions
    if Question.query.count() == 0:
        questions = [
            Question(subject='Math', exam='JEE', difficulty='easy', prompt='What is 2+2?', answer='4', options='2,3,4,5'),
            Question(subject='Chemistry', exam='NEET', difficulty='medium', prompt='What is the atomic number of Carbon?', answer='6', options='5,6,7,8'),
            Question(subject='Physics', exam='JEE', difficulty='hard', prompt='What is the speed of light?', answer='3x10^8 m/s', options='3x10^8 m/s,3x10^7 m/s,3x10^9 m/s,3x10^6 m/s'),
        ]
        db.session.add_all(questions)
    
    db.session.commit()
    print("Database initialized with sample data!")

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        grade = request.form.get('grade')
        target_exam = request.form.get('target_exam') or None
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            grade=grade,
            target_exam=target_exam
        )
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Count completed resources
    completed_resources = Progress.query.filter_by(
        user_id=current_user.id,
        item_type='resource'
    ).count()
    
    total_resources = Resource.query.count()
    
    # Count quiz attempts
    quiz_attempts = Progress.query.filter_by(
        user_id=current_user.id,
        item_type='quiz'
    ).count()
    
    total_quizzes = Question.query.count()
    
    # Simple achievements
    achievements = []
    if completed_resources >= 5:
        achievements.append('Resource Explorer')
    if quiz_attempts >= 10:
        achievements.append('Quiz Master')
    if completed_resources >= 10 and quiz_attempts >= 20:
        achievements.append('Dedicated Learner')
    
    return render_template('dashboard.html',
                         completed_resources=completed_resources,
                         total_resources=total_resources,
                         quiz_attempts=quiz_attempts,
                         total_quizzes=total_quizzes,
                         achievements=achievements)

@app.route('/resources')
@login_required
def resources():
    subject = request.args.get('subject', '')
    difficulty = request.args.get('difficulty', '')
    
    query = Resource.query
    
    if subject:
        query = query.filter_by(subject=subject)
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    
    # Filter by user's grade/exam if available
    if current_user.grade:
        query = query.filter((Resource.grade == current_user.grade) | (Resource.grade == None))
    if current_user.target_exam:
        query = query.filter((Resource.exam == current_user.target_exam) | (Resource.exam == None))
    
    items = query.all()
    subjects = db.session.query(Resource.subject).distinct().all()
    subjects = [s[0] for s in subjects]
    
    return render_template('resources.html', items=items, subjects=subjects)

@app.route('/track', methods=['POST'])
@login_required
def track():
    kind = request.form.get('kind')
    ref_id = request.form.get('ref_id')
    
    progress = Progress(
        user_id=current_user.id,
        item_type=kind,
        ref_id=ref_id
    )
    db.session.add(progress)
    db.session.commit()
    
    # Update weekly stats
    update_weekly_stats(current_user.id)
    
    # Return JSON for AJAX requests (check if it's an AJAX request)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
        return jsonify({'status': 'success', 'message': 'Progress tracked!'})
    
    flash('Progress tracked!', 'success')
    return redirect(request.referrer or url_for('resources'))

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    subject = request.args.get('subject', '')
    
    if request.method == 'POST':
        qid = request.form.get('qid')
        chosen = request.form.get('chosen')
        question = Question.query.get(qid)
        
        if question and chosen == question.answer:
            # Correct answer
            score = 1
            flash('Correct!', 'success')
        else:
            score = 0
            flash(f'Wrong! Correct answer: {question.answer}', 'error')
        
        # Track progress
        progress = Progress(
            user_id=current_user.id,
            item_type='quiz',
            ref_id=qid,
            extra_score=score
        )
        db.session.add(progress)
        db.session.commit()
        
        # Update weekly stats
        update_weekly_stats(current_user.id)
        
        return redirect(url_for('quiz', subject=subject))
    
    # Determine target difficulty based on recent performance
    recent_quizzes = Progress.query.filter_by(
        user_id=current_user.id,
        item_type='quiz'
    ).order_by(Progress.timestamp.desc()).limit(5).all()
    
    if recent_quizzes:
        avg_score = sum(q.extra_score or 0 for q in recent_quizzes) / len(recent_quizzes)
        if avg_score >= 0.8:
            target_diff = 'hard'
        elif avg_score >= 0.5:
            target_diff = 'medium'
        else:
            target_diff = 'easy'
    else:
        target_diff = 'easy'
    
    # Get question
    query = Question.query.filter_by(difficulty=target_diff)
    if subject:
        query = query.filter_by(subject=subject)
    
    questions = query.all()
    question = random.choice(questions) if questions else None
    
    subjects = db.session.query(Question.subject).distinct().all()
    subjects = [s[0] for s in subjects]
    
    return render_template('quiz.html', question=question, subjects=subjects, target_diff=target_diff)

@app.route('/study_plan', methods=['GET', 'POST'])
@login_required
def study_plan():
    if request.method == 'POST':
        duration_weeks = int(request.form.get('duration_weeks', 4))
        selected_subjects = request.form.getlist('subjects')
        
        if not selected_subjects:
            flash('Please select at least one subject', 'error')
            return redirect(url_for('study_plan'))
        
        # Deactivate old plans
        StudyPlan.query.filter_by(user_id=current_user.id).update({'is_active': False})
        
        # Generate weekly plan
        start_date = date.today()
        plan_items = []
        
        for week in range(duration_weeks):
            for day in range(7):
                current_date = start_date + timedelta(weeks=week, days=day)
                subject = random.choice(selected_subjects)
                plan_items.append(StudyPlan(
                    user_id=current_user.id,
                    date=current_date,
                    subject=subject,
                    is_active=True
                ))
        
        db.session.add_all(plan_items)
        db.session.commit()
        
        flash('Study plan generated!', 'success')
        return redirect(url_for('study_plan'))
    
    # Get active plan
    plan = StudyPlan.query.filter_by(
        user_id=current_user.id,
        is_active=True
    ).order_by(StudyPlan.date).all()
    
    all_subjects = ['Math', 'Physics', 'Chemistry', 'Biology', 'English']
    
    return render_template('study_plan.html', plan=plan, all_subjects=all_subjects)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        
        if form_type == 'resource':
            url = request.form.get('url', '').strip()
            resource_type = request.form.get('resource_type', 'other')
            
            # Check if PDF file was uploaded
            pdf_file = request.files.get('pdf_file')
            if pdf_file and pdf_file.filename:
                # Handle file upload
                uploaded_url = save_uploaded_pdf(pdf_file)
                if uploaded_url:
                    url = uploaded_url
                    resource_type = 'pdf'
                    flash('PDF file uploaded successfully!', 'success')
                else:
                    flash('Invalid file. Only PDF files are allowed.', 'error')
                    return redirect(url_for('admin'))
            
            # Handle pdf_url type (convert to pdf)
            if resource_type == 'pdf_url':
                resource_type = 'pdf'
            
            # If no file uploaded and no URL provided
            if not url:
                flash('Please provide either a URL or upload a PDF file.', 'error')
                return redirect(url_for('admin'))
            
            # Auto-detect resource type if not specified and URL provided
            if resource_type == 'auto' and url:
                resource_type = detect_resource_type(url)
            
            # Validate YouTube URL format
            if resource_type == 'youtube':
                # Convert youtu.be to youtube.com format
                if 'youtu.be' in url:
                    video_id = url.split('/')[-1].split('?')[0]
                    url = f'https://www.youtube.com/watch?v={video_id}'
                elif 'youtube.com' not in url:
                    flash('Invalid YouTube URL format', 'error')
                    return redirect(url_for('admin'))
            
            resource = Resource(
                title=request.form.get('title'),
                subject=request.form.get('subject'),
                grade=request.form.get('grade') or None,
                exam=request.form.get('exam') or None,
                difficulty=request.form.get('difficulty', 'easy'),
                url=url,
                resource_type=resource_type
            )
            db.session.add(resource)
            db.session.commit()
            flash(f'Resource added successfully! ({resource_type.upper()})', 'success')
        
        elif form_type == 'question':
            question = Question(
                subject=request.form.get('subject'),
                exam=request.form.get('exam'),
                difficulty=request.form.get('difficulty', 'easy'),
                prompt=request.form.get('prompt'),
                options=request.form.get('options'),
                answer=request.form.get('answer')
            )
            db.session.add(question)
            db.session.commit()
            flash('Question added!', 'success')
        
        return redirect(url_for('admin'))
    
    resources = Resource.query.order_by(Resource.created_at.desc()).limit(10).all()
    questions = Question.query.order_by(Question.created_at.desc()).limit(10).all()
    
    return render_template('admin.html', resources=resources, questions=questions)

@app.route('/db_browser')
@login_required
def db_browser():
    """Web-based database browser"""
    if not current_user.is_admin:
        flash('Access denied. Admin only.', 'error')
        return redirect(url_for('dashboard'))
    
    # Get statistics
    stats = {
        'users': User.query.count(),
        'resources': Resource.query.count(),
        'questions': Question.query.count(),
        'progress': Progress.query.count(),
        'weekly_stats': WeeklyStats.query.count(),
        'study_plans': StudyPlan.query.count()
    }
    
    # Get data
    users = User.query.order_by(User.created_at.desc()).limit(50).all()
    resources = Resource.query.order_by(Resource.created_at.desc()).limit(50).all()
    questions = Question.query.order_by(Question.created_at.desc()).limit(50).all()
    weekly_stats = WeeklyStats.query.order_by(WeeklyStats.week_start.desc()).limit(20).all()
    recent_progress = Progress.query.order_by(Progress.timestamp.desc()).limit(30).all()
    
    return render_template('db_browser.html',
                         stats=stats,
                         users=users,
                         resources=resources,
                         questions=questions,
                         weekly_stats=weekly_stats,
                         recent_progress=recent_progress)

@app.route('/weekly_monitoring', methods=['GET'])
@login_required
def weekly_monitoring():
    # Update current week stats
    current_week_stat = update_weekly_stats(current_user.id)
    
    # Get last 4 weeks of stats
    today = date.today()
    weeks_data = []
    
    for i in range(4):
        week_start = get_week_start(today) - timedelta(weeks=i)
        week_stat = WeeklyStats.query.filter_by(
            user_id=current_user.id,
            week_start=week_start
        ).first()
        
        if week_stat:
            weeks_data.append({
                'week': f"Week {4-i}",
                'week_start': week_stat.week_start.strftime('%Y-%m-%d'),
                'resources': week_stat.resources_completed,
                'quizzes': week_stat.quizzes_attempted,
                'accuracy': round(week_stat.get_accuracy(), 1),
                'study_hours': round(week_stat.study_hours, 1)
            })
        else:
            weeks_data.append({
                'week': f"Week {4-i}",
                'week_start': week_start.strftime('%Y-%m-%d'),
                'resources': 0,
                'quizzes': 0,
                'accuracy': 0,
                'study_hours': 0
            })
    
    # Calculate trends
    if len(weeks_data) >= 2:
        current = weeks_data[0]
        previous = weeks_data[1]
        
        trends = {
            'resources': current['resources'] - previous['resources'],
            'quizzes': current['quizzes'] - previous['quizzes'],
            'accuracy': current['accuracy'] - previous['accuracy'],
            'study_hours': current['study_hours'] - previous['study_hours']
        }
    else:
        trends = {'resources': 0, 'quizzes': 0, 'accuracy': 0, 'study_hours': 0}
    
    return render_template('weekly_monitoring.html', 
                         current_week=current_week_stat,
                         weeks_data=weeks_data,
                         trends=trends)

if __name__ == '__main__':
    with app.app_context():
        # Create all tables (including WeeklyStats)
        db.create_all()
        print("✓ Database tables created/verified")
        
        # Add resource_type column if it doesn't exist (migration)
        try:
            from sqlalchemy import inspect, text
            inspector = inspect(db.engine)
            
            # Check if resource table exists and add resource_type column if needed
            try:
                columns = [col['name'] for col in inspector.get_columns('resource')]
                if 'resource_type' not in columns:
                    with db.engine.begin() as conn:
                        conn.execute(text('ALTER TABLE resource ADD COLUMN resource_type VARCHAR(20) DEFAULT "other"'))
                    print("✓ Added resource_type column to resource table")
            except Exception:
                pass  # Table might not exist yet
            
            # Verify WeeklyStats table exists
            try:
                inspector.get_columns('weekly_stats')
                print("✓ WeeklyStats table verified")
            except Exception:
                # Table doesn't exist, create it
                db.create_all()
                print("✓ WeeklyStats table created")
                
        except Exception as e:
            print(f"Database migration note: {e}")
            # Ensure all tables are created
            db.create_all()
    
    print("Starting EduTrack server...")
    print("Database: edutrack.db")
    print("Server: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

