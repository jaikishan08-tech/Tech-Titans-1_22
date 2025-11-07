# Database Location Information

## Primary Database Location

**Main Database File:**
```
C:\Users\arjun\Downloads\edutrack\edutrack.db
```

**Size:** 28,672 bytes (28 KB)
**Last Modified:** November 6, 2025, 20:10:20

## Database Configuration

In `app.py`, the database is configured as:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///edutrack.db'
```

This means the database file `edutrack.db` is located in the **project root directory**.

## Full Path

**Absolute Path:**
```
C:\Users\arjun\Downloads\edutrack\edutrack.db
```

## Additional Database File

There is also a database file in the `instance` folder:
```
C:\Users\arjun\Downloads\edutrack\instance\edutrack.db
```

**Note:** The application is currently using the database in the root directory (`.\edutrack.db`), not the one in the instance folder.

## How to Access the Database

You can:
1. **View/Edit with SQLite Browser:** Download DB Browser for SQLite
2. **Command Line:** Use `sqlite3 edutrack.db` in the project directory
3. **Python Script:** Use the `verify_db.py` script to check database status

## Database Contents

The database contains:
- User accounts
- Resources (with PDF/YouTube types)
- Questions (including AI-generated ones)
- Study plans
- Progress tracking
- Weekly statistics

