from flask import Flask, render_template, request, session, redirect
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Connect to the database
cnx = mysql.connector.connect(user='your_username',
                              password='your_password',
                              host='your_host',
                              database='your_database')

@app.route('/')
def index():
    if 'username' in session:
        return redirect('/home')
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register():
    # Get the form data
    username = request.form['username']
    password = request.form['password']
    name = request.form['name']

    # Create a cursor
    cursor = cnx.cursor()

    # Execute the query
    query = 'INSERT INTO users (name,username,password) VALUES (%s, %s, %s)'
    cursor.execute(query, (name,username, password))
    cnx.commit()

    # Close the cursor
    cursor.close()

    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    # Get the form data
    username = request.form['username']
    password = request.form['password']

    # Create a cursor
    cursor = cnx.cursor()

    # Execute the query
    query = 'SELECT * FROM users WHERE username = %s AND password = %s'
    cursor.execute(query, (username, password))

    # Fetch the results
    results = cursor.fetchone()

    # Close the cursor
    cursor.close()

    if results:
        # Create a session
        session['username'] = results[1]
        return redirect('/home')
    else:
        return 'Invalid username or password'

@app.route('/home')
def home():
    if 'username' in session:
        return 'Welcome, ' + session['username']
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
