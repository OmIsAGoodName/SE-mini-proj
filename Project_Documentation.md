# Automated Timetable Scheduling System - Documentation

## 1. Project Overview
This project is an automated, web-based Timetable Scheduling System built for educational institutions. It takes raw constraints (Faculty availability and Classroom requirements) and algorithmically generates a conflict-free weekly timetable. 

The application is split into two main areas:
- **Public Homepage:** A clean, read-only view where students and professors can view the official, published timetables.
- **Secure Admin Dashboard:** A password-protected portal where administrators can manage data, preview schedules, generate new timetables, and publish them to the homepage.

---

## 2. Technology Stack & Architecture
- **Backend:** Python with the **Flask** web framework.
- **Frontend:** Vanilla HTML5, CSS3 (using CSS Grid & Flexbox), and Jinja2 templating.
- **Data Processing:** The **Pandas** library is heavily used for reading/writing data and manipulating dataframes during scheduling.
- **Storage:** 
  - `faculty.xlsx` & `classroom.xlsx`: Act as the primary database for requirements.
  - `published.json`: Stores the final serialized HTML tables so the public homepage can load instantly without recalculating.

---

## 3. Core Files & Modules

### `app.py`
The main Flask server. It handles all the web routing:
- `@app.route('/')`: The public homepage.
- `@app.route('/admin/...')`: The secure dashboard routes (requires the password `admin123`).
- Handles the conversion of Pandas Dataframes to HTML tables for the web UI.

### `scheduler.py`
The "Brain" of the project. It contains the `Scheduler` class which houses the algorithm.
- Reads the Excel sheets and drops any empty "ghost" rows to prevent crashes.
- Iterates through 5 days a week (Monday-Friday) and 6 periods a day.
- Dynamically assigns Faculty to Classrooms while strictly obeying constraints.

### `data_manager.py`
A simple helper module that safely appends new rows to `faculty.xlsx` and `classroom.xlsx` when the Admin submits forms from the web dashboard.

---

## 4. How the Scheduling Algorithm Works
The scheduling logic is a **Constraint-Based Greedy Algorithm** with dynamic workload balancing. Here is exactly what it does step-by-step:

1. **Calculate Daily Limits (Workload Balancing):** 
   Instead of greedily packing all classes into Monday and Tuesday (which would leave Friday totally empty), the algorithm calculates a `daily_limit` using `math.ceil(remaining_hours / remaining_days)`. This guarantees that classes are spread evenly across the 5 days, pushing any "Free" periods organically to the end of the day.
2. **Shuffle Classrooms:**
   To prevent one classroom from always getting the best slots, the list of classrooms is randomly shuffled before every single period.
3. **Sort Available Subjects:**
   Subjects that require the most teaching hours are given highest priority.
4. **Faculty Matching (`get_available_faculty`):**
   The algorithm checks if a teacher's `Main Subject` or `Side Subject` matches the requirement. It then strictly checks if they have exceeded their `Max Working Hours/Day`. If a teacher is already busy in that exact time slot teaching another class, it skips them.
5. **Handling Bottlenecks:**
   If a classroom needs a subject, but all qualified teachers are currently busy teaching other classes, the algorithm handles this organically by leaving that specific slot as `"Free"`. Thanks to the daily limit math, it simply catches up and schedules that missed class on a later day.

---

## 5. How to Run the Project

1. **Prerequisites:** Ensure Python is installed.
2. **Install Dependencies:**
   Open the terminal in the project folder and run:
   ```bash
   pip install -r requirements.txt
   ```
3. **Start the Server:**
   ```bash
   python app.py
   ```
4. **Access the App:**
   Open a web browser and go to `http://127.0.0.1:5000`

---

## 6. Usage Guide for the Admin

1. Click **Admin Login** on the homepage and enter `admin123`.
2. **Add Info:** Use the forms to add new faculty constraints or classroom requirements. This safely writes to the Excel files behind the scenes.
3. **Data Preview:** Use this tab to verify that the system is reading the Excel files correctly without any formatting issues.
4. **Timetable Generation:** 
   - Click "Generate New Timetable" to trigger the algorithm.
   - Scroll down to review the results.
   - If everything looks mathematically sound, click **"Publish to Homepage"** to push the JSON data live for the students to see!
