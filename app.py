from flask import Flask
app= Flask(__name__)

@app.route("/")
def home():
    return "hello user"

@app.route("/naman")
def naman():
    return "hello naman"
app.debug = True

from controller  import *