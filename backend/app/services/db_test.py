from app.services.db import get_db_connection

def test_db_connection():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        conn.close()
        print("✅ DB connection successful:", result)
    except Exception as e:
        print("❌ DB connection failed:", e)

if __name__ == "__main__":
    test_db_connection()
