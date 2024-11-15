from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    """Utility function to get a new database connection using a context manager."""
    return mysql.connector.connect(
        host='localhost',       
        user='root',   
        password='123123',  
        database='test'
    )

def get_user_data(username):
    """Fetch user data by username."""
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT email FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()
    
    if user_data:
        return {
            'email': user_data[0]
        }
    return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    # Get the user's input from the form
    username = request.form['username']
    password = request.form['password']
    
    # Query the database to verify user credentials
    with get_db_connection() as connection:
        cursor = connection.cursor()
        query = 'SELECT * FROM users WHERE username = %s AND password = %s'
        cursor.execute(query, (username, password))
        results = cursor.fetchall()

    # If the user exists, log them in
    if results:
        session['username'] = username
        user_data = get_user_data(session['username']) 
        return render_template('Profilepage.html',user=user_data)

    # If the user doesn't exist, redirect to the Registration page
    return redirect('/Registration')

@app.route('/Registration', methods=['GET', 'POST'])
def Registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        with get_db_connection() as connection:
            cursor = connection.cursor()
            query = 'INSERT INTO users (username, password, email) VALUES (%s, %s, %s)'
            cursor.execute(query, (username, password, email))
            connection.commit()
        
        return redirect('/')
    return render_template('Registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html', username=username)
    else:
        return redirect('/')

@app.route('/profile')
def profile():
    if 'username' in session:
        user_data = get_user_data(session['username'])
        if user_data:
            return render_template('ProfilePage.html', user=user_data)
        else:
            return "User not found", 404
    else:
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session.pop('username', None)  # Ensure the session is cleared on logout
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
