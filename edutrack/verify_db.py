"""
Database verification script for EduTrack
Run this to verify all tables are created in edutrack.db
"""

from app import app, db
from models import User, Resource, Question, StudyPlan, Progress, WeeklyStats
from sqlalchemy import inspect

def verify_database():
    """Verify all tables exist in the database"""
    with app.app_context():
        print("=" * 50)
        print("EduTrack Database Verification")
        print("=" * 50)
        
        # Create all tables
        db.create_all()
        print("\n[OK] All tables created/verified")
        
        # Check which tables exist
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print("\nDatabase Tables:")
        expected_tables = ['user', 'resource', 'question', 'study_plan', 'progress', 'weekly_stats']
        
        for table in expected_tables:
            if table in tables:
                print(f"  [OK] {table}")
                
                # Show columns for WeeklyStats
                if table == 'weekly_stats':
                    columns = inspector.get_columns(table)
                    print(f"    Columns: {', '.join([col['name'] for col in columns])}")
            else:
                print(f"  [MISSING] {table}")
        
        # Check resource table for resource_type column
        try:
            columns = [col['name'] for col in inspector.get_columns('resource')]
            if 'resource_type' in columns:
                print("\n[OK] Resource table has resource_type column")
            else:
                print("\n[WARNING] Resource table missing resource_type column")
        except Exception as e:
            print(f"\n[WARNING] Could not check resource table: {e}")
        
        # Count records
        print("\nRecord Counts:")
        try:
            print(f"  Users: {User.query.count()}")
            print(f"  Resources: {Resource.query.count()}")
            print(f"  Questions: {Question.query.count()}")
            print(f"  Study Plans: {StudyPlan.query.count()}")
            print(f"  Progress Records: {Progress.query.count()}")
            print(f"  Weekly Stats: {WeeklyStats.query.count()}")
        except Exception as e:
            print(f"  Error counting records: {e}")
        
        print("\n" + "=" * 50)
        print("[OK] Database verification complete!")
        print("=" * 50)

if __name__ == '__main__':
    verify_database()

