# import psycopg2
# import os
# from dotenv import load_dotenv

# load_dotenv()

# try:
#     conn = psycopg2.connect(os.getenv("DATABASE_URL"), connect_timeout=5)
#     conn.close()
#     print("✅ DB connection successful")
# except Exception as e:
#     print("❌ DB connection failed:", e)
