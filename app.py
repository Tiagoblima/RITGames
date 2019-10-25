from flask import Flask, url_for
from flask import render_template

app = Flask(__name__, template_folder='templates')


@app.route('/')
def run_start(name=None):
    return index()


@app.route('/index.html')
def index(name=None):
    return render_template('index.html', name=name)


@app.route('/start.html')
def start(name=None):
    return render_template('start.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)
