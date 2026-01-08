import MySQLdb

def get_db_connection():
    conn = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="admin123",
        db="study_tracker"
    )
    return conn
