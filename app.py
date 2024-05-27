from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo, MongoClient
import os
from werkzeug.security import check_password_hash,generate_password_hash


app = Flask(__name__)
app.secret_key='raj'
app.config["MONGO_URI"] = os.getenv('mongo_url')
client=MongoClient(os.getenv('mongo_url'))
db=client['FitTrac']

#app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route('/about')
def about():
    return 'About Page'

if __name__ == '__main__':
    app.run(debug=True)