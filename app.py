from flask import Flask, render_template, request, redirect
from controller import readItem, insertItem

app = Flask(__name__)

@app.route('/')
def index():
    rows = readItem()
    return render_template('index.html', data = rows)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == "POST":
        return '<p>Hello, this is POST</p>'
    return render_template('register.html')

app.run(debug = True)