from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
from data_manager import append_faculty, append_classroom
from scheduler import Scheduler
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_flash_messages'

@app.route('/')
def index():
    return render_template('index.html', tables=None)

@app.route('/add_faculty', methods=['POST'])
def add_faculty():
    name = request.form.get('name')
    department = request.form.get('department')
    main_subject = request.form.get('main_subject')
    side_subject = request.form.get('side_subject')
    max_hours = request.form.get('max_hours')
    
    append_faculty(name, department, main_subject, side_subject, max_hours)
    flash(f"Successfully added faculty: {name}", "success")
    return redirect(url_for('index'))

@app.route('/add_classroom', methods=['POST'])
def add_classroom():
    classroom_id = request.form.get('classroom_id')
    subject = request.form.get('subject')
    hours = request.form.get('required_hours')
    
    append_classroom(classroom_id, subject, hours)
    flash(f"Successfully added requirement for {classroom_id}", "success")
    return redirect(url_for('index'))

@app.route('/generate', methods=['GET'])
def generate():
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
            
            # Convert to HTML table
            html_table = weekly_view.to_html(escape=False, classes="timetable-table")
            tables.append({"classroom": c, "html": html_table})
            
        return render_template('index.html', tables=tables)
    except Exception as e:
        flash(f"Error generating timetable: {str(e)}", "error")
        return redirect(url_for('index'))

if __name__ == '__main__':
    # Running on all interfaces at port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
