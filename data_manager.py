import pandas as pd
import os

FACULTY_FILE = "faculty.xlsx"
CLASSROOM_FILE = "classroom.xlsx"

def append_faculty(name, department, main_subject, side_subject, max_hours):
    if not os.path.exists(FACULTY_FILE):
        df = pd.DataFrame(columns=["Name", "Department", "Main Subject", "Side Subject", "Max Working Hours/Day"])
    else:
        df = pd.read_excel(FACULTY_FILE)
    
    new_row = {
        "Name": name,
        "Department": department,
        "Main Subject": main_subject,
        "Side Subject": side_subject,
        "Max Working Hours/Day": int(max_hours)
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(FACULTY_FILE, index=False)

def append_classroom(classroom_id, subject, required_hours):
    if not os.path.exists(CLASSROOM_FILE):
        df = pd.DataFrame(columns=["Classroom ID", "Subject", "Required Hours/Week"])
    else:
        df = pd.read_excel(CLASSROOM_FILE)
        
    new_row = {
        "Classroom ID": classroom_id,
        "Subject": subject,
        "Required Hours/Week": int(required_hours)
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(CLASSROOM_FILE, index=False)
