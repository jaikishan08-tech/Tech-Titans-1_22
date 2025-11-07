"""
Interactive SQLite Database Browser for EduTrack
Run this script to browse and query the edutrack.db database
"""

from app import app, db
from models import User, Resource, Question, StudyPlan, Progress, WeeklyStats
from sqlalchemy import text

def show_menu():
    """Display menu options"""
    print("\n" + "=" * 60)
    print("EduTrack Database Browser")
    print("=" * 60)
    print("1. View all users")
    print("2. View all resources")
    print("3. View all questions")
    print("4. View progress records")
    print("5. View weekly stats")
    print("6. View study plans")
    print("7. Run custom SQL query")
    print("8. Database statistics")
    print("0. Exit")
    print("=" * 60)

def view_users():
    """Display all users"""
    users = User.query.all()
    print(f"\nTotal Users: {len(users)}")
    print("-" * 60)
    for u in users:
        admin_status = " [ADMIN]" if u.is_admin else ""
        print(f"ID: {u.id} | Name: {u.name} | Email: {u.email}{admin_status}")
        print(f"  Grade: {u.grade or 'N/A'} | Exam: {u.target_exam or 'N/A'}")
        print(f"  Created: {u.created_at}")

def view_resources():
    """Display all resources"""
    resources = Resource.query.all()
    print(f"\nTotal Resources: {len(resources)}")
    print("-" * 60)
    for r in resources:
        print(f"ID: {r.id} | {r.title}")
        print(f"  Subject: {r.subject} | Type: {r.resource_type.upper()}")
        print(f"  Grade: {r.grade or 'N/A'} | Exam: {r.exam or 'N/A'} | Difficulty: {r.difficulty}")
        print(f"  URL: {r.url[:60]}...")

def view_questions():
    """Display all questions"""
    questions = Question.query.all()
    print(f"\nTotal Questions: {len(questions)}")
    print("-" * 60)
    for q in questions:
        print(f"ID: {q.id} | Subject: {q.subject} | Exam: {q.exam} | Difficulty: {q.difficulty}")
        print(f"  Question: {q.prompt[:60]}...")
        print(f"  Answer: {q.answer}")
        print(f"  Options: {q.options}")

def view_progress():
    """Display progress records"""
    progress = Progress.query.order_by(Progress.timestamp.desc()).limit(20).all()
    print(f"\nRecent Progress Records (showing 20):")
    print("-" * 60)
    for p in progress:
        item_type = p.item_type.upper()
        score = f" | Score: {p.extra_score}" if p.extra_score is not None else ""
        print(f"ID: {p.id} | User: {p.user_id} | Type: {item_type} | Ref ID: {p.ref_id}{score}")
        print(f"  Timestamp: {p.timestamp}")

def view_weekly_stats():
    """Display weekly stats"""
    stats = WeeklyStats.query.order_by(WeeklyStats.week_start.desc()).all()
    print(f"\nWeekly Statistics:")
    print("-" * 60)
    for s in stats:
        accuracy = s.get_accuracy()
        print(f"Week Starting: {s.week_start}")
        print(f"  User ID: {s.user_id}")
        print(f"  Resources: {s.resources_completed} | Quizzes: {s.quizzes_attempted}")
        print(f"  Correct Answers: {s.quizzes_correct} | Accuracy: {accuracy:.1f}%")
        print(f"  Study Hours: {s.study_hours:.1f}")

def view_study_plans():
    """Display study plans"""
    plans = StudyPlan.query.order_by(StudyPlan.date.desc()).limit(20).all()
    print(f"\nRecent Study Plans (showing 20):")
    print("-" * 60)
    for p in plans:
        active = " [ACTIVE]" if p.is_active else " [INACTIVE]"
        print(f"ID: {p.id} | User: {p.user_id} | Date: {p.date} | Subject: {p.subject}{active}")

def run_custom_query():
    """Run a custom SQL query"""
    print("\nEnter your SQL query (or 'back' to return):")
    query = input("SQL> ")
    if query.lower() == 'back':
        return
    
    try:
        with db.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = result.fetchall()
            
            if rows:
                print(f"\nResults ({len(rows)} rows):")
                print("-" * 60)
                for row in rows:
                    print(row)
            else:
                print("\nQuery executed successfully (no rows returned)")
    except Exception as e:
        print(f"\nError: {e}")

def database_stats():
    """Show database statistics"""
    print("\nDatabase Statistics:")
    print("-" * 60)
    print(f"Users: {User.query.count()}")
    print(f"Resources: {Resource.query.count()}")
    print(f"Questions: {Question.query.count()}")
    print(f"Study Plans: {StudyPlan.query.count()}")
    print(f"Progress Records: {Progress.query.count()}")
    print(f"Weekly Stats: {WeeklyStats.query.count()}")
    
    # Resource types breakdown
    resources = Resource.query.all()
    types = {}
    for r in resources:
        types[r.resource_type] = types.get(r.resource_type, 0) + 1
    print("\nResource Types:")
    for rtype, count in types.items():
        print(f"  {rtype.upper()}: {count}")

def main():
    """Main loop"""
    with app.app_context():
        while True:
            show_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '0':
                print("\nGoodbye!")
                break
            elif choice == '1':
                view_users()
            elif choice == '2':
                view_resources()
            elif choice == '3':
                view_questions()
            elif choice == '4':
                view_progress()
            elif choice == '5':
                view_weekly_stats()
            elif choice == '6':
                view_study_plans()
            elif choice == '7':
                run_custom_query()
            elif choice == '8':
                database_stats()
            else:
                print("\nInvalid choice. Please try again.")
            
            input("\nPress Enter to continue...")

if __name__ == '__main__':
    main()

