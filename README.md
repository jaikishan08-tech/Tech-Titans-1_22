
# EduTrack — Full-Stack Exam Prep Platform (Flask + SQLite)

A compact yet complete implementation of EduTrack with:
- Authentication (register/login)
- Exam/grade profile
- Curated resources (YouTube, notes, PYQs) with filters
- Lightweight AI study planner (exam weightage → weekly schedule)
- Adaptive quiz engine (difficulty adjusts by recent score)
- Progress tracking + simple achievements
- Admin panel for content curation

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# (Optional) create .env from example and tweak secrets
cp .env.example .env

# Initialize DB with sample data
flask --app app.py init-db

# Run
python app.py
# open http://localhost:5000
```

### Demo Accounts
- **Admin**: `admin@edutrack.local` / `admin123`
- **Student**: `student@edutrack.local` / `student123`
