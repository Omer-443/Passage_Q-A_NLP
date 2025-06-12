import sqlite3
import hashlib
import os
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

DB_PATH = "users.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    else:
        salt = bytes.fromhex(salt)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + pwd_hash.hex()

def verify_password(stored_password_hash, provided_password):
    salt = stored_password_hash[:32]  # first 16 bytes hex
    stored_hash = stored_password_hash[32:]
    pwd_hash = hash_password(provided_password, salt)
    return pwd_hash[32:] == stored_hash

def add_user(username, email, password):
    password_hash = hash_password(password)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, password_hash))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return verify_password(row["password_hash"], password)
    return False

def delete_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    changes = cursor.rowcount
    conn.commit()
    conn.close()
    return changes > 0

# OTP storage in-memory: {email: (otp, expiry_timestamp)}
otp_store = {}

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def send_email(to_email, subject, body):
    # Configure your SMTP server credentials here
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USERNAME = "omerfaisal701@gmail.com"
    SMTP_PASSWORD = "hbph loho gepd qudq"
    FROM_EMAIL = SMTP_USERNAME

    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def request_otp(email):
    otp = generate_otp()
    expiry = time.time() + 300  # OTP valid for 5 minutes
    otp_store[email] = (otp, expiry)
    subject = "Your OTP Code"
    body = f"Your OTP code is: {otp}. It is valid for 5 minutes."
    return send_email(email, subject, body)

def verify_otp(email, otp):
    if email in otp_store:
        stored_otp, expiry = otp_store[email]
        if time.time() > expiry:
            del otp_store[email]
            return False, "OTP expired"
        if otp == stored_otp:
            del otp_store[email]
            return True, "OTP verified"
    return False, "Invalid OTP"

def reset_password(email, new_password):
    password_hash = hash_password(new_password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password_hash = ? WHERE email = ?", (password_hash, email))
    conn.commit()
    changes = cursor.rowcount
    conn.close()
    return changes > 0

# Initialize the database table on import
create_users_table()
