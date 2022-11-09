from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
import os
import requests

UPLOAD_FOLDER = 'static'

app = Flask(__name__)
app.secret_key = "SECRET"
app.config['UPLOAD FOLDER'] = UPLOAD_FOLDER

@app.route('/add_cart/<item_id>/<user>', methods = ['GET'])
def add_cart(item_id, user):
    if 'user' not in session:
        return redirect(url_for('index'))
    if request.method == 'GET':
        fetch_verify_cart_res = requests.get(f"http://127.0.0.1:8000/api/cart/verify/{item_id}")
        if fetch_verify_cart_res:
            params = {
                "item_id": item_id,
                "user_name": user
            }
            row = requests.get("http://127.0.0.1:8000/api/cart/item", json = params).json()
            if not len(row):
                requests.post("http://127.0.0.1:8000/api/cart/item", json = params)
            else:
                params["new_quant"] = row[0][2] + 1
                requests.put('http://127.0.0.1:8000/api/cart/item', json = params)

            if "items" in session:
                session["items"] += 1
            else:
                session["items"] = 1
        return redirect(url_for('index'))
    return redirect(url_for('error', flag = 5, ans = -1))

@app.route('/remove_item/<int:item_id>', methods = ['GET'])
def remove_item(item_id: int):
    if "user" in session:
        if request.method == 'GET':
            user = session["user"]
            params = {
                'user_name': user,
                'item_id': item_id
            }
            row = requests.get('http://127.0.0.1:8000/api/cart/item', json = params).json()
            quant = row[0][2]
            if quant == 1:
                requests.delete('http://127.0.0.1:8000/api/cart/item', json = params)
            elif quant > 1:
                params["new_quant"] = quant - 1
                res = requests.put(f'http://127.0.0.1:8000/api/cart/item', json = params)
                print(res.json())
        return redirect(url_for('cart'))
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    if "user" in session:
        user = session["user"]
        rows = requests.get(f"http://127.0.0.1:8000/api/cart/items/{user}").json()
        lst = []
        total = 0

        for row in rows:
            data = {}
            data['item'] = row[0]
            data['cant'] = row[1]
            data['total'] = row[2]
            data['item_id'] = row[3]
            total += row[2]
            lst.append(data)

        ad = requests.get(f"http://127.0.0.1:8000/api/users/address/{user}").json()

        return render_template('cart.html', lst = lst, user = user, total = total, ad = ad)
    return redirect(url_for('index'))

@app.route('/')
def index():
    rows = requests.get('http://127.0.0.1:8000/api/items').json()
    print("auiiiii")
    print(rows)
    flag = 0
    amount = 0
    user, admin = "", ""
    
    if "user" in session:
        user = session["user"]
        lst = requests.get('http://127.0.0.1:8000/api/cart/user', params = {'user': user}).json()

        for l in lst:
            params = {
                "item_id": l[1],
                "quant2": l[2]
            }
            ans = requests.get('http://127.0.0.1:8000/api/items/user', params = params).json()
            for i in range(len(rows)):
                if rows[i][0] == l[1]:
                    rows[i][2] = ans

        amount = 0
        for it in lst:
            amount += it[2]
        flag = 1

    elif "admin" in session:
        admin = session["admin"]
        flag = 2
    return render_template('index.html', data = rows, user = user, flag = flag, admin = admin, amount = amount)

@app.route('/error/<int:flag>/<int:ans>')
def error(flag, ans):
    if "user" in session or "admin" in session:
        return render_template('error.html', flag = flag, ans = ans)

@app.route('/admin', methods = ['POST', 'GET'])
def admin():
    if "admin" in session:
        if request.method == 'POST':
            name = str(request.form['name'])
            quant = int(request.form['quant'])
            price = float(request.form['price'])
            desc = str(request.form['desc'])
            file = request.files['file']
            filename = secure_filename(file.filename)
            sold = 0
            file_upload = str('static/' + file.filename)
            file.save(os.path.join(app.config['UPLOAD FOLDER'], filename))
            fetch_verify_item_insert_res = requests.get(f"http://127.0.0.1:8000/api/items/verify/{name}/{quant}/{price}/{desc}")
            ans = fetch_verify_item_insert_res.json()
            if ans == 4:
                payload = {
                    'name': name,
                    'quant': quant,
                    'price': price,
                    'sold': sold,
                    'desc': desc,
                    'file_upload': file_upload
                }
                res = requests.post("http://127.0.0.1:8000/api/items", json = payload)
            else:
                return redirect(url_for('error', ans = ans, flag = 4))
            return redirect(url_for('index'))
        return render_template('admin.html')
    return redirect(url_for('index'))

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if 'user' in session or 'admin' in session:
        return redirect(url_for('index'))
    if request.method == "POST":
        user = request.form['user']
        passw = request.form['passw']
        params = {
            'user': user,
            'passw': passw
        }
        ans = requests.get('http://127.0.0.1:8000/api/users/user', params = params).json()
        if ans:
            if ans == 1:
                session["user"] = user
            elif ans == 2:
                session["admin"] = user
            return redirect(url_for('index'))
        return redirect(url_for('error', flag = 5, ans = -1))
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
        params = {'user': user}
        if pwd1 == pwd2 and requests.get('http://127.0.0.1:8000/api/users/exist', params = params).json():
            params = {
                'name': user,
                'passw': pwd1
            }
            res = requests.post('http://127.0.0.1:8000/api/users/user', json = params)
            return redirect(url_for('index'))
        return redirect(url_for('error', flag = 6, ans = -1))
    return render_template('register.html')

@app.route('/address', methods = ['POST', 'GET'])
def address():
    if "user" in session:
        if request.method == 'POST':
            user_name = session['user']
            add = request.form['add']
            city = request.form['city']
            phone = request.form['phone']
            params = {
                "user_name": user_name,
                "add": add,
                "city": city,
                "phone": phone
            }
            requests.post('http://127.0.0.1:8000/api/users/address', json = params)
            return redirect(url_for('cart'))
        return render_template('address.html')
    return redirect(url_for('index'))

@app.route('/pay/<user>', methods = ['GET'])
def pay(user):
    if "user" in session:
        if request.method == 'GET':
            return render_template('pay.html')
    return redirect(url_for('index'))

@app.route('/discount/<total>', methods = ['GET'])
def disc(total):
    if 'user' in session:
        return render_template('discount.html', total = total)
    return url_for(redirect('index'))

@app.route('/payProcess', methods = ['POST'])
def payProcess():
    if "user" in session:
        user = session['user']
        if request.method == 'POST':
            name = request.form['name']
            lname1 = request.form['lname1']
            lname2 = request.form['lname2']
            ccnum = request.form['number']
            ccv = request.form['code']
            params = {
                'user_name': user,
                'name': name,
                'lname1': lname1,
                'lname2': lname2,
                'ccnum': ccnum,
                'ccv': ccv
            }
            ans = requests.get('http://127.0.0.1:8000/api/payments/pay', json = params).json()
            print(ans)
            if ans <= 2: return redirect(url_for('error', flag = ans, ans = 10))
            elif ans == 3: return redirect(url_for('index'))
            elif ans > 3: return redirect(url_for('disc', total = ans))

@app.route('/references')
def references():
    if 'user' in session:
        user = session['user']
        references = requests.get('http://127.0.0.1:8000/api/auxiliaries/ref', json = {'user_name': user}).json()
        return render_template('references.html', user = user, references = references)
    return redirect(url_for('index'))

@app.route('/search', methods = ['POST', 'GET'])
def searchReference():
    if 'user' in session:
        user = session['user']
        products = []
        if request.method == 'POST':
            ref = request.form['ref']
            products = requests.get('http://127.0.0.1:8000/api/auxiliaries/search', json = {'reference': ref}).json()
        return render_template('searchref.html', products = products)
    return redirect(url_for('index'))

@app.route('/transaction', methods = ['POST', 'GET'])
def transaction():
    if 'user' in session:
        user = session['user']
        data = requests.get('http://127.0.0.1:8000/api/auxiliaries/bought', json = {'user_name': user}).json()
        return render_template('transaction.html', data = data)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug = True)