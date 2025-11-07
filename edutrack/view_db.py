"""
Quick Database Viewer for EduTrack
Shows database contents without interactive input
"""

from app import app, db
from models import User, Resource, Question, StudyPlan, Progress, WeeklyStats

def show_database_contents():
    """Display database contents"""
    with app.app_context():
        print("=" * 70)
        print("EduTrack Database Contents")
        print("=" * 70)
        
        # Users
        users = User.query.all()
        print(f"\n[USERS] Total: {len(users)}")
        print("-" * 70)
        for u in users:
            admin = " [ADMIN]" if u.is_admin else ""
            print(f"  {u.id}. {u.name} ({u.email}){admin}")
        
        # Resources
        resources = Resource.query.all()
        print(f"\n[RESOURCES] Total: {len(resources)}")
        print("-" * 70)
        for r in resources[:10]:  # Show first 10
            print(f"  {r.id}. {r.title} [{r.resource_type.upper()}] - {r.subject}")
        if len(resources) > 10:
            print(f"  ... and {len(resources) - 10} more")
        
        # Questions
        questions = Question.query.all()
        print(f"\n[QUESTIONS] Total: {len(questions)}")
        print("-" * 70)
        for q in questions[:10]:  # Show first 10
            print(f"  {q.id}. {q.subject} ({q.exam}) - {q.difficulty}")
            print(f"      Q: {q.prompt[:50]}...")
        if len(questions) > 10:
            print(f"  ... and {len(questions) - 10} more")
        
        # Progress
        progress_count = Progress.query.count()
        print(f"\n[PROGRESS RECORDS] Total: {progress_count}")
        
        # Weekly Stats
        weekly_stats = WeeklyStats.query.all()
        print(f"\n[WEEKLY STATS] Total: {len(weekly_stats)}")
        print("-" * 70)
        for ws in weekly_stats:
            accuracy = ws.get_accuracy()
            print(f"  Week {ws.week_start}: Resources={ws.resources_completed}, "
                  f"Quizzes={ws.quizzes_attempted}, Accuracy={accuracy:.1f}%, "
                  f"Hours={ws.study_hours:.1f}")
        
        # Study Plans
        plans_count = StudyPlan.query.count()
        print(f"\n[STUDY PLANS] Total: {plans_count}")
        
        print("\n" + "=" * 70)
        print("Database Location: C:\\Users\\arjun\\Downloads\\edutrack\\edutrack.db")
        print("=" * 70)

if __name__ == '__main__':
    show_database_contents()

