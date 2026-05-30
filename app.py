from flask import Flask, render_template, request, redirect, url_for, flash, session
import pandas as pd
from data_manager import append_faculty, append_classroom
from scheduler import Scheduler
import os
import json

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_flash_messages'

ADMIN_PASSWORD = 'admin123'
PUBLISHED_FILE = 'published.json'

def load_published():
    if os.path.exists(PUBLISHED_FILE):
        try:
            with open(PUBLISHED_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return None
    return None

def save_published(data):
    with open(PUBLISHED_FILE, 'w') as f:
        json.dump(data, f)

# Helper to check auth
def is_admin():
    return session.get('logged_in') == True

@app.route('/')
def home():
    published_tables = load_published()
    return render_template('home.html', tables=published_tables, is_admin=is_admin())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            flash("Successfully logged in as Admin.", "success")
            return redirect(url_for('admin'))
        else:
            flash("Incorrect password.", "error")
    return render_template('login.html', is_admin=is_admin())

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for('home'))

@app.route('/admin')
def admin():
    if not is_admin():
        flash("You must be logged in to view the admin dashboard.", "error")
        return redirect(url_for('login'))
    return redirect(url_for('admin_generate_view'))

@app.route('/admin/generate_view')
def admin_generate_view():
    if not is_admin(): return redirect(url_for('login'))
    generated_tables = session.get('generated_tables', None)
    return render_template('admin_generate.html', generated_tables=generated_tables, is_admin=is_admin())

@app.route('/admin/preview')
def admin_preview():
    if not is_admin(): return redirect(url_for('login'))
    
    try:
        faculty_df = pd.read_excel('faculty.xlsx').dropna(how='all').dropna(axis=1, how='all').fillna("")
        faculty_html = faculty_df.to_html(classes="data-table", index=False)
    except Exception:
        faculty_html = "<p>No faculty data found.</p>"
        
    try:
        classroom_df = pd.read_excel('classroom.xlsx').dropna(how='all').dropna(axis=1, how='all').fillna("")
        classroom_html = classroom_df.to_html(classes="data-table", index=False)
    except Exception:
        classroom_html = "<p>No classroom data found.</p>"
        
    return render_template('admin_preview.html', faculty_html=faculty_html, classroom_html=classroom_html, is_admin=is_admin())

@app.route('/admin/add')
def admin_add():
    if not is_admin(): return redirect(url_for('login'))
    return render_template('admin_add.html', is_admin=is_admin())

@app.route('/admin/add_faculty', methods=['POST'])
def admin_add_faculty():
    if not is_admin(): return redirect(url_for('login'))
    
    name = request.form.get('name')
    department = request.form.get('department')
    main_subject = request.form.get('main_subject')
    side_subject = request.form.get('side_subject')
    max_hours = request.form.get('max_hours')
    
    try:
        append_faculty(name, department, main_subject, side_subject, max_hours)
        flash(f"Successfully added faculty: {name}", "success")
    except Exception as e:
        flash(f"Error adding faculty: {e}", "error")
        
    return redirect(url_for('admin_add'))

@app.route('/admin/add_classroom', methods=['POST'])
def admin_add_classroom():
    if not is_admin(): return redirect(url_for('login'))
    
    classroom_id = request.form.get('classroom_id')
    subject = request.form.get('subject')
    hours = request.form.get('required_hours')
    
    try:
        append_classroom(classroom_id, subject, hours)
        flash(f"Successfully added requirement for {classroom_id}", "success")
    except Exception as e:
        flash(f"Error adding requirement: {e}", "error")
        
    return redirect(url_for('admin_add'))

@app.route('/admin/generate', methods=['POST'])
def admin_generate():
    if not is_admin(): return redirect(url_for('login'))
    
    try:
        scheduler = Scheduler("faculty.xlsx", "classroom.xlsx")
        timetable_df = scheduler.generate_timetable()
        
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        classrooms = sorted(list(timetable_df["Classroom"].unique()))
        
        tables = []
        for c in classrooms:
            df_c = timetable_df[timetable_df["Classroom"] == c].copy()
            df_c["Cell"] = df_c["Subject"] + "<br><small>(" + df_c["Faculty"] + ")</small>"
            weekly_view = df_c.pivot(index="Slot", columns="Day", values="Cell")
            weekly_view = weekly_view[days_order]
            
            html_table = weekly_view.to_html(escape=False, classes="timetable-table")
            tables.append({"classroom": c, "html": html_table})
            
        session['generated_tables'] = tables
        flash("Timetables successfully generated! Review below and click Publish to show on Homepage.", "success")
    except Exception as e:
        flash(f"Error generating timetable: {str(e)}", "error")
        
    return redirect(url_for('admin_generate_view'))

@app.route('/admin/publish', methods=['POST'])
def admin_publish():
    if not is_admin(): return redirect(url_for('login'))
    
    generated_tables = session.get('generated_tables')
    if generated_tables:
        save_published(generated_tables)
        flash("Timetables successfully published to the Homepage!", "success")
    else:
        flash("No generated timetables found to publish.", "error")
        
    return redirect(url_for('admin_generate_view'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
