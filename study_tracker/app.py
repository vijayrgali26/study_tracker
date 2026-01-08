from flask import Flask, flash, render_template, request, redirect, url_for
from config import get_db_connection
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from flask import Flask

app = Flask(__name__)  # Create the app instance first
app.secret_key = 'your_unique_secret_key_here'  # Then set the secret key


# rest of your code...




scheduler = BackgroundScheduler()
scheduler.start()

def auto_create_daily_entry():
    conn = get_db_connection()
    cur = conn.cursor()
    today = datetime.now().date()
    cur.execute("SELECT * FROM timetable WHERE date=%s", (today,))
    if not cur.fetchone():
        cur.execute("INSERT INTO timetable (date, total_hours, tasks) VALUES (%s, 0, '')", (today,))
        conn.commit()
    cur.close()
    conn.close()

scheduler.add_job(auto_create_daily_entry, 'cron', hour=0, minute=0)


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM goals")
    goals = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', goals=goals)

@app.route('/add_goal', methods=['POST'])
def add_goal():
    goal_name = request.form['goal_name']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    target_hours = float(request.form['target_hours'])

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO goals (goal_name, start_date, end_date, target_hours) VALUES (%s,%s,%s,%s)",
                (goal_name, start_date, end_date, target_hours))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

@app.route('/delete_goal', methods=['POST'])
def delete_goal():
    goal_id = request.form.get('goal_id')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM goals WHERE id=%s", (goal_id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Goal deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/delete_session', methods=['POST'])
def delete_session():
    session_id = request.form.get('session_id')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM timetable WHERE id=%s", (session_id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Session deleted successfully!', 'success')
    return redirect(url_for('timetable'))




@app.route('/timetable', methods=['GET', 'POST'])
def timetable():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        tasks = request.form['tasks']

        fmt = '%H:%M'
        diff = (datetime.strptime(end_time, fmt) - datetime.strptime(start_time, fmt)).total_seconds() / 3600

        cur.execute("INSERT INTO timetable (date, start_time, end_time, total_hours, tasks) VALUES (%s,%s,%s,%s,%s)",
                    (date, start_time, end_time, diff, tasks))
        conn.commit()

        # Update total hours completed in goals (assuming one goal for simplicity)
        cur.execute("UPDATE goals SET hours_completed = hours_completed + %s WHERE id=1", (diff,))
        conn.commit()

    cur.execute("SELECT * FROM timetable ORDER BY date DESC")
    entries = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('timetable.html', entries=entries)

if __name__ == "__main__":
    app.run(debug=True)
