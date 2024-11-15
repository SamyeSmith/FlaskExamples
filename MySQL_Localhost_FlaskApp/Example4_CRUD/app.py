from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flash messages

# Database configuration
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='123123',
        database='crud_app'
    )

# Home route - Read all users
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return render_template('index.html', users=users)

# Create user - Show form and handle submission
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)', (name, email, phone))
            conn.commit()
            flash('User created successfully!', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            conn.close()

        return redirect(url_for('index'))
    return render_template('create.html')

# Update user - Show form and handle submission
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cursor.execute('UPDATE users SET name = %s, email = %s, phone = %s WHERE id = %s', (name, email, phone, id))
        conn.commit()
        conn.close()
        flash('User updated successfully!', 'success')
        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM users WHERE id = %s', (id,))
    user = cursor.fetchone()
    conn.close()
    return render_template('update.html', user=user)

# Delete user
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
