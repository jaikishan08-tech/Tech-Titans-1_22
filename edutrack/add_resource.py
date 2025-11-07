"""
Simple script to add resources to EduTrack
Usage: python add_resource.py
"""

from app import app, db
from models import Resource

def add_resource(title, subject, url, grade=None, exam=None, difficulty='easy', resource_type='auto'):
    """
    Add a resource to the database
    
    Parameters:
    - title: Resource title (required)
    - subject: Subject name like Math, Physics, etc. (required)
    - url: Resource URL (required)
    - grade: Grade level (10, 11, 12) - optional
    - exam: Exam type (JEE, NEET, KCET, etc.) - optional
    - difficulty: easy, medium, or hard (default: easy)
    - resource_type: auto, youtube, pdf, or other (default: auto)
    """
    with app.app_context():
        # Auto-detect resource type if set to 'auto'
        if resource_type == 'auto':
            url_lower = url.lower()
            if 'youtube.com' in url_lower or 'youtu.be' in url_lower:
                resource_type = 'youtube'
            elif url_lower.endswith('.pdf') or 'pdf' in url_lower:
                resource_type = 'pdf'
            else:
                resource_type = 'other'
        
        resource = Resource(
            title=title,
            subject=subject,
            url=url,
            grade=grade,
            exam=exam,
            difficulty=difficulty,
            resource_type=resource_type
        )
        
        db.session.add(resource)
        db.session.commit()
        print(f"✓ Successfully added: {title} ({resource_type.upper()})")
        return resource

# Example: Add some sample resources
if __name__ == '__main__':
    print("Adding sample resources...")
    print("-" * 50)
    
    # Example 1: YouTube video
    add_resource(
        title="Khan Academy - Algebra Basics",
        subject="Math",
        url="https://youtube.com/watch?v=NybHckSEQBI",
        grade="10",
        difficulty="easy",
        resource_type="youtube"
    )
    
    # Example 2: PDF document
    add_resource(
        title="Physics Formula Sheet",
        subject="Physics",
        url="https://example.com/physics-formulas.pdf",
        exam="JEE",
        difficulty="medium",
        resource_type="pdf"
    )
    
    # Example 3: Auto-detect (will detect as YouTube)
    add_resource(
        title="Chemistry Tutorial",
        subject="Chemistry",
        url="https://youtu.be/example123",
        grade="11",
        exam="NEET",
        difficulty="hard"
    )
    
    # Example 4: Other link
    add_resource(
        title="Study Guide Website",
        subject="Biology",
        url="https://example.com/study-guide",
        exam="NEET",
        difficulty="medium",
        resource_type="other"
    )
    
    print("-" * 50)
    print("Done! Check the Resources section or Admin panel to see added resources.")

