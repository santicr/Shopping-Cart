from flask import Flask, render_template, request, redirect, session, url_for
from controller import readItem, insertItem, readUser, insertUser, existUser

app = Flask(__name__)
app.secret_key = "SECRET"

@app.route('/')
def index():
    rows = readItem()
    flag = False
    user = ""
    if "user" in session:
        user = session["user"]
        flag = True
    return render_template('index.html', data = rows, user = user, flag = flag)

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        user = request.form['user']
        passw = request.form['passw']
        if existUser(user, passw):
            session["user"] = user
        return redirect(url_for('error'))
    return render_template('login.html')

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

if __name__ == "__main__":
    app.run(debug = True)