"""
database.py - SQLite Database for Robo Receptionist +
Manages qualified medical specialists, hospital departments, on-call schedules, and triage history.
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "receptionist.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Doctors Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        title TEXT NOT NULL,
        specialty TEXT NOT NULL,
        sub_specialty TEXT NOT NULL,
        department TEXT NOT NULL,
        experience_years INTEGER NOT NULL,
        rating REAL NOT NULL,
        on_call_night BOOLEAN NOT NULL DEFAULT 1,
        phone TEXT NOT NULL,
        email TEXT NOT NULL,
        avatar_url TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Available',
        room_number TEXT NOT NULL
    )
    """)

    # 2. Triage Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS triage_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        injury_type TEXT NOT NULL,
        severity TEXT NOT NULL,
        confidence REAL NOT NULL,
        specialty_needed TEXT NOT NULL,
        first_aid TEXT NOT NULL,
        doctor_assigned_id INTEGER,
        patient_ticket TEXT,
        image_preview TEXT,
        FOREIGN KEY (doctor_assigned_id) REFERENCES doctors (id)
    )
    """)

    # Check if doctors are already seeded
    cursor.execute("SELECT COUNT(*) FROM doctors")
    if cursor.fetchone()[0] == 0:
        seed_doctors(cursor)

    conn.commit()
    conn.close()

def seed_doctors(cursor):
    sample_doctors = [
        (
            "Dr. Vikram Sen", "Chief of Trauma Surgery", "Trauma & Emergency",
            "Acute Trauma, Hemorrhage Control, Internal Injuries",
            "Emergency Department (Red Bay)", 18, 4.9, 1, "+91 98112-40912",
            "v.sen@cityhospital.org", "https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=150",
            "On Duty", "ER-Trauma-01"
        ),
        (
            "Dr. Ananya Sharma", "Senior Orthopedic Surgeon", "Orthopedic Surgery",
            "Bone Fractures, Joint Dislocations, Tendon Tears",
            "Orthopedics & Sports Medicine", 14, 4.8, 1, "+91 98450-23491",
            "a.sharma@cityhospital.org", "https://images.unsplash.com/photo-1594824813580-c11451f28b24?w=150",
            "Available", "OR-Wing-04"
        ),
        (
            "Dr. Marcus Hayes", "Consultant Plastic & Reconstructive Surgeon", "Plastic & Reconstructive Surgery",
            "Complex Lacerations, Facial Trauma, Tissue Flaps",
            "Surgical Specialities Wing", 12, 4.9, 1, "+91 98301-88231",
            "m.hayes@cityhospital.org", "https://images.unsplash.com/photo-1537368910025-700350fe46c7?w=150",
            "Available", "Surg-02"
        ),
        (
            "Dr. Priya Patel", "Dermatologist & Burn Care Specialist", "Dermatology & Burn Care",
            "Thermal Burns, Chemical Scalds, Acute Contact Dermatitis",
            "Burn ICU & Dermatology Unit", 15, 4.9, 1, "+91 98711-55420",
            "p.patel@cityhospital.org", "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=150",
            "On Duty", "Burn-Unit-B"
        ),
        (
            "Dr. David Chen", "Senior Ophthalmologist", "Ophthalmology",
            "Corneal Abrasions, Ocular Chemical Exposure, Orbital Trauma",
            "Ophthalmology Clinic", 11, 4.7, 1, "+91 98992-11490",
            "d.chen@cityhospital.org", "https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=150",
            "Available", "Eye-Clinic-01"
        ),
        (
            "Dr. Sarah Jenkins", "Emergency Medicine & Head Trauma Specialist", "Neurology & Head Trauma",
            "Head Contusions, Concussions, Craniofacial Impact",
            "Neuro-Emergency Wing", 16, 4.8, 1, "+91 98103-66219",
            "s.jenkins@cityhospital.org", "https://images.unsplash.com/photo-1582750433449-648ed127bb54?w=150",
            "Available", "Neuro-ER-03"
        ),
        (
            "Dr. Rajesh Kulkarni", "Attending Emergency Physician", "General Emergency Medicine",
            "Minor Lacerations, Contusions, Soft Tissue Sprains, Tetanus Prophylaxis",
            "Triage & Fast-Track ER", 9, 4.6, 1, "+91 98200-77312",
            "r.kulkarni@cityhospital.org", "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=150",
            "On Duty", "FastTrack-02"
        )
    ]

    cursor.executemany("""
    INSERT INTO doctors (
        name, title, specialty, sub_specialty, department,
        experience_years, rating, on_call_night, phone, email,
        avatar_url, status, room_number
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_doctors)

def find_doctors_for_specialty(specialty_keyword):
    """
    Finds and ranks doctors matching the specialty needed, prioritizing on-call specialists.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Search with keyword matching across specialty and sub_specialty
    keyword = f"%{specialty_keyword}%"
    cursor.execute("""
    SELECT * FROM doctors
    WHERE specialty LIKE ? OR sub_specialty LIKE ?
    ORDER BY on_call_night DESC, rating DESC, experience_years DESC
    """, (keyword, keyword))

    matches = [dict(row) for row in cursor.fetchall()]

    # If no direct match, fallback to General Emergency & Trauma
    if not matches:
        cursor.execute("""
        SELECT * FROM doctors
        ORDER BY on_call_night DESC, rating DESC
        LIMIT 3
        """)
        matches = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return matches

def log_triage(injury_type, severity, confidence, specialty_needed, first_aid, doctor_id=None, image_preview=""):
    conn = get_connection()
    cursor = conn.cursor()
    ticket_num = f"ER-{datetime.now().strftime('%H%M%S')}-{datetime.now().microsecond // 1000}"
    cursor.execute("""
    INSERT INTO triage_logs (
        injury_type, severity, confidence, specialty_needed, first_aid,
        doctor_assigned_id, patient_ticket, image_preview
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (injury_type, severity, confidence, specialty_needed, first_aid, doctor_id, ticket_num, image_preview))
    triage_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return triage_id, ticket_num

def assign_doctor_to_triage(triage_id, doctor_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE triage_logs
    SET doctor_assigned_id = ?
    WHERE id = ?
    """, (doctor_id, triage_id))

    cursor.execute("SELECT patient_ticket FROM triage_logs WHERE id = ?", (triage_id,))
    ticket_row = cursor.fetchone()
    ticket_num = ticket_row["patient_ticket"] if ticket_row else f"ER-{triage_id}"

    cursor.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
    doc_row = cursor.fetchone()
    doctor = dict(doc_row) if doc_row else None
    conn.commit()
    conn.close()
    return {"doctor": doctor, "ticket_num": ticket_num}

def get_all_doctors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctors ORDER BY id ASC")
    doctors = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return doctors

def get_recent_scans(limit=5):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT t.*, d.name as doctor_name, d.specialty as doctor_specialty
    FROM triage_logs t
    LEFT JOIN doctors d ON t.doctor_assigned_id = d.id
    ORDER BY t.timestamp DESC
    LIMIT ?
    """, (limit,))
    logs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return logs

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
