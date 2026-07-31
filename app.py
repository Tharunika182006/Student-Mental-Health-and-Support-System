from flask import Flask, render_template, request, redirect, url_for, session
from db_config import db, cursor
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Secret Key for Session
app.secret_key = os.getenv("SECRET_KEY")


# ======================
# Home Page
# ======================

@app.route('/')
def home():
    return render_template('index.html')


# ======================
# Register Page
# ======================

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        department = request.form['department']
        year_of_study = request.form['year_of_study']
        dob = request.form['dob']
        gender = request.form['gender']
        emergency_contact_name = request.form['emergency_contact_name']
        emergency_contact_number = request.form['emergency_contact_number']

        sql = """
        INSERT INTO users
        (
            full_name,
            email,
            password,
            department,
            year_of_study,
            dob,
            gender,
            emergency_contact_name,
            emergency_contact_number
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            full_name,
            email,
            password,
            department,
            year_of_study,
            dob,
            gender,
            emergency_contact_name,
            emergency_contact_number
        )

        cursor.execute(sql, values)
        db.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


# ======================
# Login Page
# ======================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        sql = "SELECT * FROM users WHERE email=%s AND password=%s"
        cursor.execute(sql, (email, password))

        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            session['name'] = user[1]

            return redirect(url_for('dashboard'))

        else:
            return "Invalid Email or Password"

    return render_template('login.html')


# ======================
# Dashboard
# ======================

@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Latest Stress Assessment
    cursor.execute("""
        SELECT score, level
        FROM stress_assessment
        WHERE user_id=%s
        ORDER BY id DESC
        LIMIT 1
    """, (session['user_id'],))
    stress = cursor.fetchone()

    # Latest Mood
    cursor.execute("""
        SELECT mood
        FROM mood_logs
        WHERE user_id=%s
        ORDER BY id DESC
        LIMIT 1
    """, (session['user_id'],))
    latest_mood = cursor.fetchone()

    return render_template(
        'dashboard.html',
        name=session['name'],
        stress=stress,
        latest_mood=latest_mood
    )




# ======================
# Mood Tracker
# ======================

@app.route('/mood', methods=['GET', 'POST'])
def mood():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        selected_mood = request.form['mood']

        sql = """
        INSERT INTO mood_logs(user_id, mood)
        VALUES(%s,%s)
        """

        cursor.execute(sql, (session['user_id'], selected_mood))
        db.commit()

        return redirect(url_for('dashboard'))

    return render_template('mood.html')

@app.route('/stress', methods=['GET', 'POST'])
def stress():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        q1 = int(request.form['q1'])
        q2 = int(request.form['q2'])
        q3 = int(request.form['q3'])

        score = q1 + q2 + q3

        if score <= 4:
            level = "Low"
        elif score <= 8:
            level = "Moderate"
        else:
            level = "High"

        sql = """
        INSERT INTO stress_assessment(user_id, score, level)
        VALUES(%s,%s,%s)
        """

        cursor.execute(
            sql,
            (session['user_id'], score, level)
        )

        db.commit()

        return f"""
        <h2>Assessment Complete</h2>
        <h3>Stress Score: {score}</h3>
        <h3>Stress Level: {level}</h3>
        <a href='/dashboard'>Back to Dashboard</a>
        """

    return render_template('stress.html')


# Gemini API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")



@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    response_text = ""

    if request.method == 'POST':

        user_message = request.form['message']

        try:

            prompt = f"""
            You are MindFlow AI, a friendly mental health assistant.

            User says:
            {user_message}

            Give supportive, positive, and helpful advice.
            """

            response = model.generate_content(prompt)

            response_text = response.text

            cursor.execute(
                """
                INSERT INTO chat_history
                (user_id, user_message, ai_response)
                VALUES (%s, %s, %s)
                """,
                (
                    session['user_id'],
                    user_message,
                    response_text
                )
            )

            db.commit()

        except Exception as e:
            response_text = str(e)

    return render_template(
        'chatbot.html',
        response=response_text
    )


@app.route('/wellness-report')
def wellness_report():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Latest Mood
    cursor.execute("""
        SELECT mood
        FROM mood_logs
        WHERE user_id=%s
        ORDER BY id DESC
        LIMIT 1
    """, (session['user_id'],))
    mood = cursor.fetchone()

    # Latest Stress
    cursor.execute("""
        SELECT level
        FROM stress_assessment
        WHERE user_id=%s
        ORDER BY id DESC
        LIMIT 1
    """, (session['user_id'],))
    stress = cursor.fetchone()

    # Mood Count
    cursor.execute("""
        SELECT COUNT(*)
        FROM mood_logs
        WHERE user_id=%s
    """, (session['user_id'],))
    mood_count = cursor.fetchone()[0]

    # Chat Count
    cursor.execute("""
        SELECT COUNT(*)
        FROM chat_history
        WHERE user_id=%s
    """, (session['user_id'],))
    chat_count = cursor.fetchone()[0]

    return render_template(
        'report.html',
        mood=mood,
        stress=stress,
        mood_count=mood_count,
        chat_count=chat_count
    )
@app.route('/focus')
def focus():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template('focus.html')


@app.route('/save-focus', methods=['POST'])
def save_focus():

    if 'user_id' not in session:
        return "Login Required"

    sql = """
    INSERT INTO focus_sessions
    (
        user_id,
        session_name,
        start_time,
        end_time,
        status
    )
    VALUES
    (
        %s,
        'Pomodoro Session',
        NOW(),
        NOW(),
        'Completed'
    )
    """

    cursor.execute(sql, (session['user_id'],))
    db.commit()

    return "saved"
# ======================
# Logout
# ======================

@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login'))
@app.route('/mood-history')
def mood_history():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    sql = """
    SELECT mood, created_at
    FROM mood_logs
    WHERE user_id=%s
    ORDER BY created_at DESC
    """

    cursor.execute(sql, (session['user_id'],))
    moods = cursor.fetchall()

    return render_template(
        'mood_history.html',
        moods=moods
    )
    # ======================
# Stress Assessment
# ======================
@app.route('/stress-assessment', methods=['GET', 'POST'])
def stress_assessment():

    if request.method == 'POST':

        score = (
            int(request.form['q1']) +
            int(request.form['q2']) +
            int(request.form['q3']) +
            int(request.form['q4']) +
            int(request.form['q5'])
        )

        if score <= 7:
            level = "Low"
        elif score <= 14:
            level = "Moderate"
        else:
            level = "High"

        sql = """
        INSERT INTO stress_assessment(user_id, score, level)
        VALUES(%s,%s,%s)
        """

        cursor.execute(
            sql,
            (session['user_id'], score, level)
        )
        db.commit()

        return f"Stress Level: {level}"

    return render_template('stress_assessment.html')

# ======================
# Pomodoro Timer
# ======================

@app.route('/pomodoro')
def pomodoro():
    return render_template('pomodoro.html')

@app.route('/report')
def report():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Latest Mood
    cursor.execute("""
        SELECT mood, created_at
        FROM mood_logs
        WHERE user_id=%s
        ORDER BY id DESC
        LIMIT 1
    """, (session['user_id'],))
    mood = cursor.fetchone()

    # Latest Stress Assessment
    cursor.execute("""
        SELECT score, level
        FROM stress_assessment
        WHERE user_id=%s
        ORDER BY id DESC
        LIMIT 1
    """, (session['user_id'],))
    stress = cursor.fetchone()

    # Total Chat Messages
    cursor.execute("""
        SELECT COUNT(*)
        FROM chat_history
        WHERE user_id=%s
    """, (session['user_id'],))
    chats = cursor.fetchone()[0]

    return render_template(
        'report.html',
        mood=mood,
        stress=stress,
        chats=chats
    )



# ======================
# Run App
# ======================

if __name__ == '__main__':
    app.run(debug=True)