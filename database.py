import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_connection():
    """Create and return a database connection"""
    try:
        conn = psycopg2.connect(
            os.getenv("DATABASE_URL"),
            cursor_factory=RealDictCursor  # Return results as dictionaries
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def save_user_interests(user_id, username, interests):
    """Save user interests and username to database"""
    conn = get_connection()
    if conn is None:
        print("Database connection failed")
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (user_id, username, interests)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id) 
            DO UPDATE SET 
                username = EXCLUDED.username,
                interests = EXCLUDED.interests;
        """, (str(user_id), username, interests))
        conn.commit()
        print(f"Successfully saved interests for user {username}: {interests}")
        return True
    except Exception as e:
        print(f"Failed to save user interests: {e}")
        return False
    finally:
        conn.close()

def find_matching_users(user_id, interests):
    """Find other users with matching interests"""
    conn = get_connection()
    if conn is None:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT username, interests 
            FROM users 
            WHERE user_id != %s::varchar 
            AND interests && %s::text[];
        """, (str(user_id), interests))
        matches = cursor.fetchall()
        print(f"Found matching users: {matches}")
        return matches
    except Exception as e:
        print(f"Failed to match users: {e}")
        return []
    finally:
        conn.close()