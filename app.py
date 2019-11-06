from flask import Flask, url_for, flash, redirect, request
from flask import render_template
from config import Config
from forms import RegistrationForm

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)


@app.route('/')
def run_start():
    return index()


@app.route('/index.html', methods=['GET', 'POST'])
def index(name=None):
    form = RegistrationForm(request.form)
    if form.validate_on_submit() and form.validate():
        flash("Cadastro Realizado com sucesso!")
        return redirect('/index.html')
    print(form.validate())
    return render_template('index.html', form=form)


@app.route('/start.html')
def start(name=None):
    return render_template('start.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)
