from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route('/about')
def about():
    return 'About Page'

if __name__ == '__main__':
    app.run(debug=True)
t