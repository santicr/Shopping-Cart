from flask import Flask, render_template, request, redirect, session, url_for
from controller import *
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static'

app = Flask(__name__)
app.secret_key = "SECRET"
app.config['UPLOAD FOLDER'] = UPLOAD_FOLDER

@app.route('/add_cart/<itemId>/<user>', methods = ['GET'])
def add_cart(itemId, user):
    if 'user' not in session:
        return redirect(url_for('index'))
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
        lst = []
        total = 0

        for row in rows:
            data = {}
            data['item'] = row[0]
            data['cant'] = row[1]
            data['total'] = row[2]
            data['idIt'] = row[3]
            total += row[2]
            lst.append(data)

        return render_template('cart.html', lst = lst, user = user, total = total)
    return redirect(url_for('index'))

@app.route('/')
def index():
    rows = readItem()
    flag = 0
    amount = 0
    user, admin = "", ""
    
    if "user" in session:
        user = session["user"]
        lst = readCart(user)
        amount = 0
        for it in lst:
            amount += it[2]
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
        return redirect(url_for('index'))
    if "admin" in session:
        return render_template('admin.html')
    return redirect(url_for('index'))

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if 'user' in session or 'admin' in session:
        return redirect(url_for('index'))
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

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
        session.pop('items', None)
    elif 'admin' in session:
        session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if 'user' in session or 'admin' in session:
        return redirect(url_for('index'))
    if request.method == "POST":
        user = request.form['user']
        pwd1 = request.form['passw1']
        pwd2 = request.form['passw2']
        if pwd1 == pwd2 and readUser(user):
            insertUser(user, pwd1)
            return redirect(url_for('index'))
        return redirect(url_for('error'))
    return render_template('register.html')

@app.route('/remove_item/<idIt>', methods = ['GET'])
def remove_item(idIt):
    if "user" in session:
        if request.method == 'GET':
            deleteCart(idIt, session['user'])
        return redirect(url_for('cart'))
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug = True)