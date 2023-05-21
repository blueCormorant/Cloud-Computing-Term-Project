from flask import Flask, render_template, request
from config import Config
from forms import LoginForm, SignupForm
from celery import group
from tasks import translate_file
from tasks import tokenizer, model
from tasks import Response
import json
import nltk
import os
import logging

nltk.download('punkt')

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your_secret_key_here'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_file = os.path.join(os.getcwd(), 'event.log')
file_handler = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def chunk_text(text, max_tokens=50):
    tokens = nltk.word_tokenize(text)
    chunks = []

    current_chunk = []
    current_chunk_tokens = 0

    for token in tokens:
        if current_chunk_tokens + len(nltk.word_tokenize(token)) <= max_tokens:
            current_chunk.append(token)
            current_chunk_tokens += len(nltk.word_tokenize(token))
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [token]
            current_chunk_tokens = len(nltk.word_tokenize(token))

    chunks.append(' '.join(current_chunk))  # Add the last chunk

    return chunks

def postprocess_jobs(jobs):
    responses = sorted(jobs, key=lambda x: (x['filename'], x['index']))

    grouped_dict = {}
    for response in responses:
        try:
            grouped_dict[response["filename"]].append(response["text"])
        except KeyError:
            grouped_dict[response["filename"]] = []
            grouped_dict[response["filename"]].append(response["text"])
    
    grouped_list = []
    for filename in grouped_dict:
        file_dict = {}
        file_dict["filename"] = filename
        file_dict["text"] = " ".join(grouped_dict[filename])
        grouped_list.append(file_dict)

    return grouped_list


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.form.get('priority') is not None:
        priority = "high"
    else:
        priority = "low"
    files = request.files.getlist("file[]")
    files = [(file.filename, file.read().decode('utf-8')) for file in files]
    files = sorted(files, key=lambda file: len(file[1]))
    responses = []
    tasks = []
    for file in files:
        filename, text = file[0], file[1]
        logger.info(f"ARRIVE:{filename}:{priority}")
        for index, chunk in enumerate(chunk_text(text)):
            tasks.append(translate_file.subtask((filename, index, chunk)))

    # use a Celery group to run all tasks in parallel
    if priority == "high":
        # High priority queue
        print("high_priority")
        job = group(tasks).apply_async(queue="high_priority")
    else:
        # Low priority queue
        print("low_priority")
        job = group(tasks).apply_async(queue="low_priority")
        
    # wait for all tasks to complete
    job.join()

    # get the results of each task
    responses = postprocess_jobs(job.get())

    for response in responses:
        logger.info(f"RETURN:{response['filename']}:{priority}")

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
    app.run(debug=True, host="0.0.0.0", port=8000)
