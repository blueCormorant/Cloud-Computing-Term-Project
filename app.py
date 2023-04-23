from flask import Flask, render_template, request
from config import Config
from transformers import T5Tokenizer, TFT5ForConditionalGeneration
import tensorflow as tf
import logging
from forms import LoginForm, SignupForm

logging.getLogger('tensorflow').setLevel(logging.ERROR)

tokenizer = T5Tokenizer.from_pretrained('t5-small')
model = TFT5ForConditionalGeneration.from_pretrained('t5-small', return_dict=True)

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def index():
    return render_template('index.html')


# Rewrite the upload route to take multiple text files

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist("file[]")
    response = []
    for file in files:
        text = str(file.read().decode('utf-8'))
        input_ids = tokenizer("translate English to French: " + text, return_tensors="tf").input_ids
        outputs = model.generate(input_ids, max_length=512, num_beams=4, early_stopping=True)
        decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response.append(f"{decoded}\n")
    return render_template('index.html', response=response)

@app.route('/login', methods=["GET"])
def login_get():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form)

@app.route('/signup', methods=['GET'])
def signup_get():
    form = SignupForm()
    return render_template('signup.html', title='Signup', form=form)

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_id", None)    
    session.pop("logged_in", None)
    flash("You have been logged out")
    return redirect(url_for("login_get"))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
