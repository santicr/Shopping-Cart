from flask import Flask, render_template, request, redirect, session, url_for
from controller import readItem, insertItem, readUser, insertUser

app = Flask(__name__)

@app.route('/')
def index():
    rows = readItem()
    return render_template('index.html', data = rows)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == "POST":
        user = request.form['user']
        pwd1 = request.form['passw1']
        pwd2 = request.form['passw2']
        if pwd1 == pwd2 and readUser(user):
            insertUser(user, pwd1)
            return redirect(url_for('index'))
        return redirect(url_for('error'))
    return render_template('register.html')

app.run(debug = True)