from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<p>Hello, this is a new app using Flask</p>'

app.run(debug = True)