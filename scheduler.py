import pandas as pd
import random

class Scheduler:
    def __init__(self, faculty_file, classroom_file):
        self.faculty_df = pd.read_excel(faculty_file)
        self.classroom_df = pd.read_excel(classroom_file)
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.slots_per_day = 6
        
        # Build faculty lookup
        self.faculty_db = []
        for _, row in self.faculty_df.iterrows():
            self.faculty_db.append({
                "name": row["Name"],
                "main_subject": row["Main Subject"],
                "side_subject": row["Side Subject"] if pd.notna(row["Side Subject"]) else "",
                "max_daily_hours": row["Max Working Hours/Day"],
                "hours_today": 0
            })
            
        # Build requirements
        self.requirements = {}
        self.classrooms = self.classroom_df["Classroom ID"].unique()
        for c in self.classrooms:
            self.requirements[c] = {}
            
        for _, row in self.classroom_df.iterrows():
            c_id = row["Classroom ID"]
            subj = row["Subject"]
            hours = row["Required Hours/Week"]
            self.requirements[c_id][subj] = hours

    def reset_daily_hours(self):
        for f in self.faculty_db:
            f["hours_today"] = 0

    def get_available_faculty(self, subject, busy_faculty):
        """Returns a faculty member who can teach the subject and hasn't exceeded daily hours."""
        available = []
        for f in self.faculty_db:
            if f["name"] not in busy_faculty:
                if subject in [f["main_subject"], f["side_subject"]]:
                    if f["hours_today"] < f["max_daily_hours"]:
                        available.append(f)
        if available:
            # Prefer faculty who haven't taught as many hours today to balance the load
            available.sort(key=lambda x: x["hours_today"])
            return available[0]
        return None

    def generate_timetable(self):
        timetable = []
        
        for day in self.days:
            self.reset_daily_hours()
            
            # To avoid scheduling the same subject multiple times a day if possible
            scheduled_today = {c: set() for c in self.classrooms}
            
            for slot in range(1, self.slots_per_day + 1):
                busy_faculty_this_slot = set()
                
                # Shuffle classrooms to avoid giving priority always to the same classroom
                cls_list = list(self.classrooms)
                random.shuffle(cls_list)
                
                for c_id in cls_list:
                    available_subjects = [s for s, h in self.requirements[c_id].items() if h > 0]
                    
                    if not available_subjects:
                        timetable.append({
                            "Classroom": c_id, "Day": day, "Slot": f"Period {slot}",
                            "Subject": "Free", "Faculty": "-"
                        })
                        continue
                    
                    # Sort: first by whether it's scheduled today (False first), then by remaining hours descending
                    available_subjects.sort(key=lambda s: (s in scheduled_today[c_id], -self.requirements[c_id][s]))
                    
                    assigned = False
                    for subject in available_subjects:
                        faculty = self.get_available_faculty(subject, busy_faculty_this_slot)
                        if faculty:
                            # Assign
                            timetable.append({
                                "Classroom": c_id, "Day": day, "Slot": f"Period {slot}",
                                "Subject": subject, "Faculty": faculty["name"]
                            })
                            faculty["hours_today"] += 1
                            self.requirements[c_id][subject] -= 1
                            scheduled_today[c_id].add(subject)
                            busy_faculty_this_slot.add(faculty["name"])
                            assigned = True
                            break
                    
                    if not assigned:
                        # Could not assign anything (constraints too tight or bug)
                        timetable.append({
                            "Classroom": c_id, "Day": day, "Slot": f"Period {slot}",
                            "Subject": "Conflict/Free", "Faculty": "-"
                        })
                        
        return pd.DataFrame(timetable)
