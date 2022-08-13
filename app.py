from flask import Flask, render_template, request, redirect, session, url_for
from controller import *
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static'

app = Flask(__name__)
app.secret_key = "SECRET"
app.config['UPLOAD FOLDER'] = UPLOAD_FOLDER

@app.route('/add_cart/<int:itemId>/<user>', methods = ['GET'])
def add_cart(itemId, user):
    if request.method == 'GET':
        insertCart(user, itemId)
        if "items" in session:
            session["items"] += 1
        else:
            session["items"] = 1
        return redirect(url_for('index'))
    return redirect(url_for('error'))

@app.route('/cart')
def cart():
    if "user" in session:
        user = session["user"]
        rows = readCartItems(user)
        return render_template('cart.html', rows = rows)
    return redirect(url_for('index'))

@app.route('/')
def index():
    rows = readItem()
    flag = 0
    amount = 0
    user, admin = "", ""
    if "user" in session:
        user = session["user"]
        if "items" in session:
            amount = session["items"]
        else:
            amount = readCart(user)
            session["items"] = amount
        flag = 1
    elif "admin" in session:
        admin = session["admin"]
        flag = 2
    return render_template('index.html', data = rows, user = user, flag = flag, admin = admin, amount = amount)

@app.route('/admin', methods = ['POST', 'GET'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        quant = request.form['quant']
        price = request.form['price']
        desc = request.form['desc']
        file = request.files['file']
        filename = secure_filename(file.filename)
        data = [name, quant, price, 0, desc, 'static/' + file.filename]
        file.save(os.path.join(app.config['UPLOAD FOLDER'], filename))
        insertItem(data)
    if "admin" in session:
        return render_template('admin.html')
    return redirect(url_for('index'))

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        user = request.form['user']
        passw = request.form['passw']
        ans = existUser(user, passw)
        if ans:
            if ans == 1:
                session["user"] = user
            else:
                session["admin"] = user
            return redirect(url_for('index'))
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