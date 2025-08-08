from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

def get_db():
    return mysql.connector.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DB,
        autocommit=True
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE username=%s", (u,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user and user.get('password_hash') == p:  # temporary: replace with hashed password check
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    # demo stats and recent (you should query actual counts)
    stats = {'total_students': 0, 'open_jobs': 0, 'total_applications': 0}
    recent = []
    return render_template('dashboard.html', username=session['username'], stats=stats, recent=recent)

# view students
@app.route('/db/')
def view_db():
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM Student")
    students = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('view_db.html', students=students)

@app.route('/add_student', methods=['GET','POST'])
def add_student():
    if request.method == 'POST':
        data = {
            'regNo': request.form['regNo'],
            'firstName': request.form['firstName'],
            'lastName': request.form.get('lastName'),
            'email': request.form.get('email'),
            'dob': request.form.get('dob'),
            'phoneNo': request.form.get('phoneNo'),
            'gender': request.form.get('gender')
        }
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Student (regNo, firstName, lastName, dob, email, phoneNo, gender)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (data['regNo'], data['firstName'], data['lastName'], data['dob'], data['email'], data['phoneNo'], data['gender']))
        conn.commit()
        cur.close()
        conn.close()
        flash("Student added")
        return redirect(url_for('view_db'))
    return render_template('add_student.html')

# Add job route
@app.route('/add_job', methods=['GET','POST'])
def add_job():
    if request.method == 'POST':
        job_Id = request.form['job_Id']
        company = request.form['company']
        position = request.form['position']
        eligibility = request.form.get('eligibility')
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO Job (job_Id, company, position, eligibility) VALUES (%s,%s,%s,%s)",
                    (job_Id, company, position, eligibility))
        conn.commit()
        cur.close()
        conn.close()
        flash("Job added")
        return redirect(url_for('home'))
    return render_template('add_job.html')

@app.route('/viewstat')
def viewstat():
    # If you have a preexisting stats.html file you want to keep, render it.
    try:
        return render_template('stats.html')
    except:
        return "Stats page not found. If you have a stats.html, place it in templates/"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
