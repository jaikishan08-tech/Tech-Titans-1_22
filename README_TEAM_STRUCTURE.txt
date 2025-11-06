===============================================
PROJECT: Personalized Learning & Exam Planner App
TEAM: 5 Members (24-hour Hackathon)
===============================================

🧭 OVERVIEW
-----------
Our application helps students (Grades 1–10) access grade-wise educational content:
🎓 Curated YouTube video lessons
📘 Study notes (PDFs)
📄 Past 3 years’ question papers with solutions
📊 Subject-wise exam weightage
🧠 AI-based personalized study plans and quizzes
🏆 Gamified progress and achievement tracking

It also includes an Admin Panel for educators to upload materials,
add weightages, and manage YouTube video resources.

-----------------------------------------------
📁 GITHUB BRANCH STRUCTURE
-----------------------------------------------

main                → Final tested, production-ready code (only merged after review)
frontend-ui         → All frontend pages (HTML, CSS, JS, React or Jinja Templates)
backend-api         → Flask backend APIs and YouTube Data API integration
database-schema     → SQL schema, sample data, DB connection files
ai-module           → AI logic (study plan, quiz generation, resource ranking)
docs-presentation   → Reports, screenshots, and presentation slides

-----------------------------------------------
👥 TEAM ROLE & RESPONSIBILITIES
-----------------------------------------------

1️⃣ Jai Kishan (Team Leader / Repository Owner / Full Stack)
   - Owns and manages the repository structure
   - Reviews and merges all Pull Requests
   - Designs backend architecture & MySQL schema
   - Integrates YouTube API data into backend routes
   - Oversees overall integration, testing, and presentation

2️⃣ Frontend Dev 1 (UI/UX Specialist)
   - Builds Login & Signup pages
   - Designs dashboard layout (tabs: Lessons, Notes, Past Papers, Progress)
   - Implements progress bar & achievement badges
   - Adds grade-wise themes and responsive design

3️⃣ Frontend Dev 2 (Interactivity & Integration)
   - Connects frontend with backend Flask APIs (resources, YouTube lessons)
   - Creates "Video Lessons" section using embedded YouTube players
   - Implements Study Plan and Quiz UI
   - Adds animations, filtering (by subject/topic), and chart visualizations

4️⃣ Backend Dev (API & Data Integration)
   - Develops all Flask routes:
       /login, /signup, /resources/<grade>, /pastpapers/<grade>,
       /weightage/<grade>, /studyplan, /quiz, /admin
   - Integrates YouTube Data API v3 for fetching video lessons dynamically
   - Handles search, filter, and cache of video results
   - Adds admin upload route for manually curated YouTube links
   - Manages authentication and authorization

5️⃣ AI & DB Dev (Logic + Data Management)
   - Builds and manages MySQL database:
       users, resources, youtube_videos, past_papers, weightage,
       study_plan, quiz, admin
   - Adds fields for grade, subject, video title, URL, channel name, and tags
   - Implements AI logic for:
       - Personalized study plan generation
       - Resource ranking by subject difficulty
       - Short quiz creation based on weak topics
   - Preloads database with sample YouTube lessons and past papers

-----------------------------------------------
🎥 YOUTUBE LESSONS IMPLEMENTATION DETAILS
-----------------------------------------------

✅ API Used: YouTube Data API v3

1️⃣ Fetch curated videos by grade and subject:
   - Example: Search query = "Class 10 Physics Motion Chapter Lecture"
   - API URL: https://www.googleapis.com/youtube/v3/search
   - Parameters:
       - key=YOUR_API_KEY
       - q=Class+10+Physics+Chapter+1
       - type=video
       - maxResults=5
       - part=snippet

2️⃣ Store results in the database:
   Table: youtube_videos
   Columns:
   - id (INT, PK)
   - grade (INT)
   - subject (VARCHAR)
   - video_title (VARCHAR)
   - video_url (TEXT)
   - channel_name (VARCHAR)
   - description (TEXT)
   - tags (TEXT)

3️⃣ Display videos on the dashboard:
   - Frontend fetches data via `/resources/<grade>` route.
   - Videos shown as responsive YouTube embeds or thumbnails with title & channel.

4️⃣ Admin functionality:
   - Admin can manually add or remove YouTube video links.
   - Validation to ensure proper embedding URLs.
   - Future option: auto-fetch videos daily using YouTube API.

-----------------------------------------------
🗃️ DATABASE OVERVIEW
-----------------------------------------------

Database: learning_app

Tables:
- users(id, name, email, grade, password, progress, achievements)
- youtube_videos(id, grade, subject, title, url, channel, tags, difficulty)
- resources(id, grade, subject, type, title, link, difficulty)
- past_papers(id, grade, subject, year, file_link, solution_link)
- weightage(id, grade, subject, percentage)
- study_plan(id, user_id, subject, topic, hours, date)
- quiz(id, grade, subject, question, options, answer)
- admin(id, username, password)

-----------------------------------------------
⚙️ GITHUB WORKFLOW
-----------------------------------------------

1️⃣ Each teammate works only inside their assigned branch.
2️⃣ Commit changes frequently with descriptive messages, e.g.:
     feat: integrated YouTube API for Class 10 Physics
     fix: resolved video embed issue
     style: improved lesson card layout
3️⃣ Before merging to main:
     - Pull latest main branch
     - Test locally (Flask + DB + YouTube API)
     - Create Pull Request → Reviewed by Jai Kishan
4️⃣ Merge only tested, stable code into main.
5️⃣ No direct commits to main branch.

-----------------------------------------------
🧱 DEVELOPMENT STAGES (SUMMARY)
-----------------------------------------------

Phase 1 (0–2 hr): Planning, repo setup, assign roles  
Phase 2 (2–5 hr): Database setup + YouTube API connection  
Phase 3 (5–8 hr): Frontend structure + Video Lessons dashboard  
Phase 4 (8–12 hr): AI logic + Study plan + Quiz  
Phase 5 (12–15 hr): Admin panel + Video curation tools  
Phase 6 (15–18 hr): Progress bar + Achievements + Analytics  
Phase 7 (18–21 hr): Final testing, bug fixes, and styling  
Phase 8 (21–24 hr): Demo recording + Presentation slides

-----------------------------------------------
✅ FINAL DELIVERABLES
-----------------------------------------------

- Grade-wise YouTube lessons (auto-fetched + curated)
- Study materials & past 3 years’ papers with solutions
- AI-generated personalized study plan + short quizzes
- Subject weightage charts
- Student progress & achievement system
- Admin panel for content management
- Fully documented GitHub repository
- Demo video + Presentation slides

===============================================
END OF FILE
===============================================
