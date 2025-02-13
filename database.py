import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def get_connection():
    """创建并返回数据库连接"""
    try:
        conn = psycopg2.connect(
            os.getenv("DATABASE_URL"),
            cursor_factory=RealDictCursor  # 返回字典形式的结果
        )
        return conn
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

def save_user_interests(user_id, interests):
    """保存用户兴趣到数据库"""
    conn = get_connection()
    if conn is None:
        print("数据库连接失败")
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (user_id, interests)
            VALUES (%s, %s)
            ON CONFLICT (user_id) 
            DO UPDATE SET interests = EXCLUDED.interests;
        """, (str(user_id), interests))  # 将 user_id 转换为字符串
        conn.commit()
        print(f"成功保存用户 {user_id} 的兴趣：{interests}")
        return True
    except Exception as e:
        print(f"保存用户兴趣失败: {e}")
        return False
    finally:
        conn.close()

def find_matching_users(user_id, interests):
    """根据兴趣匹配其他用户"""
    conn = get_connection()
    if conn is None:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id, interests 
            FROM users 
            WHERE user_id != %s::varchar  -- 将 user_id 转换为字符串
            AND interests && %s::text[];
        """, (str(user_id), interests))  # 将 user_id 转换为字符串
        matches = cursor.fetchall()
        print(f"找到匹配用户：{matches}")  # 打印匹配结果
        return matches
    except Exception as e:
        print(f"匹配用户失败: {e}")
        return []
    finally:
        conn.close()