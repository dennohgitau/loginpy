from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'pass'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythonlogin'


mysql = MySQL(app)


@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username or password'

    return render_template('index.html', msg='')


@app.route('/pythonlogin/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES(NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered'
    elif request.method == 'POST' :
        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)


@app.route('/pythonlogin/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/pythonlogin/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return redirect(url_for('login'))


@app.route('/pythonlogin/home/Houses', methods=['GET', 'POST'])
def houses():
    '''if request.method == 'POST' and 'id' in request.form:
        id = request.form['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM houses WHERE id = %s', (id,))
        account = cursor.fetchone()
        mysql.connection.commit()
        return render_template('houses.html')
        '''

    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM houses')
        data = cursor.fetchall()
        return render_template('houses.html', value=data)


@app.route('/insert', methods=["POST"])
def insert():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        id = request.form['id']
        HouseNo = request.form['HouseNo']
        features = request.form['features']
        Rent = request.form['Rent']
        Status = request.form['Status']
        statement = "INSERT INTO houses (id, house_number, features, rent, status) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(statement), (id, HouseNo, features, Rent, Status)
        mysql.connection.commit()
        return redirect(url_for("houses"))


@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM houses WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('houses'))

@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        house_number = request.form['HouseNo']
        rent = request.form['rent']
        features = request.form['features']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE students
               SET id=%s, house_number=%s, rent=%s
               WHERE features=%s
            """, (id, house_number, rent, features))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('houses'))



@app.route('/pythonlogin/home/Tenants', methods=['GET'])
def tenants():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tenants')
        data = cursor.fetchall()
        return render_template('tenants.html', value=data)


@app.route('/pythonlogin/home/Payment', methods=['GET'])
def payment():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM payments')
        data = cursor.fetchall()
        return render_template('payments.html', value=data)


@app.route('/pythonlogin/home/Vacant', methods=['GET'])
def vacant():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM vacant')
        data = cursor.fetchall()
        return render_template('vacant.html', value=data)









