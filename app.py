from flask import Flask # TODO learn what WSGI is

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'