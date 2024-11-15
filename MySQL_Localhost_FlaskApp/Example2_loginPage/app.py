from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Connect to the database
cnx = mysql.connector.connect(user='root',
                              password='123123',
                              host='localhost',
                              database='test')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    # Get the user's input from the form
    username = request.form['username']
    password = request.form['password']
    
    # Create a cursor
    cursor = cnx.cursor()

    # Check if the user exists in the database
    query = 'SELECT * FROM users WHERE username = %s AND password = %s'
    cursor.execute(query, (username, password))

    # Fetch the results
    results = cursor.fetchall()

    # If the user exists, log them in
    if results:
        session['username'] = username
        return redirect('/dashboard')

    # If the user doesn't exist, redirect to the Registeartion page
    else:
        return redirect('/Registration')

@app.route('/Registration',methods=['POST'])
def Registration():
    return render_template('Registration.html')
    #return redirect('/')

@app.route('/signup', methods=['POST'])
def signup():
    # Get the user's input from the form
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    cursor = cnx.cursor()
    query = 'INSERT INTO users (username, password, email) VALUES (%s, %s, %s)'
    cursor.execute(query, (username, password, email))
    cnx.commit()
    cursor.close()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html', username=username)
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)


# Resources 
# https://freefrontend.com/css-login-forms/