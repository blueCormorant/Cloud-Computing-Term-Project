from flask import Flask, render_template, request
from config import Config
from forms import LoginForm, SignupForm
from celery import group
from tasks import translate_file
from tasks import tokenizer, model
from tasks import Response
import json

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist("file[]")
    responses = []
    tasks = []
    for file in files:
        text = str(file.read().decode('utf-8'))
        filename = file.filename
        tasks.append(translate_file.subtask((filename, text)))

    # use a Celery group to run all tasks in parallel
    job = group(tasks).apply_async()

    # wait for all tasks to complete
    job.join()

    # get the results of each task
    responses = job.get()
    return render_template('index.html', responses=responses)

@app.route('/login', methods=["GET"])
def login_get():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form)

@app.route('/login', methods=['POST'])
def login_post():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form)

@app.route('/signup', methods=['GET'])
def signup_get():
    form = SignupForm()
    return render_template('signup.html', title='Signup', form=form)

@app.route('/signup', methods=['POST'])
def signup_post():
    form = SignupForm()
    return render_template('signup.html', title='Signup', form=form)

@app.route("/logout")
def logout():
    return redirect(url_for("login_get"))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
