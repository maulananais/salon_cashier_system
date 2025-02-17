import mysql.connector

# Koneksi ke database MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="salon"
)
cursor = db.cursor()

def close_db():
    # Tutup koneksi database
    cursor.close()
    db.close()
