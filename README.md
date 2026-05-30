# Automated Timetable Scheduling System

A Python-based utility designed to automatically generate collision-free timetables for multiple classrooms. This system evaluates faculty working constraints and classroom syllabus requirements to seamlessly distribute academic workload over a 5-day week.

## Features
- **Collision Detection:** Guarantees that a professor is never double-booked across different classrooms during the same period.
- **Constraint Management:** Strictly adheres to maximum daily working hours for all faculty members to prevent overload.
- **Web Interface:** Features a clean, professional Flask-based UI for effortless data management.
- **Secure Admin Dashboard:** A password-protected portal allowing administrators to preview raw data, generate schedules, and publish official timetables.

## Getting Started

Follow these steps to set up and run the project locally on your machine.

### 1. Clone the Repository
Open your command prompt or terminal and download the code:
```bash
git clone https://github.com/OmIsAGoodName/SE-mini-proj.git
cd SE-mini-proj
```

### 2. Install Dependencies
Ensure you have Python installed, then install the required libraries:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
Start the local Flask web server:
```bash
python app.py
```

### 4. Access the Dashboard
Once the server is running, open your web browser and navigate to the local address provided (typically):
[http://127.0.0.1:5000](http://127.0.0.1:5000)

## Usage Instructions
1. **Public View:** The homepage displays the currently active timetables. If none are visible, an admin needs to publish them.
2. **Admin Portal:** Click "Admin Login" in the header (Password: `admin123`) to access the secure dashboard.
3. **Manage Data:** From the Admin panel, you can view existing datasets (loaded from Excel) or use the forms to add new Faculty members and Classroom requirements.
4. **Generate & Publish:** Click "Generate New Timetable" to create a fresh schedule based on the current data. If the preview looks correct, click "Publish to Homepage" to make it visible to everyone!
