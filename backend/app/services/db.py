# import psycopg2
# import os

# def get_db_connection():
#     return psycopg2.connect(
#         os.getenv("DATABASE_URL"),
#         connect_timeout=5,
#         options="-c statement_timeout=3000"
#     )
