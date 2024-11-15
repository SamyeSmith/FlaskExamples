from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': '123123',  # Replace with your MySQL password
    'database': 'profile_app'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Home page - profile display
@app.route('/')
def profile():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get user and experience data
    cursor.execute('SELECT * FROM users WHERE id = 1')
    user = cursor.fetchone()
    
    cursor.execute('SELECT * FROM experiences WHERE user_id = 1')
    experiences = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('profile.html', user=user, experiences=experiences)

# Add new experience
@app.route('/add_experience', methods=('GET', 'POST'))
def add_experience():
    if request.method == 'POST':
        job_title = request.form['job_title']
        company = request.form['company']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        description = request.form['description']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO experiences (user_id, job_title, company, start_date, end_date, description) VALUES (%s, %s, %s, %s, %s, %s)',
            (1, job_title, company, start_date, end_date, description)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('profile'))
    return render_template('add_experience.html')

# Edit experience
@app.route('/edit_experience/<int:id>', methods=('GET', 'POST'))
def edit_experience(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch the experience record to be edited
        cursor.execute('SELECT * FROM experiences WHERE id = %s', (id,))
        experience = cursor.fetchone()

        if not experience:
            return "Experience not found.", 404  # Handle case where the ID doesn't exist

        if request.method == 'POST':
            job_title = request.form['job_title']
            company = request.form['company']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            description = request.form['description']

            cursor.execute(
                '''
                UPDATE experiences 
                SET job_title = %s, company = %s, start_date = %s, end_date = %s, description = %s 
                WHERE id = %s
                ''',
                (job_title, company, start_date, end_date, description, id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('profile'))

        cursor.close()
        conn.close()
        return render_template('edit_experience.html', experience=experience)

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return "A database error occurred. Please try again later.", 500
    except Exception as e:
        print(f"Error: {e}")
        return "An unexpected error occurred. Please try again.", 500


# Delete experience
@app.route('/delete_experience/<int:id>')
def delete_experience(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM experiences WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run(debug=True)
