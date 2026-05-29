import pandas as pd

def generate_mock_data():
    # 1. Faculty Dataset
    faculty_data = {
        "Name": [
            "Dr. Alice", "Prof. Bob", "Dr. Charlie", 
            "Prof. Dave", "Dr. Eve", "Prof. Frank"
        ],
        "Department": [
            "Computer Science", "Computer Science", "Computer Science", 
            "Computer Science", "Computer Science", "Mathematics"
        ],
        "Main Subject": [
            "Data Structures", "Algorithms", "Operating Systems", 
            "Database Systems", "Software Engineering", "Mathematics"
        ],
        "Side Subject": [
            "Algorithms", "Database Systems", "Software Engineering", 
            "Operating Systems", "Data Structures", ""
        ],
        "Max Working Hours/Day": [
            4, 3, 4, 3, 4, 3
        ]
    }
    df_faculty = pd.DataFrame(faculty_data)
    df_faculty.to_excel("faculty.xlsx", index=False)
    print("Created faculty.xlsx")

    # 2. Classroom Syllabus Dataset
    # Total slots per week = 5 days * 6 slots = 30 slots per classroom
    comp1_data = {
        "Classroom ID": ["CS-Year2-Comp1"] * 6,
        "Subject": [
            "Data Structures", "Algorithms", "Operating Systems", 
            "Database Systems", "Software Engineering", "Mathematics"
        ],
        "Required Hours/Week": [
            6, 5, 5, 5, 5, 4
        ]
    }
    
    comp2_data = {
        "Classroom ID": ["CS-Year2-Comp2"] * 6,
        "Subject": [
            "Data Structures", "Algorithms", "Operating Systems", 
            "Database Systems", "Software Engineering", "Mathematics"
        ],
        "Required Hours/Week": [
            6, 5, 5, 5, 5, 4
        ]
    }
    
    df_classroom = pd.concat([pd.DataFrame(comp1_data), pd.DataFrame(comp2_data)], ignore_index=True)
    df_classroom.to_excel("classroom.xlsx", index=False)
    print("Created classroom.xlsx")

if __name__ == "__main__":
    generate_mock_data()
